"""Phonetics Specialist — annotates words with IPA and flags tricky sounds.

For each Dutch word/phrase:
- IPA transcription (Netherlands Dutch).
- Tricky sounds (subset of: ui, eu, ij, oe, ch, sch, g, long vs short vowels).
- Syllable chunks to display for the dyslexic learner.

Also proposes minimal pairs for words containing tricky sounds, drawn from
common A0/A1 vocabulary (e.g. man/maan, bos/boos, lopen/lopen vs roepen).

Output shape:
{
  "annotations": [
    {
      "dutch": "goedemorgen",
      "ipa": "ˈɣudəˌmɔrɣə(n)",
      "tricky_sounds": ["ɣ"],
      "syllables": ["goe", "de", "mor", "gen"]
    },
    ...
  ],
  "minimal_pairs": [
    {
      "dutch_a": "man", "ipa_a": "mɑn",
      "dutch_b": "maan", "ipa_b": "maːn",
      "contrast": "short a vs long a"
    }
  ]
}
"""
from __future__ import annotations

import json as _json
from .base import call_claude_json

SYSTEM = """You are a phonetics expert in Netherlands Dutch (not Flemish).

For each Dutch word given, produce:
- An IPA transcription using standard Dutch IPA conventions.
- A list of "tricky sounds" — IPA symbols that English-speaking beginners typically
  find hard. Draw from: œy (ui), øː (eu), ɛi (ei/ij), uː/u (oe), x/ɣ (g, ch),
  sx (sch), and long-vs-short vowel pairs (a/aː, o/oː, e/eː).
- Syllable chunks suitable for visual chunking of long words.

Then propose 2-4 minimal pair drills based on the tricky sounds you found.
Minimal pairs MUST use real A0/A1 Dutch words (e.g. man/maan, bos/boos, kip/kop).
Do not invent words.

Return ONLY a JSON object inside a ```json fence. No prose outside the fence.
"""

PROMPT = """Annotate these Dutch items:

{words_json}

Return JSON with shape:
{{
  "annotations": [
    {{"dutch": "...", "ipa": "...", "tricky_sounds": ["..."], "syllables": ["...","..."]}}
  ],
  "minimal_pairs": [
    {{"dutch_a": "...", "ipa_a": "...", "dutch_b": "...", "ipa_b": "...", "contrast": "..."}}
  ]
}}
"""


def run(words: list[dict]) -> dict:
    user = PROMPT.format(words_json=_json.dumps(words, ensure_ascii=False, indent=2))
    return call_claude_json(SYSTEM, user, max_tokens=2048)
