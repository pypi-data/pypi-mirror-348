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
from .modeller import Svar, Question, TYPE_SVAR, TYPE_SPØRSMÅL, TYPE_KORREKTUR


class QuizRapid:
    """The quiz rapid for questions and answers."""

    def __init__(
        self,
        team_name: str,
        ignored_categories: list = [],
        topic: str | None  = os.getenv("QUIZ_TOPIC"),
        consumer_group_id: str = str(uuid.uuid4()),
        path_to_certs: str = os.environ.get("QUIZ_CERTS", "leesah-certs.yaml"),
        auto_commit: bool = False,
    ):
        """
        Constructs all the necessary attributes for a Quiz object.

        Parameters
        ----------
            team_name : str
                team name to publish messages with
            ignored_categories : list
                list of categories to ignore (default is an empty list)
            topic : str
                topic to produce and consume messages on (default is first topic in certs file)
            consumer_group_id : str
                the kafka consumer group id to commit offset on (default is random uuid)
            path_to_certs : str
                path to the certificate file (default is leesah-certs.yaml)
            auto_commit : bool, optional
                auto commit offset for the consumer (default is False)
        """
        print("🚀 Starting...")
        certs_path = Path(path_to_certs)
        if not certs_path.exists():
            if Path("certs/leesah-certs.yaml").exists():
                certs_path = Path("certs/leesah-certs.yaml")
            else:
                raise FileNotFoundError(
                    f"Could not find certs: {path_to_certs} or {certs_path}"
                )

        certs = yaml.load(certs_path.open(mode="r").read(), Loader=SafeLoader)
        if not topic:
            self._topic = certs["topics"][0]
        else:
            self._topic = topic

        consumer = Consumer(consumer_config(certs, consumer_group_id, auto_commit))
        consumer.subscribe([self._topic])

        producer = Producer(producer_config(certs))

        self.running = True
        self._team_name = team_name
        self._producer: Producer = producer
        self._consumer: Consumer = consumer
        self._ignored_categories = ignored_categories
        print("🔍 Looking for the first question")

    def fetch_question(self):
        """Retrieves the next question from the quiz."""
        while self.running:
            msg = self._consumer.poll(timeout=1)
            if msg is None:
                continue

            if msg.error():
                self._handle_error(msg)
            else:
                question = self._handle_message(msg)
                if question:
                    print(f"📥 Received question: {question}")
                    return question

    def _handle_error(self, msg):
        """Handles errors from the consumer."""
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print(
                "{} {} [{}] reached end at offset\n".format(
                    msg.topic(), msg.partition(), msg.offset()
                )
            )
        elif msg.error():
            raise KafkaException(msg.error())

    def _handle_question(self, msg):
        self._last_message = msg

        return Question(
            category=msg["kategori"],
            question=msg["spørsmål"],
            answer_format=msg["svarformat"],
            id=msg["spørsmålId"],
            documentation=msg["dokumentasjon"],
        )

    def _handle_feedback(self, msg):
        """Handles feedback from the consumer."""
        if msg["lagnavn"] != self._team_name:
            return

        if msg["korrektur"] != "KORREKT":
            print(f"❌ You answered incorrectly: id='{msg['spørsmålId']}' category='{msg['kategori']}'")
            return

        print(f"✅ You answered correctly: id='{msg['spørsmålId']}' category='{msg['kategori']}'")

    def _handle_message(self, blob):
        """Handles messages from the consumer."""
        try:
            msg = json.loads(blob.value().decode("utf-8"))
        except JSONDecodeError as e:
            print(f"error: could not decode message: {blob}, error: {e}")
            return

        if "kategori" in msg and msg["kategori"] in self._ignored_categories:
            return

        try:
            if msg["@event_name"] == TYPE_SPØRSMÅL:
                return self._handle_question(msg)
            elif msg["@event_name"] == TYPE_KORREKTUR:
                self._handle_feedback(msg)
        except KeyError as e:
            print(f"error: unknown message: {msg}, missing key: {e}")
            return

    def publish_answer(self, svar: str):
        """Publishes an answer to the quiz."""
        try:
            if svar:
                msg = self._last_message
                answer = Svar(
                    spørsmålId=msg["spørsmålId"],
                    kategori=msg["kategori"],
                    lagnavn=self._team_name,
                    svar=svar,
                ).model_dump()
                answer["@event_name"] = TYPE_SVAR

                print(f"📤 Published answer: category='{msg['kategori']}' answer='{svar}' teamName='{self._team_name}'")

                value = json.dumps(answer).encode("utf-8")
                self._producer.produce(topic=self._topic, value=value)
                self._last_message = None
        except KeyError as e:
            print(f"error: unknown answer: {msg}, missing key: {e}")
        except TypeError:
            stack = traceback.format_stack()
            print("DoubleAnswerException (are you trying to answer twice in a row?):")
            for line in stack:
                if "quiz_rapid.py" in line:
                    break
                print(line, end="")
            exit(1)

    def close(self):
        """Closing quiz."""
        print("🛑 Shutting down...")
        self.running = False
        self._producer.flush()
        self._consumer.close()
        self._consumer.close()
