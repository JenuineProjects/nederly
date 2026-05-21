# Nederly â€” Project Memory

> Living notes about this project. Edit freely â€” this is your scratchpad / source of truth that you and any AI assistant can read at the start of a session.

---

## What this is

A mobile app to help me (a **dyslexic adult complete-beginner**) practice **Netherlands Dutch** right after each lesson.

**Biggest pain point:** pronunciation of Dutch vowels â€” `ui`, `eu`, `ij`, long vs short `a` / `o` / `e`.

---

## Approach

Agents design and build the app itself ("meta-build"). Pipeline:

```
Researcher â”€â†’ [Gate 0] â”€â†’ â”Œâ”€ Dutch Expert â”€â†’ Phonetics â”€â”
                          â””â”€ Dyslexia Expert â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â†’ [Gate 1] â”€â†’ Designer â”€â†’ [Gate 2] â”€â†’ Builder â”€â†’ [Final]
```

- **Manager** = Claude Code itself (reviews at every gate, escalates user decisions). Reads `docs/agents/manager_memory.md` before each run; writes a `docs/agents/reports/YYYY-MM-DD-NN-report.md` at the end.
- **Researcher** runs first â€” web research + reads `Lesson Notes/` to ground the pipeline in evidence
- Each agent has a system-prompt brief in `docs/agents/briefs/`
- Each agent's output is a markdown doc in `docs/agents/` (except Builder, which updates `index.html`)

---

## Decisions made so far

| Date | Decision | Why |
|---|---|---|
| 2026-05-18 | Mobile app (not web/desktop) | Practice right after class, on my phone |
| 2026-05-18 | TTS playback + record-and-score pronunciation | Per-phoneme feedback is the killer feature |
| 2026-05-18 | Multi-agent pipeline with parallel advisors | Matches prior experience; better separation of concerns |
| 2026-05-18 | Builder separated from Designer | Cheaper review; swappable Builder later |
| 2026-05-19 | Agents write the app (meta-build) instead of running at runtime | One-time design effort, not per-session runtime cost |
| 2026-05-19 | **v1 is offline-only â€” no API, no backend, no LLM at runtime** | Zero cost, zero key leakage, works anywhere. AI generation + per-phoneme scoring deferred to v2. |
| 2026-05-20 | Designer + Builder agents reviewed `web/index.html` | Fixed zoom lock (accessibility), added PWA manifest, Apple/Android home screen tags, pre-hydration loading state, Dutch noscript fallback |
| 2026-05-20 | Working locally before pushing to GitHub | No local git in `app/` â€” will init and push when HTML changes are finalised |
| 2026-05-20 | Switched from Vite + React to a single `index.html` file | Removes the need for `npm install` / dev server â€” open directly in any browser, edit after each lesson |
| 2026-05-20 | Lesson 1 data added to app | Home, Familie, Klanken, Zinnen categories + 6 new minimal pairs from lesson sounds |
| 2026-05-20 | Sound Guide screen added to app | All 28 sounds with plain-English descriptions, â˜… markers, colour coding, and two play buttons each (sound in isolation + in a word) |
| 2026-05-20 | Dutch Expert produced corrected sound guide | 3 critical errors fixed (u, g, j/tje); updated with dyslexia + phonetics expert reviews |
| 2026-05-20 | Sound guide cross-referenced against online sources | Dutch Expert, Dyslexia Expert, Phonetics Expert + web research (HearDutchHere, LearnDutchFree, Babbel, Transparent Language) all reconciled |
| 2026-05-20 | Refresh pipeline ran end-to-end (Dutch + Dyslexia + Phonetics + Designer + Builder) | All four agent docs updated; 18 changes applied to `index.html`; VERSION bumped 2 â†’ 3 |
| 2026-05-20 | Accessibility fixes applied | `#A0A0A0` text â†’ `#6B6B6B` (WCAG AA fix); OpenDyslexic loaded via `@font-face`; `line-height: 1.6`; `letter-spacing: 0.04em`; slow TTS rate 0.5Ã— â†’ 0.75Ã— |
| 2026-05-20 | Content expansion: Numbers extended to 1â€“20; new Kleuren category; "Hoe gaat het?", "Ik heb dorst", and Les 1 Zinnen additions | Driven by Dutch Expert Â§6 + Researcher-equivalent web cross-check |
| 2026-05-20 | All Lesson 1 nouns now show with their article (de/het) | Dutch Expert Â§3.4 â€” learning nouns with articles from day one is essential |
| 2026-05-20 | Minimal pairs updated: leuk/look replaced with deur/door; huis/hijs (ui vs ij) and goed/hoed (Dutch g vs h) added | Phonetics Â§3 â€” `look` is archaic standalone; ui/ij and g contrast were missing |
| 2026-05-20 | Pipeline restructured: added Researcher agent at the front; Phonetics now runs after Dutch Expert (parallel to Dyslexia Expert) | User decision â€” research grounding + preserve specialist depth |
| 2026-05-20 | Manager given persistent memory (`docs/agents/manager_memory.md`) and produces a report per run (`docs/agents/reports/`) | User request â€” accumulating state across pipeline runs |
| 2026-05-20 | **Full new pipeline ran end-to-end** (Researcher â†’ Dutch + Phonetics + Dyslexia â†’ Designer â†’ Builder). All 4 gates PASS. VERSION 3 â†’ 4. First formal report written: `docs/agents/reports/2026-05-20-01-report.md` | First test of the restructured pipeline |
| 2026-05-20 | Researcher produced `researcher.md` with 64 cited sources covering English-L1 traps, engagement evidence, typical first lessons, dyslexia + L2 research | Grounds every downstream agent in evidence rather than training-knowledge guesses |
| 2026-05-20 | VERSION 4 content additions: Food (+thee, melk, bier, vlees, groente), Transport (+de fiets, het vliegveld, rechtdoor, Hoe kom ik bij?), Places (+de apotheek, de bibliotheek), new Numbers 21+ (Inversion) category | Dutch Expert Â§2 + cited curriculum survey |
| 2026-05-20 | Minimal pairs: `huis/hijs` â†’ `uit/ijs` (real A0 standalone words on both sides); `neus/noos` removed (deur/door already covers eu/oo) | Phonetics Â§3 â€” `hijs` was verb morphology a beginner has no reason to know; `noos` was a non-word |
| 2026-05-20 | New engagement features in VERSION 4: **category progress bar** (visible progress without streaks) and **mastery card** replacing the percentage screen | Dyslexia Expert Â§11 â€” engagement without streaks, motivational gap-fill backed by [S44][S45] |
| 2026-05-20 | Sound guide cards now line-clamp descriptions to 2 lines with per-card "Show more" / "Show less" toggle | Dyslexia Expert Â§9 â€” density fix |
| 2026-05-20 | **Sound guide TTS hotfix** â€” every vowel `speakAs` now uses a different real Dutch word (was raw letters/digraphs the Web Speech API couldn't pronounce reliably) | User flagged the `uu` sound was wrong; root cause was isolated vowels can't be TTS'd |
| 2026-05-20 | **Pronunciation respelling pill** added to every sound card â€” always-visible (not hidden behind "Show more"), shows English-respelling like "say: BOOK" or "say: tight-lipped MURE" | User request â€” see pronunciation beside the example word |
| 2026-05-20 | **Lesson notes** feature added â€” new Home button, `LESSONS` array in HTML, LessonsList + LessonDetail screens. Lesson 1 (2026-05-18) curated from raw notes into bulleted sections (Sounds drilled, Words â€” Thuis, Words â€” Familie, Words â€” phonetics examples, Phrases, Notes) | User request â€” review lesson notes before practicing |
| 2026-05-20 | **Dutch Sound Reference Guide** added as second card in Lesson notes with `kind: 'reference'` (purple left-border, no "Lesson N" prefix, "Reference Â· updated YYYY-MM-DD" label). All 7 sections embedded from `Lesson Notes/Dutch Sound Reference Guide.md` | User request â€” sound reference accessible inside the app |

---

## Open questions (for me to answer when I revisit)

- [x] ~~Azure Speech pronunciation scoring?~~ **No â€” deferred to v2.** v1 uses on-device TTS + visual IPA only.
- [x] ~~Fully offline or backend?~~ **Fully offline for v1.**
- [x] ~~Laptop companion CLI?~~ **Not needed â€” no API to replace.**
- [x] ~~Tech stack confirmation: Expo (React Native)?~~ **Replaced with single `index.html`** â€” simpler, no build step, open directly in browser.
- [ ] **v2 features** (when v1 is working): per-phoneme pronunciation scoring (Azure) and/or AI-generate-from-topic (Anthropic) â€” decide later.
- [ ] Push `index.html` to GitHub when ready.

---

## File map

```
Nederly/
â”œâ”€â”€ PROJECT_MEMORY.md          â† you are here
â”œâ”€â”€ docs/
â”‚   â””â”€â”€ agents/
â”‚       â”œâ”€â”€ briefs/            â† system prompts for each agent
â”‚       â”‚   â”œâ”€â”€ README.md
â”‚       â”‚   â”œâ”€â”€ manager.md
â”‚       â”‚   â”œâ”€â”€ researcher.md          â† NEW: research agent (runs first)
â”‚       â”‚   â”œâ”€â”€ dutch_expert.md
â”‚       â”‚   â”œâ”€â”€ dyslexia_expert.md
â”‚       â”‚   â”œâ”€â”€ phonetics.md
â”‚       â”‚   â”œâ”€â”€ designer.md
â”‚       â”‚   â””â”€â”€ builder.md
â”‚       â”œâ”€â”€ manager_memory.md  â† cross-run ledger (decisions, VERSIONs used, follow-ups)
â”‚       â”œâ”€â”€ reports/           â† one MD report per pipeline run
â”‚       â”‚   â”œâ”€â”€ README.md
â”‚       â”‚   â””â”€â”€ 2026-05-20-01-report.md  â† first formal report (VERSION 3 â†’ 4)
â”‚       â”œâ”€â”€ researcher.md      â† (produced by Researcher, ~280 lines, 64 cited sources)
â”‚       â”œâ”€â”€ dutch_expert.md    â† (produced by Dutch Expert, ~470 lines)
â”‚       â”œâ”€â”€ dyslexia_expert.md â† (produced by Dyslexia Expert, ~530 lines)
â”‚       â”œâ”€â”€ phonetics.md       â† (produced by Phonetics Specialist, ~440 lines)
â”‚       â””â”€â”€ design_spec.md     â† (produced by Designer, ~620 lines, v4 spec)
â”œâ”€â”€ backend/                   â† legacy runtime-agent code â€” NOT used in v1 (offline-only)
â”‚   â””â”€â”€ agents/                â† old Python agent modules (kept as reference / possible v2 input)
â”œâ”€â”€ index.html               â† â­ THE APP â€” open this directly in a browser, no build needed
â”œâ”€â”€ OpenDyslexic-Regular.woff2 â† REQUIRED: download from opendyslexic.org, place here
â”œâ”€â”€ Lesson Notes/
â”‚   â”œâ”€â”€ Lesson 1.md            â† raw notes from lesson 1
â”‚   â””â”€â”€ Dutch Sound Reference Guide.md  â† corrected sound guide (updated 2026-05-20)
â””â”€â”€ app/                       â† legacy Expo/Vite build (kept for reference, not the active version)
    â”œâ”€â”€ web/                   â† Vite + React web build
    â”‚   â”œâ”€â”€ index.html         â† updated with PWA tags (2026-05-20)
    â”‚   â”œâ”€â”€ public/manifest.json
    â”‚   â””â”€â”€ src/               â† React source (screens, components, lib, data)
    â””â”€â”€ ...                    â† Expo/React Native source
```

---

## Status (as of 2026-05-20 â€” VERSION 4 shipped + Lesson Notes feature)

- âœ… Initial plan: `C:\Users\carey\.claude\plans\streamed-strolling-taco.md`
- âœ… All 7 agent briefs written: `docs/agents/briefs/`
- âœ… Full pipeline ran end-to-end with Researcher in front: Researcher â†’ Dutch Expert + Phonetics + Dyslexia Expert â†’ Designer â†’ Builder. All 4 gates PASS. First formal report at `docs/agents/reports/2026-05-20-01-report.md`.
- âœ… Manager memory + reports infrastructure in active use (`manager_memory.md`, `reports/`)
- âœ… App on GitHub: https://github.com/JenuineProjects/nederly (older version; latest `index.html` not yet pushed)
- âœ… **`index.html`** â€” VERSION = 4
  - Screens: Home, Categories, Session, SessionComplete (mastery card), Minimal Pairs, Progress, Add Vocab, Sound Guide, **Lesson notes (new)**, **Lesson detail (new)**
  - 18 categories (12 general + 4 Les 1 + Kleuren + Numbers 21+ Inversion). Numbers extended through 20 + inversion examples (eenentwintig etc.)
  - Food/Transport/Places expanded (thee, melk, bier, vlees, groente / de fiets, het vliegveld, rechtdoor, Hoe kom ik bij? / de apotheek, de bibliotheek)
  - All Lesson 1 nouns show with their article (de/het)
  - 16 minimal pairs (replaced huis/hijs â†’ uit/ijs; removed neus/noos as duplicate)
  - 28-sound guide with: line-clamp+toggle on long descriptions, fixed TTS speakAs (different Dutch word per sound), always-visible "say: ..." English-respelling pills
  - **Lesson notes section** with 2 cards: Lesson 1 â€” Phonetics + Thuis + Familie (2026-05-18, structured bullet lists) and Dutch Sound Reference Guide (purple-bordered reference card with all 28 sounds + top-5 + common mistakes)
  - Engagement: category progress bar, mastery card replacing the percentage screen, sound-card respelling pills
  - Accessibility: `@font-face` for OpenDyslexic, `line-height: 1.6`, `letter-spacing: 0.04em`, helper text `#6B6B6B`, slow rate `0.75Ã—`
- âœ… All four agent output docs are research-cited and current (researcher.md is new)
- â³ **OpenDyslexic font file not yet downloaded** â€” drop `OpenDyslexic-Regular.woff2` next to `index.html` from https://opendyslexic.org. Bold face also pending.
- â³ **Local only** â€” VERSION 4 `index.html` not yet pushed to GitHub
- â¬œ After each lesson: add a new entry to `LESSONS` (sections with items) AND add words to `CATEGORIES`; bump VERSION number for CATEGORIES changes (next: `'5'`)
- â¬œ Push to GitHub when ready
- â¬œ Deferred for next pipeline run (v5 candidates): Grammar reference screen (diminutives, subordinate-clause word order, full number inversion 21â€“99), non-decaying mastery badges, rotating daily prompt picker, opt-in short-term goal nudge, 320px viewport overflow verification

---

## How to resume a session

1. Re-read this file
2. Open `index.html` directly in your browser to check the current state of the app
3. Tell Claude Code what you want to work on â€” it will pick up from the `Status` section above
4. For pipeline runs, the Manager also reads `docs/agents/manager_memory.md` (run history, persistent decisions, open follow-ups) and writes a report at `docs/agents/reports/YYYY-MM-DD-NN-report.md` at the end
5. After each Dutch lesson:
   - Share your notes
   - I'll curate them into the `LESSONS` array (bulleted sections â€” Sounds drilled, Words, Phrases, Notes)
   - And add any new vocabulary to `CATEGORIES` (bumping VERSION so the new words seed into localStorage)
6. Update the `Status` and `Decisions` sections as you go

---

## Notes / observations (free-form)

<!-- Add anything that doesn't fit above. Lesson notes, things I noticed about my learning, ideas, frustrations. -->
