from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


ItemType = Literal["listen_and_repeat", "minimal_pair", "flashcard", "type_what_you_hear"]


class DyslexiaHints(BaseModel):
    chunks: list[str] = Field(default_factory=list)
    color_code: dict[str, str] = Field(default_factory=dict)


class MinimalPair(BaseModel):
    dutch_a: str
    dutch_b: str
    ipa_a: str
    ipa_b: str
    contrast: str


class ExerciseItem(BaseModel):
    type: ItemType
    dutch: str
    english: str | None = None
    ipa: str
    tricky_sounds: list[str] = Field(default_factory=list)
    audio_url: str | None = None
    dyslexia_hints: DyslexiaHints = Field(default_factory=DyslexiaHints)
    minimal_pair: MinimalPair | None = None


class ExerciseSpec(BaseModel):
    session_id: str
    topic: str
    items: list[ExerciseItem]


class GenerateRequest(BaseModel):
    mode: Literal["paste", "topic"]
    text: str
    max_items: int = 8


class PronunciationScore(BaseModel):
    word: str
    accuracy: float
    fluency: float | None = None
    completeness: float | None = None
    phonemes: list[PhonemeScore] = Field(default_factory=list)


class PhonemeScore(BaseModel):
    phoneme: str
    accuracy: float


PronunciationScore.model_rebuild()
