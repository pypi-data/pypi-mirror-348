# Leesah Python in English

🇧🇻 Du finner den norske utgaven [lengre ned](#leesah-python-på-norsk).

> Leesah-game is an event-driven application development game that challenges players to build an event-driven application.
> The application handles different types of tasks that it receives as events on a Kafka-based event stream.
> The tasks vary from very simple to more complex.

This is the Python library to play Leesah!

## Getting started

There are two versions of the the Leesah game!
On is for local play, directly in the terminal.
While the other is running on the Nais platform, and you learn how to be a developer in Nav and use Nais.
This library is used by both versions, but the following documentation is **just** for local play.

### Setting up local environment

We recommend to use a virtual environment when playing Leesah, for example using [Venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

Start by creating the folder `leesah-game`.
Then set up the virtual environment using the following commands.

**For macOS/Linux**
```shell
cd leesah-game
python3 -m venv venv
source ./venv/bin/activate
```

**For Windows**
```shell
cd leesah-game
python3 -m venv venv
.\venv\Scripts\activate
```

### Install the library

There is only one dependency you need to play, and that is the [leesah-game](https://pypi.org/project/leesah-game/) library.

```shell
python3 -m pip install leesah-game
```

### Fetch Kafka certificates

You need some certificates to connect to the Kafka cluster, which is available at [leesah.io/certs](https://leesah.io/certs).
The username is always `leesah-game`, and the password will be distributed.

You can also use the one-liner below:

```bash
curl -u leesah-game:<see presentation> -o leesah-certs.zip https://leesah.io/certs && unzip leesah-certs.zip
```

Using the command above you will end up with `leesah-certs.yaml` in the `leesah-game` directory you made earlier.

### Example code

To make it easy to start we have made a working example that answer the first question, `team-registration`, with a dummy name and color.
All you need to do is update `TEAM_NAME` and `HEX_CODE`, and your ready to compete!

Create a file called `main.py` and paste the code below.

```python
"""Play Leesah Game

1. Download the Kafka certificate, and make sure that you have a file called leesah-certs.yaml in the same directory as this file
2. Set your own 'TEAM_NAME'
3. Set your own 'HEX_CODE' as team color
"""
import leesah

TEAM_NAME = "CHANGE ME"
HEX_CODE = "CHANGE ME"


class Rapid(leesah.QuizRapid):
    """The class that will answer the questions."""

    def run(self):
        """Start quiz!

        We recommend that you use seperate functions to answer each question.
        """
        while True:
            message = self.fetch_question()
            if message.category == "team-registration":
                self.handle_team_registration(message.question)

    def handle_team_registration(self, message):
        self.publish_answer(HEX_CODE)


if __name__ == "__main__":
    rapid = Rapid(TEAM_NAME, ignored_categories=[
        # "team-registration",
    ])

    try:
        rapid.run()
    except (KeyboardInterrupt, SystemExit):
        rapid.close()
```

### Running code

Run you code:

```shell
python3 main.py
```

# Leesah Python på norsk

🇬🇧 Go [further up](#leesah-python-in-english) for the English documentation.

> Leesah-game er et hendelsedrevet applikasjonsutviklingspill som utfordrer spillerne til å bygge en hendelsedrevet applikasjon. 
> Applikasjonen håndterer forskjellige typer oppgaver som den mottar som hendelser på en Kafka-basert hendelsestrøm. 
> Oppgavene varierer fra veldig enkle til mer komplekse.

Python-bibliotek for å spille Leesah!

## Kom i gang

Det finnes to versjoner av Leesah-game!
En hvor man lager en applikasjon som kjører på Nais, og en hvor man spiller lokalt direkte fra terminalen.
Dette biblioteket kan brukes i begge versjoner, men denne dokumentasjonen dekker **kun** lokal spilling.

### Sett opp lokalt miljø

Vi anbefaler at du bruker et virtuelt miljø for å kjøre koden din, som for eksempel [Venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

Start med å opprette en katalog `leesah-game`.

**For macOS/Linux**
```shell
cd leesah-game
python3 -m venv venv
source ./venv/bin/activate
```

**For Windows**
```shell
cd leesah-game
python3 -m venv venv
.\venv\Scripts\activate
```

### Installer biblioteket

Det er kun en avhengighet du trenger, og det er biblioteket [leesah-game](https://pypi.org/project/leesah-game/).

```shell
python3 -m pip install leesah-game
```

### Hent Kafkasertifikat

Sertifikater for å koble seg på Kafka ligger tilgjengelig på [leesah.io/certs](https://leesah.io/certs), passord får du utdelt.

Du kan også bruke kommandoen nedenfor:

```bash
curl -u leesah-game:<se presentasjon> -o leesah-certs.zip https://leesah.io/certs && unzip leesah-certs.zip
```

Du vil nå ende opp med filen `leesah-certs.yaml` i `leesah-game`-katalogen du lagde tidligere.

### Eksempelkode

For å gjøre det enklere å komme i gang har vi et fungerende eksempel som svarer på spørsmålet om lagregistrering med et navn og en farge (hexkode).
Opprett filen `main.py` og lim inn koden nedenfor.

```python
"""Spill Leesah Game

1. Hent ned sertifikater, og sikre deg at de ligger i filen leesah-certs.yaml
2. Sett 'LAGNAVN' til ditt valgte lagnavn
3. Sett 'HEXKODE' til din valgte farge
"""
import leesah

LAGNAVN = "BYTT MEG"
HEXKODE = "BYTT MEG"


class Rapid(leesah.KvissRapid):
    """Klassen som svarer på spørsmålene."""

    def kjør(self):
        """Start quizen!

        Vi anbefaler at du bruker funksjoner til å svare på spørsmålene.
        """
        while True:
            melding = self.hent_spørsmål()
            if melding.kategori == "lagregistrering":
                self.behandle_lagregistrering(melding.spørsmål)

    def behandle_lagregistrering(self, spørsmål):
        self.publiser_svar(HEXKODE)


if __name__ == "__main__":
    rapid = Rapid(LAGNAVN, ignorerte_kategorier=[
        # "lagregistrering",
    ])

    try:
        rapid.kjør()
    except (KeyboardInterrupt, SystemExit):
        rapid.avslutt()
```

### Kjør koden

Kjør koden din med:

```shell
python3 main.py
```
