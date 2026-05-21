"""Designer — synthesizes advisor outputs into a concrete Exercise Spec.

Inputs (all three advisors run in parallel before this):
- vocab:        list[dict]   from Dutch Expert
- presentation: dict         from Dyslexia Expert
- phonetics:    dict         from Phonetics Specialist

Output:
- A JSON object matching schemas.ExerciseSpec (validated by the Manager).

Designer decisions:
- Respects Dyslexia Expert's max_items_per_session, favor/avoid lists, color codes.
- Mixes exercise types: listen_and_repeat for every item, plus minimal_pair drills
  for any vocab item whose tricky_sounds overlap with a phonetics minimal pair.
- Adds flashcards last for spaced review of meaning.
"""
from __future__ import annotations

import json as _json
from .base import call_claude_json

SYSTEM = """You are an instructional designer for a dyslexia-friendly Dutch app.

Combine the three inputs below into a single Exercise Spec JSON.

Rules:
- Honor `presentation.max_items_per_session` — never exceed it. Trim vocab if needed.
- Order items from phonetically simple to tricky (see presentation.ordering_notes).
- Every vocab item gets a "listen_and_repeat" exercise.
- For each phonetics.minimal_pair, add ONE "minimal_pair" exercise after the
  listen_and_repeat items.
- End the session with one "flashcard" exercise per vocab item.
- Skip any exercise type listed in presentation.avoid.
- Populate dyslexia_hints.chunks from phonetics.syllables.
- Populate dyslexia_hints.color_code from presentation.color_codes, but only
  include keys whose digraph actually appears in this item's dutch text.
- audio_url MUST be null (the backend fills it later from Azure TTS).
- session_id MUST be the literal string "PLACEHOLDER" (the Manager replaces it).

Return ONLY a JSON object inside a ```json fence matching this shape:

{
  "session_id": "PLACEHOLDER",
  "topic": "<string>",
  "items": [
    {
      "type": "listen_and_repeat" | "minimal_pair" | "flashcard" | "type_what_you_hear",
      "dutch": "<string>",
      "english": "<string or null>",
      "ipa": "<string>",
      "tricky_sounds": ["<ipa symbol>", ...],
      "audio_url": null,
      "dyslexia_hints": {
        "chunks": ["<chunk>", ...],
        "color_code": { "<digraph>": "<hex>" }
      },
      "minimal_pair": null OR {
        "dutch_a": "...", "ipa_a": "...",
        "dutch_b": "...", "ipa_b": "...",
        "contrast": "..."
      }
    }
  ]
}
"""

PROMPT = """topic: {topic}

vocab (from Dutch Expert):
{vocab}

presentation (from Dyslexia Expert):
{presentation}

phonetics (from Phonetics Specialist):
{phonetics}
"""


def run(*, topic: str, vocab: list[dict], presentation: dict, phonetics: dict) -> dict:
    user = PROMPT.format(
        topic=topic,
        vocab=_json.dumps(vocab, ensure_ascii=False, indent=2),
        presentation=_json.dumps(presentation, ensure_ascii=False, indent=2),
        phonetics=_json.dumps(phonetics, ensure_ascii=False, indent=2),
    )
    return call_claude_json(SYSTEM, user, max_tokens=4096)
