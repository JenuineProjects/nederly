# Manager Memory

> Persistent memory for the Manager (Claude Code orchestrating the Nederly pipeline). Read this at the start of every pipeline run. Append to it at the end.

---

## Run index

| Date | Report | Outcome (1 line) |
|------|--------|------------------|
| 2026-05-20 | [2026-05-20-01-report.md](reports/2026-05-20-01-report.md) | First run with new pipeline. All gates PASS. VERSION 3 → 4. Researcher added, Food/Transport/Places expanded, Numbers 21+ category, uit/ijs replacing huis/hijs, neus/noos removed, category progress bar, mastery card, sound guide line-clamp+toggle. |
| 2026-05-20 | _(hotfix, no formal report)_ | Sound guide TTS fix: every vowel `speakAs` now uses a different real Dutch word (was raw letters/digraphs the TTS couldn't pronounce). Added `exPronounce` field with English respellings shown in always-visible pill on every sound card. |
| 2026-05-20 | _(feature add, no formal report)_ | New **Lesson notes** section: `LESSONS` array embedded in HTML, new Home button, LessonsList + LessonDetail screens. Lesson 1 curated from `Lesson Notes/Lesson 1.md` into structured sections. Lesson 1 date corrected to 2026-05-18; sections refactored to bulleted lists. No VERSION bump (LESSONS is not stored in localStorage). |
| 2026-05-20 | _(feature add, no formal report)_ | **Dutch Sound Reference Guide** added as a second card in Lesson notes. Card distinguished by `kind: 'reference'` (purple left-border, "Reference · updated YYYY-MM-DD" label, no "Lesson N" prefix). All 7 sections (single/long/diphthong/consonant/complex vowels, top 5, common mistakes, usage tip) from `Lesson Notes/Dutch Sound Reference Guide.md` embedded. |
| 2026-05-22 | [2026-05-22-01-report.md](reports/2026-05-22-01-report.md) | Professional polish + phonetic display on flashcards. VERSION 5 → 6. 181 words updated with IPA/respelling. 50 CSS/JS changes applied. All 5 gates PASS. |

---

## Persistent decisions — do not re-litigate

| Decision | Source | Date |
|----------|--------|------|
| v1 is offline-only — no API, no backend, no LLM at runtime | User, 2026-05-19 | 2026-05-19 |
| App is a single `nederly.html` file (vanilla JS) — not Expo/React Native | User, 2026-05-20 | 2026-05-20 |
| TTS = Web Speech API (`window.speechSynthesis`, `lang: 'nl-NL'`) | Pipeline, 2026-05-20 | 2026-05-20 |
| Storage = `localStorage`, reseed-on-VERSION-bump pattern | Pipeline, 2026-05-20 | 2026-05-20 |
| Pronunciation scoring deferred to v2 | User, 2026-05-19 | 2026-05-19 |
| AI generation deferred to v2 | User, 2026-05-19 | 2026-05-19 |
| Streaks / lives / timers are explicitly prohibited | Dyslexia Expert | 2026-05-20 |
| OpenDyslexic font loaded via `@font-face` from local WOFF2 | Pipeline, 2026-05-20 | 2026-05-20 |
| Helper/secondary text colour is `#6B6B6B` (not `#A0A0A0` — fails WCAG AA) | Pipeline, 2026-05-20 | 2026-05-20 |
| Slow playback rate = `0.75` (not `0.5` — distorts vowels) | Pipeline, 2026-05-20 | 2026-05-20 |
| Every word object carries 7 phonetic fields: article, respelling, audioRequired, articulatoryHint, ipa, trapRank, soundCategory | Builder, 2026-05-22 | 2026-05-22 |

---

## VERSION numbers used (in `initStorage()`)

| VERSION | Pipeline run | Notes |
|---------|--------------|-------|
| `'1'` | Initial build (pre-pipeline) | First seed |
| `'2'` | 2026-05-20 lesson 1 addition | Added Les 1 categories |
| `'3'` | 2026-05-20 refresh pipeline | Articles on nouns, Numbers 1–20, Kleuren, new minimal pairs, dyslexia fixes |
| `'4'` | 2026-05-20-01 (first full new-pipeline run) | Food/Transport/Places expansions, Numbers 21+ category, uit/ijs swap, neus/noos removed, progress bar, mastery card, sound guide toggle |
| `'6'` | 2026-05-22-01 | Professional polish + phonetic display. 181 words updated. |

**Next available: `'7'`**

---

## Recurring patterns — lessons across runs

- **Non-words slip past Dutch Expert and Designer without Phonetic re-review.** `noos` and `hijs` both survived two pipeline runs before Phonetics + Researcher flagged them together. Future Gate 1 must explicitly verify every minimal pair word is a real A0 standalone Dutch word. (2026-05-20-01)
- **Researcher saves agent runtime.** Downstream agents stop guessing at evidence. Trap rankings, streak bans, engagement choices all became cite-backed. Keep Researcher in every run. (2026-05-20-01)
- **Citations make Gate review trivial.** When every Designer decision points to an upstream section, Gate 2 takes seconds. Reinforce "cite or it didn't happen" in spawn prompts. (2026-05-20-01)
- **No-streaks needs a positive counterpart.** Saying "no streaks" without filling the motivational gap reads as deprivation. Pair every anti-pattern with at least one engagement feature recommendation. (2026-05-20-01)
- **IPA/respelling must be added at data-entry time.** Retrofitting 181 words took the full Builder budget. Future lesson vocab should include these fields when first added. (2026-05-22-01)

---

## Open follow-ups carried forward

| Item | Source run | Status |
|------|-----------|--------|
| Push `nederly.html` to GitHub | 2026-05-20 | ~~Resolved — done 2026-05-22 in a hotfix~~ |
| Download `OpenDyslexic-Regular.woff2` into the app folder | 2026-05-20 refresh | **Still pending — surface to user each run** |
| Download `OpenDyslexic-Bold.woff2` for heading weight | 2026-05-20-01 | Pending — currently only Regular face loaded |
| Lesson 2 vocabulary | Future | ~~Resolved — added 2026-05-22 before this pipeline run~~ |
| Grammar reference screen (diminutives, subordinate-clause word order, full number inversion 21–99) | 2026-05-20-01 (deferred) | Designer chose Option B (defer); candidate for v5 |
| Non-decaying mastery badges | 2026-05-20-01 (deferred) | Dyslexia Expert §11.3 — engagement feature for future version |
| Rotating daily prompt picker | 2026-05-20-01 (deferred) | Dyslexia Expert §11.4 |
| Opt-in short-term goal nudge | 2026-05-20-01 (deferred) | Dyslexia Expert §11.5 |
| Verify 320px viewport overflow | 2026-05-20-01 | Not verified this run; needs a browser check |
| IPA/respelling for any new lesson vocab | 2026-05-22-01 | Add these fields at the time new words are added to CATEGORIES |

**Resolved (do not carry forward):**
- ~~Food & Drink expansion~~ ✅ shipped in VERSION 4
- ~~Transport expansion~~ ✅ shipped in VERSION 4
