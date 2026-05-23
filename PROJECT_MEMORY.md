# Nederly — Project Memory

> Living notes about this project. Edit freely — this is your scratchpad / source of truth that you and any AI assistant can read at the start of a session.

---

## What this is

A mobile app to help me (a **dyslexic adult complete-beginner**) practice **Netherlands Dutch** right after each lesson.

**Biggest pain point:** pronunciation of Dutch vowels — `ui`, `eu`, `ij`, long vs short `a` / `o` / `e`.

---

## Approach

Agents design and build the app itself ("meta-build"). Pipeline:

```
Researcher ─→ [Gate 0] ─→ ┌─ Dutch Expert ─→ Phonetics ─┐
                          └─ Dyslexia Expert ────────────┴─→ [Gate 1] ─→ Designer ─→ [Gate 2] ─→ Builder ─→ [Final]
```

- **Manager** = Claude Code itself (reviews at every gate, escalates user decisions). Reads `docs/agents/manager_memory.md` before each run; writes a `docs/agents/reports/YYYY-MM-DD-NN-report.md` at the end.
- **Researcher** runs first — web research + reads `Lesson Notes/` to ground the pipeline in evidence
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
| 2026-05-19 | **v1 is offline-only — no API, no backend, no LLM at runtime** | Zero cost, zero key leakage, works anywhere. AI generation + per-phoneme scoring deferred to v2. |
| 2026-05-20 | Designer + Builder agents reviewed `web/index.html` | Fixed zoom lock (accessibility), added PWA manifest, Apple/Android home screen tags, pre-hydration loading state, Dutch noscript fallback |
| 2026-05-20 | Switched from Vite + React to a single `index.html` file | Removes the need for `npm install` / dev server — open directly in any browser, edit after each lesson |
| 2026-05-20 | Lesson 1 data added to app | Home, Familie, Klanken, Zinnen categories + 6 new minimal pairs from lesson sounds |
| 2026-05-20 | Sound Guide screen added to app | All 28 sounds with plain-English descriptions, ★ markers, colour coding, and two play buttons each (sound in isolation + in a word) |
| 2026-05-20 | Dutch Expert produced corrected sound guide | 3 critical errors fixed (u, g, j/tje); updated with dyslexia + phonetics expert reviews |
| 2026-05-20 | Sound guide cross-referenced against online sources | Dutch Expert, Dyslexia Expert, Phonetics Expert + web research (HearDutchHere, LearnDutchFree, Babbel, Transparent Language) all reconciled |
| 2026-05-20 | Refresh pipeline ran end-to-end (Dutch + Dyslexia + Phonetics + Designer + Builder) | All four agent docs updated; 18 changes applied to `index.html`; VERSION bumped 2 → 3 |
| 2026-05-20 | Accessibility fixes applied | `#A0A0A0` text → `#6B6B6B` (WCAG AA fix); OpenDyslexic loaded via `@font-face`; `line-height: 1.6`; `letter-spacing: 0.04em`; slow TTS rate 0.5× → 0.75× |
| 2026-05-20 | Content expansion: Numbers extended to 1–20; new Kleuren category; "Hoe gaat het?", "Ik heb dorst", and Les 1 Zinnen additions | Driven by Dutch Expert §6 + Researcher-equivalent web cross-check |
| 2026-05-20 | All Lesson 1 nouns now show with their article (de/het) | Dutch Expert §3.4 — learning nouns with articles from day one is essential |
| 2026-05-20 | Minimal pairs updated: leuk/look replaced with deur/door; huis/hijs (ui vs ij) and goed/hoed (Dutch g vs h) added | Phonetics §3 — `look` is archaic standalone; ui/ij and g contrast were missing |
| 2026-05-20 | Pipeline restructured: added Researcher agent at the front; Phonetics now runs after Dutch Expert (parallel to Dyslexia Expert) | User decision — research grounding + preserve specialist depth |
| 2026-05-20 | Manager given persistent memory (`docs/agents/manager_memory.md`) and produces a report per run (`docs/agents/reports/`) | User request — accumulating state across pipeline runs |
| 2026-05-20 | **Full new pipeline ran end-to-end** (Researcher → Dutch + Phonetics + Dyslexia → Designer → Builder). All 4 gates PASS. VERSION 3 → 4. First formal report written: `docs/agents/reports/2026-05-20-01-report.md` | First test of the restructured pipeline |
| 2026-05-20 | Researcher produced `researcher.md` with 64 cited sources covering English-L1 traps, engagement evidence, typical first lessons, dyslexia + L2 research | Grounds every downstream agent in evidence rather than training-knowledge guesses |
| 2026-05-20 | VERSION 4 content additions: Food (+thee, melk, bier, vlees, groente), Transport (+de fiets, het vliegveld, rechtdoor, Hoe kom ik bij?), Places (+de apotheek, de bibliotheek), new Numbers 21+ (Inversion) category | Dutch Expert §2 + cited curriculum survey |
| 2026-05-20 | Minimal pairs: `huis/hijs` → `uit/ijs` (real A0 standalone words on both sides); `neus/noos` removed (deur/door already covers eu/oo) | Phonetics §3 — `hijs` was verb morphology a beginner has no reason to know; `noos` was a non-word |
| 2026-05-20 | New engagement features in VERSION 4: **category progress bar** (visible progress without streaks) and **mastery card** replacing the percentage screen | Dyslexia Expert §11 — engagement without streaks, motivational gap-fill backed by [S44][S45] |
| 2026-05-20 | Sound guide cards now line-clamp descriptions to 2 lines with per-card "Show more" / "Show less" toggle | Dyslexia Expert §9 — density fix |
| 2026-05-20 | **Sound guide TTS hotfix** — every vowel `speakAs` now uses a different real Dutch word (was raw letters/digraphs the Web Speech API couldn't pronounce reliably) | User flagged the `uu` sound was wrong; root cause was isolated vowels can't be TTS'd |
| 2026-05-20 | **Pronunciation respelling pill** added to every sound card — always-visible (not hidden behind "Show more"), shows English-respelling like "say: BOOK" or "say: tight-lipped MURE" | User request — see pronunciation beside the example word |
| 2026-05-20 | **Lesson notes** feature added — new Home button, `LESSONS` array in HTML, LessonsList + LessonDetail screens. Lesson 1 (2026-05-18) curated from raw notes into bulleted sections (Sounds drilled, Words — Thuis, Words — Familie, Words — phonetics examples, Phrases, Notes) | User request — review lesson notes before practicing |
| 2026-05-20 | **Dutch Sound Reference Guide** added as second card in Lesson notes with `kind: 'reference'` (purple left-border, no "Lesson N" prefix, "Reference · updated YYYY-MM-DD" label). All 7 sections embedded from `Lesson Notes/Dutch Sound Reference Guide.md` | User request — sound reference accessible inside the app |
| 2026-05-22 | **Git repo initialised** in `Nederly/` and force-pushed to GitHub, replacing the old Expo app | Old Expo build was superseded by single `index.html`; `app/` excluded via `.gitignore` (still on disk for reference) |
| 2026-05-22 | **`nederly.html` renamed to `index.html`** | GitHub Pages serves `index.html` by default at the root URL — avoids needing the filename in the URL |
| 2026-05-22 | **GitHub Actions Pages workflow added** (`.github/workflows/deploy.yml`) | Classic branch-based Pages wasn't triggering rebuilds; Actions workflow deploys on every push to master |
| 2026-05-22 | **App live on GitHub Pages** at `https://jenuineprojects.github.io/nederly/` | VERSION 4 now publicly accessible for mobile testing |
| 2026-05-22 | **Lesson 2 added** — "Zitten in een café". New `Les 2: Café` category (31 items: drinks, food, café items, verbs, phrases). Lesson notes entry added to `LESSONS`. VERSION bumped 4 → 5. | Lesson 2 taken 2026-05-22 |
| 2026-05-22 | **Full pipeline ran end-to-end** (Researcher → Dutch Expert + Dyslexia Expert → Phonetics → Designer → Builder). All 5 gates PASS. VERSION 5 → 6. Report: `docs/agents/reports/2026-05-22-01-report.md` | User requested professional look, user-friendly layout, phonetic spelling during practice |
| 2026-05-22 | **Phonetic display on every flashcard** — respelling pill (e.g. "say: HOW-s") always visible on question side; IPA and article chip (blue `de` / green `het`) appear after tap; ★ badge on tricky sounds taps to reveal one-line articulatory hint | User request — get used to sounds while practicing |
| 2026-05-22 | **Professional visual polish** — white cards with 16px radius + shadow, white header with shadow, amber missed-state (replacing red), minimal pair colours unified to `#1A1A1A`, spacing upgraded to 8px rhythm, button styles consistent throughout | User request — professional and user-friendly look |
| 2026-05-22 | **Data model expanded** — every word object now carries 7 phonetic fields: `ipa`, `respelling`, `articulatoryHint`, `article`, `trapRank`, `soundCategory`, `audioRequired`. 181 words updated. | Required for phonetic display feature |

---

## Open questions (for me to answer when I revisit)

- [x] ~~Azure Speech pronunciation scoring?~~ **No — deferred to v2.** v1 uses on-device TTS + visual IPA only.
- [x] ~~Fully offline or backend?~~ **Fully offline for v1.**
- [x] ~~Laptop companion CLI?~~ **Not needed — no API to replace.**
- [x] ~~Tech stack confirmation: Expo (React Native)?~~ **Replaced with single `index.html`** — simpler, no build step, open directly in browser.
- [x] ~~Push `index.html` to GitHub when ready.~~ **Done 2026-05-22 — live at `https://jenuineprojects.github.io/nederly/`**
- [ ] **v2 features** (when v1 is working): per-phoneme pronunciation scoring (Azure) and/or AI-generate-from-topic (Anthropic) — decide later.

---

## File map

```
Nederly/
├── PROJECT_MEMORY.md          ← you are here
├── .github/
│   └── workflows/
│       └── deploy.yml         ← GitHub Actions: deploys Pages on push to master
├── docs/
│   └── agents/
│       ├── briefs/            ← system prompts for each agent
│       │   ├── README.md
│       │   ├── manager.md
│       │   ├── researcher.md          ← NEW: research agent (runs first)
│       │   ├── dutch_expert.md
│       │   ├── dyslexia_expert.md
│       │   ├── phonetics.md
│       │   ├── designer.md
│       │   └── builder.md
│       ├── manager_memory.md  ← cross-run ledger (decisions, VERSIONs used, follow-ups)
│       ├── reports/           ← one MD report per pipeline run
│       │   ├── README.md
│       │   ├── 2026-05-20-01-report.md  ← first formal report (VERSION 3 → 4)
│       │   └── 2026-05-22-01-report.md  ← second formal report (VERSION 5 → 6)
│       ├── researcher.md      ← (produced by Researcher, ~500 lines, 28 cited sources — updated 2026-05-22)
│       ├── dutch_expert.md    ← (produced by Dutch Expert — includes full IPA+respelling table for all ~130 words)
│       ├── dyslexia_expert.md ← (produced by Dyslexia Expert — includes phonetic chip styling + professional polish checklist)
│       ├── phonetics.md       ← (produced by Phonetics Specialist — includes 12-field card data spec)
│       └── design_spec.md     ← (produced by Designer — 50-row change table, v6 spec)
├── backend/                   ← legacy runtime-agent code — NOT used in v1 (offline-only)
│   └── agents/                ← old Python agent modules (kept as reference / possible v2 input)
├── index.html                 ← ⭐ THE APP — open directly in browser or via GitHub Pages
├── OpenDyslexic-Regular.woff2 ← REQUIRED: download from opendyslexic.org, place here (not in git)
├── Lesson Notes/
│   ├── Lesson 1.md            ← raw notes from lesson 1
│   ├── Lesson 2.md            ← raw notes from lesson 2 (2026-05-22)
│   └── Dutch Sound Reference Guide.md  ← corrected sound guide (updated 2026-05-20)
└── app/                       ← legacy Expo/Vite build (excluded from git, kept on disk for reference)
    ├── web/                   ← Vite + React web build
    │   ├── index.html         ← updated with PWA tags (2026-05-20)
    │   ├── public/manifest.json
    │   └── src/               ← React source (screens, components, lib, data)
    └── ...                    ← Expo/React Native source
```

---

## Status (as of 2026-05-22 — VERSION 6)

- ✅ Initial plan: `C:\Users\carey\.claude\plans\streamed-strolling-taco.md`
- ✅ All 7 agent briefs written: `docs/agents/briefs/`
- ✅ Two full pipeline runs completed. Reports at `docs/agents/reports/`.
- ✅ Manager memory + reports infrastructure in active use (`manager_memory.md`, `reports/`)
- ✅ **App live on GitHub Pages:** `https://jenuineprojects.github.io/nederly/` (needs push to update to VERSION 6)
- ✅ **`index.html`** — VERSION = 6
  - Screens: Home, Categories, Session, SessionComplete (mastery card), Minimal Pairs, Progress, Add Vocab, Sound Guide, Lesson notes, Lesson detail
  - 19 categories (12 general + 4 Les 1 + 1 Les 2 + Kleuren + Numbers 21+ Inversion)
  - 181 words — each carries `ipa`, `respelling`, `articulatoryHint`, `article`, `trapRank`, `soundCategory`, `audioRequired`
  - **Flashcard phonetics:** respelling pill always visible on question side; IPA + article chip appear after reveal; ★ badge on tricky sounds taps to show articulatory hint
  - **Professional visual polish:** white cards (16px radius, shadow), white header with shadow, amber missed-state, 8px spacing rhythm, consistent buttons
  - 16 minimal pairs, 28-sound guide, lesson notes (Lesson 1 + Lesson 2 + Dutch Sound Reference Guide)
  - Engagement: category progress bar, mastery card
  - Accessibility: `@font-face` for OpenDyslexic, `line-height: 1.6`, `letter-spacing: 0.04em`, `#6B6B6B` secondary text, slow TTS at `0.75×`
- ✅ All agent output docs updated and research-cited (`researcher.md`, `dutch_expert.md`, `dyslexia_expert.md`, `phonetics.md`, `design_spec.md`)
- ✅ Git repo on GitHub; Actions workflow deploys Pages on every push to master
- ⏳ **OpenDyslexic font not yet on GitHub Pages** — `OpenDyslexic-Regular.woff2` must be placed next to `index.html` and committed (or downloaded on each device). The `.otf` version is in `app/assets/fonts/opendyslexic-0.92/` but the app expects `.woff2`.
- ⬜ After each lesson: add entry to `LESSONS`, add words to `CATEGORIES` (with all 7 phonetic fields), bump VERSION (next: `'7'`)
- ⬜ Deferred for a future pipeline run: Grammar reference screen (diminutives, word order, number inversion 21–99), non-decaying mastery badges, rotating daily prompt picker, opt-in short-term goal nudge, 320px viewport overflow verification

---

## How to resume a session

1. Re-read this file
2. Open `https://jenuineprojects.github.io/nederly/` (or `index.html` locally) to check the current state of the app
3. Tell Claude Code what you want to work on — it will pick up from the `Status` section above
4. For pipeline runs, the Manager also reads `docs/agents/manager_memory.md` (run history, persistent decisions, open follow-ups) and writes a report at `docs/agents/reports/YYYY-MM-DD-NN-report.md` at the end
5. After each Dutch lesson:
   - Share your notes
   - I'll curate them into the `LESSONS` array (bulleted sections — Sounds drilled, Words, Phrases, Notes)
   - And add any new vocabulary to `CATEGORIES` — **each word needs all 7 phonetic fields**: `ipa`, `respelling`, `articulatoryHint`, `article`, `trapRank`, `soundCategory`, `audioRequired`
   - Bump VERSION so new words seed into localStorage (next: `'7'`)
6. Update the `Status` and `Decisions` sections as you go

---

## Notes / observations (free-form)

<!-- Add anything that doesn't fit above. Lesson notes, things I noticed about my learning, ideas, frustrations. -->
