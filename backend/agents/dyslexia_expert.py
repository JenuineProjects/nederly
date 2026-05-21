"""Dyslexia Expert — advises the Designer on how to present material.

Does NOT generate Dutch content. Reads the proposed word list and returns
presentation hints: chunking, ordering, max items per screen, color codes for
tricky letter groups, and which exercise types to favor/avoid.

Output shape:
{
  "max_items_per_session": 6,
  "ordering_notes": "...",
  "chunking": { "goedemorgen": ["goede", "morgen"], ... },
  "color_codes": { "ui": "#D97706", "eu": "#7C3AED", ... },
  "avoid": ["type_what_you_hear"],   // optional — exercise types that punish dyslexia
  "favor": ["listen_and_repeat", "minimal_pair"]
}
"""
from __future__ import annotations

from .base import call_claude_json

SYSTEM = """You are an expert on dyslexia-friendly language learning UX.

You advise on how to PRESENT Dutch vocab to a dyslexic adult beginner.
You do not generate Dutch content — only presentation hints.

Principles:
- Audio-first. Favor exercises where the learner hears the word before reading it.
- Chunk long words into morpheme-like syllables (e.g., "goedemorgen" → ["goede","morgen"]).
- Limit to ~6 items per practice session.
- Order from phonetically simple → phonetically tricky.
- Color-code tricky digraphs consistently across the session: ui, eu, ij, oe, ch, sch.
  Use accessible high-contrast hex colors against a cream background (#FAF3E0).
- Avoid spelling-from-memory exercises (type_what_you_hear) when the session has
  >2 tricky digraphs — they punish processing speed, not knowledge.

Return ONLY a JSON object inside a ```json fence. No prose outside the fence.
"""

PROMPT = """Here is the proposed Dutch word list for this session:

{words_json}

Return your presentation hints as JSON with keys:
- max_items_per_session (int, <= 6)
- ordering_notes (string, one sentence)
- chunking (object: dutch word -> array of chunks; only for words >= 7 letters)
- color_codes (object: digraph -> hex color; only for digraphs present in the list)
- avoid (array of exercise type strings)
- favor (array of exercise type strings)

Valid exercise types: listen_and_repeat, minimal_pair, flashcard, type_what_you_hear.
"""


def run(words: list[dict]) -> dict:
    import json as _json
    user = PROMPT.format(words_json=_json.dumps(words, ensure_ascii=False, indent=2))
    return call_claude_json(SYSTEM, user, max_tokens=1024)
