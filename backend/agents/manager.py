"""Manager — orchestrates the full agent pipeline.

Pipeline:
    Dutch Expert ─┐
    Dyslexia    ─┼─ (parallel) → Designer → validate → ExerciseSpec
    Phonetics   ─┘

The Manager also:
- Picks a session_id (uuid).
- Validates the Designer's output against the Pydantic schema.
- Retries the Designer once on schema failure, including the validation error
  in the retry prompt so it can self-correct.
"""
from __future__ import annotations

import uuid
from concurrent.futures import ThreadPoolExecutor

from pydantic import ValidationError

from schemas import ExerciseSpec, GenerateRequest

from . import dutch_expert, dyslexia_expert, phonetics, designer
from .base import call_claude_json


def generate(req: GenerateRequest) -> ExerciseSpec:
    topic = req.text.strip() if req.mode == "topic" else "from your lesson"

    vocab = dutch_expert.run(mode=req.mode, text=req.text, max_items=req.max_items)

    with ThreadPoolExecutor(max_workers=2) as pool:
        f_presentation = pool.submit(dyslexia_expert.run, vocab)
        f_phonetics = pool.submit(phonetics.run, vocab)
        presentation = f_presentation.result()
        phonetics_data = f_phonetics.result()

    spec_dict = designer.run(
        topic=topic,
        vocab=vocab,
        presentation=presentation,
        phonetics=phonetics_data,
    )
    spec_dict["session_id"] = str(uuid.uuid4())

    try:
        return ExerciseSpec.model_validate(spec_dict)
    except ValidationError as e:
        repaired = _repair_spec(spec_dict, str(e))
        repaired["session_id"] = spec_dict["session_id"]
        return ExerciseSpec.model_validate(repaired)


_REPAIR_SYSTEM = """You are fixing a JSON document so it matches a Pydantic schema.
Return ONLY the corrected JSON inside a ```json fence. Do not add prose.
"""

_REPAIR_PROMPT = """The following JSON failed schema validation.

JSON:
{spec}

Validation errors:
{errors}

Return the corrected JSON.
"""


def _repair_spec(spec: dict, errors: str) -> dict:
    import json as _json
    user = _REPAIR_PROMPT.format(
        spec=_json.dumps(spec, ensure_ascii=False, indent=2),
        errors=errors,
    )
    return call_claude_json(_REPAIR_SYSTEM, user, max_tokens=4096)
