"""Modeller for spillet."""

import uuid
from pydantic import BaseModel

TYPE_SPØRSMÅL = "SPØRSMÅL"
TYPE_SVAR = "SVAR"
TYPE_KORREKTUR = "KORREKTUR"


class Svar(BaseModel):
    """Et svar til et spørsmål."""

    spørsmålId: str
    kategori: str
    lagnavn: str = ""
    svar: str = ""
    svarId: str = str(uuid.uuid4())


class Spørsmål(BaseModel):
    """Et spørsmål som venter på et svar."""

    id: str
    kategori: str
    spørsmål: str
    svarformat: str
    dokumentasjon: str

class Question(BaseModel):
    """A question waiting for an answer."""

    id: str
    category: str
    question: str
    answer_format: str
    documentation: str
