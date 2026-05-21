"""Dutch Expert — produces accurate A0/A1 vocab content.

Two modes:
- `paste`: validate & clean what the learner typed (fix typos, add English,
  add a short example sentence).
- `topic`: generate fresh A0/A1 vocab for the given topic.

Output shape:
[
  {
    "dutch": "goedemorgen",
    "english": "good morning",
    "example": "Goedemorgen, hoe gaat het?",
    "register": "neutral"
  },
  ...
]
"""
from __future__ import annotations

from .base import call_claude_json

SYSTEM = """You are a Dutch language expert who teaches A0/A1 beginners.

Your job is to produce small, accurate vocab sets. Constraints:
- CEFR level A0/A1 only — common, high-frequency words and phrases.
- Standard Netherlands Dutch (not Flemish/Belgian).
- Each item must have correct spelling, including capitalization and diacritics.
- Each item must include a SHORT example sentence (max 6 words) using the word.
- Mark the register: "neutral", "formal", or "informal".

Return ONLY a JSON array inside a ```json fence. No prose outside the fence.
"""

PASTE_PROMPT = """The learner pasted what they just learned. Clean it up:
- Fix any typos or spelling.
- Split into individual items (one per word/phrase).
- Add an English gloss and a short example sentence to each.
- If something is clearly not Dutch, omit it.
- Limit to at most {max_items} items.

Learner input:
---
{text}
---
"""

TOPIC_PROMPT = """Generate {max_items} useful A0/A1 Dutch vocab items for the topic: "{topic}".

Prefer the most frequent, daily-life words a beginner would actually use.
"""


def run(*, mode: str, text: str, max_items: int = 8) -> list[dict]:
    if mode == "paste":
        user = PASTE_PROMPT.format(text=text.strip(), max_items=max_items)
    elif mode == "topic":
        user = TOPIC_PROMPT.format(topic=text.strip(), max_items=max_items)
    else:
        raise ValueError(f"Unknown mode: {mode}")

    return call_claude_json(SYSTEM, user, max_tokens=2048)
