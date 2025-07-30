import json
import uuid
import os
import yaml
import traceback

from datetime import datetime
from pathlib import Path
from yaml.loader import SafeLoader
from json import JSONDecodeError
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException

from .kafka_config import consumer_config, producer_config
from .modeller import Svar, Spørsmål, TYPE_SVAR, TYPE_SPØRSMÅL, TYPE_KORREKTUR


class KvissRapid:
    """Kvissformidler av spørsmål og svar.

    Til og fra stryket på vegne av deltakerne.
    """

    def __init__(
        self,
        lagnavn: str,
        ignorerte_kategorier: list = [],
        topic: str | None = os.getenv("QUIZ_TOPIC"),
        consumer_group_id: str = str(uuid.uuid4()),
        path_to_certs: str = os.environ.get("QUIZ_CERTS", "leesah-certs.yaml"),
        auto_commit: bool = False,
    ):
        """
        Konstruerer alle de nødvendige attributtene for et Kvissobjekt.

        Parametere
        ----------
            lagnavn : str
                lagnavn for å publisere meldinger med
            ignorerte_kategorier : list
                liste av kategorier som ikke skal logges (default er en tom liste)
            topic : str
                topic to produce and consume messages on (default is first topic in certs file)
            consumer_group_id : str
                the kafka consumer group id to commit offset on (default is random uuid)
            path_to_certs : str
                path to the certificate file (default is leesah-certs.yaml)
            auto_commit : bool, optional
                auto commit offset for the consumer (default is False)
        """
        print("🚀 Starter opp...")
        certs_path = Path(path_to_certs)
        if not certs_path.exists():
            if Path("certs/leesah-certs.yaml").exists():
                certs_path = Path("certs/leesah-certs.yaml")
            else:
                raise FileNotFoundError(
                    f"Kunne ikke finne sertifikater: {path_to_certs} eller {certs_path}"
                )

        certs = yaml.load(certs_path.open(mode="r").read(), Loader=SafeLoader)
        if not topic:
            self._topic = certs["topics"][0]
        else:
            self._topic = topic

        konsument = Consumer(consumer_config(certs, consumer_group_id, auto_commit))
        konsument.subscribe([self._topic])

        produsent = Producer(producer_config(certs))

        self.kjører = True
        self._lagnavn = lagnavn
        self._producer: Producer = produsent
        self._consumer: Consumer = konsument
        self._ignorerte_kategorier = ignorerte_kategorier
        print("🔍 Ser etter første spørsmål")


    def hent_spørsmål(self):
        """Henter neste spørsmål fra stryket."""
        while self.kjører:
            melding = self._consumer.poll(timeout=1)
            if melding is None:
                continue

            if melding.error():
                self._håndter_feil(melding)
            else:
                spørsmål = self._håndter_melding(melding)
                if spørsmål:
                    if spørsmål.kategori not in self._ignorerte_kategorier:
                        print(f"📥 Mottok spørsmål: {spørsmål}")
                    return spørsmål

    def _håndter_feil(self, melding):
        """Behandler feil fra forbrukeren."""
        if melding.error().code() == KafkaError._PARTITION_EOF:
            print(
                "{} {} [{}] kom til enden av offset\n".format(
                    melding.topic(), melding.partition(), melding.offset()
                )
            )
        elif melding.error():
            raise KafkaException(melding.error())

    def _håndter_melding(self, melding_blob):
        """Håndterer meldinger fra konsumenten."""
        try:
            melding = json.loads(melding_blob.value().decode("utf-8"))
        except JSONDecodeError as e:
            print(f"feil: kunne ikke lese meldingen: {melding_blob.value()}, feil: {e}")
            return

        if "kategori" in melding and melding["kategori"] not in self._ignorerte_kategorier:
            return

        try:
            if melding["@event_name"] == TYPE_SPØRSMÅL:
                return self._håndter_spørsmål(melding, TopicPartition(melding_blob.topic(), melding_blob.partition(), melding_blob.offset()))
            elif melding["@event_name"] == TYPE_KORREKTUR:
                return self._håndter_korrektur(melding)
        except KeyError as e:
            print(f"feil: ukjent melding: {melding}, mangler nøkkel: {e}")

        return None

    def _håndter_spørsmål(self, melding, topicPartition):
        self._siste_melding = melding
        self._siste_topicPartition = topicPartition

        return Spørsmål(
            kategori=melding["kategori"],
            spørsmål=melding["spørsmål"],
            svarformat=melding["svarformat"],
            id=melding["spørsmålId"],
            dokumentasjon=melding["dokumentasjon"],
        )

    def _håndter_korrektur(self, melding):
        """Håndterer korrekturmeldinger."""
        if melding["lagnavn"] != self._lagnavn: # or melding["spørsmålId"] in self._svar:
            return

        if melding["korrektur"] != "KORREKT":
            print(f"❌ Du svarte feil på et spørsmål: id='{melding['spørsmålId']}' kategori='{melding['kategori']}'")
            return

        print(f"✅ Du svarte riktig på et spørsmål: id='{melding['spørsmålId']}' kategori='{melding['kategori']}'")

    def publiser_svar(self, svar: str):
        """Publiserer et svar til stryket."""
        try:
            if svar:
                melding = self._siste_melding

                answer = Svar(
                    spørsmålId=melding["spørsmålId"],
                    kategori=melding["kategori"],
                    lagnavn=self._lagnavn,
                    svar=svar,
                ).model_dump()
                answer["@event_name"] = TYPE_SVAR

                print(f"📤 Publisert svar: kategori='{melding['kategori']}' svar='{svar}' lagnavn='{self._lagnavn}'")

                value = json.dumps(answer).encode("utf-8")
                self._producer.produce(topic=self._topic, value=value)
                self._siste_melding = None
        except KeyError as e:
            print(f"feil: ukjent svar: {melding}, mangler nøkkel: {e}")
        except TypeError:
            spor = traceback.format_stack()
            print("DobbeltSvarException (prøver du å svare to ganger på rad?):")
            for linje in spor:
                if "quiz_rapid.py" in linje:
                    break
                print(linje, end="")
            exit(1)

    def avslutt(self):
        """Avslutter kviss."""
        print("🛑 Stenger ned...")
        self.kjører = False
        self._producer.flush()
        self._consumer.close()
