# Design Spec — Nederly VERSION 4

> Buildable specification for the v3 → v4 update of `nederly.html`.
> The Builder implements this verbatim — no design decisions remain open.
> All decisions cite an upstream document (Researcher, Dutch Expert, Dyslexia Expert, Phonetics).

---

## 0. Scope of this version (v4)

Six concrete change groups, in implementation order:

1. **Content** — expand Food & Drink, Transport, Places; add Numbers 21+ category. (Per Dutch Expert §2.5, §2.7, §2.8, §8.)
2. **Minimal pairs** — replace `huis/hijs` with `uit/ijs`; remove `neus/noos`. (Per Phonetics §3.2, §3.3.)
3. **Engagement — category progress bar** on the Session screen. (Per Dyslexia Expert §11.1.)
4. **Engagement — mastery card** replaces the percentage-heavy SessionComplete screen. (Per Dyslexia Expert §11.2.)
5. **Sound guide card density** — `-webkit-line-clamp: 2` on description + "Show more" toggle. (Per Dyslexia Expert §9 / §10 "still required" table.)
6. **VERSION bump** — `'3'` → `'4'` in `initStorage` to trigger re-seed. (Per architecture rule in brief §1.)

Items deferred to a future version are listed in §10.

---

## 1. Architecture decision (unchanged from v3)

Per Designer Brief §1 — PREDETERMINED:

- Fully offline. No API, no backend, no LLM at runtime.
- **TTS:** Web Speech API — `window.speechSynthesis`, `lang: 'nl-NL'`, `rate: 1.0` normal / `0.75` slow.
- **IPA:** static text in `SOUNDS`/inline cues (no IPA in CATEGORIES — keep as-is).
- **Vocab generation:** none. Hardcoded `CATEGORIES` + `MINIMAL_PAIRS` arrays + user "Paste your vocab" path.
- **Storage:** `localStorage`. `VERSION` constant in `initStorage()` triggers re-seed when bumped.
- **No build step, no npm, no framework, no third-party libraries.**

Confirmed unchanged for v4.

---

## 2. Tech stack (unchanged from v3)

| Item | Value |
|------|-------|
| File | Single `nederly.html` |
| Language | Vanilla HTML5 + CSS3 + JS (ES2020) |
| Storage | `localStorage` |
| Audio | Web Speech API (`window.speechSynthesis`, `lang: 'nl-NL'`) |
| Font | OpenDyslexic (WOFF2, local) + `system-ui` fallback |
| Target | Mobile browsers (Chrome Android, Safari iOS), 320px viewport minimum |

---

## 3. Data model

### 3.1 In-file constants (hardcoded, re-seeded on version bump)

| Constant | Shape | Purpose |
|----------|-------|---------|
| `CATEGORIES` | `[{ name: string, words: [{ dutch, english }] }]` | Seed of practice categories. v4 edits — see §8. |
| `MINIMAL_PAIRS` | `[{ word_a, word_b, english_a, english_b, contrast, tricky_sound }]` | Seed of pair-discrimination drills. v4 edits — see §8. |
| `SOUNDS` | `[{ section, sound, speakAs, star, desc, example, exEnglish }]` | Sound-guide cards. **No schema change in v4.** |
| `COLOR_PATTERNS` | `[{ p, c }]` | Letter-pattern colour highlights. Unchanged. |
| `HINTS` | `{ sound: hintText }` | Per-sound pronunciation hints on Session. Unchanged. |

### 3.2 localStorage keys (unchanged)

| Key | Shape | Notes |
|-----|-------|-------|
| `nederly_words` | `[{ id, dutch, english, categoryId, sessionId, createdAt }]` | Re-seeded on version bump |
| `nederly_categories` | `[{ id, name }]` | Re-seeded on version bump |
| `nederly_minimal_pairs` | `[{ id, ...MINIMAL_PAIRS[i] }]` | Re-seeded on version bump |
| `nederly_sessions` | `[{ id, createdAt, wordCount, exerciseType }]` | Cleared on version bump |
| `nederly_attempts` | `[{ id, sessionId, wordId, exerciseType, outcome, createdAt }]` | Cleared on version bump |
| `nederly_initialized` | string — current VERSION | Triggers re-seed when ≠ `'4'` |

### 3.3 Derived values used by new components

| Value | Derivation | Used by |
|-------|------------|---------|
| `categoryWordCount` | `S.sessionWords.length` (already in state) | Category progress bar (§5.1) |
| `currentPosition` | `S.sessionIndex + 1` when revealed/answered, else `S.sessionIndex` | Category progress bar label |
| `wordsThisSession` | `out.correct + out.incorrect + out.skipped` | Mastery card body (§5.2) |
| `sessionCategoryName` | New state field `S.sessionCategoryName: string \| null` — set in `select-category` handler, cleared in paste flow | Mastery card body line 2 |

**No persistent schema change.** All new values are runtime-derived.

---

## 4. Screen list with flow

Eight screens. **Changes vs v3 are bolded.** All other screens unchanged.

### 4.1 Home (unchanged)
- Purpose: launch into one of four practice modes.
- Entry: app open / Back from any screen.
- Exit: AddVocab, Categories, MinimalPairs, Sounds, Progress.

### 4.2 AddVocab (unchanged)
- Purpose: paste 1–20 lines of vocab → start a session.
- Entry: Home.
- Exit: Session.

### 4.3 Categories (unchanged structure — content expanded; see §8)
- Purpose: pick a curated category to drill.
- Entry: Home.
- Exit: Session.

### 4.4 **Session (modified — adds progress bar)**
- Purpose: flashcard practice loop over `S.sessionWords`.
- Entry: AddVocab, Categories.
- Exit: SessionComplete (on last advance).
- **Change vs v3:** Add a thin progress bar between dots-row and card, showing position in the category. Dots row is **kept** (it shows micro-position; the bar shows macro % completed). See §5.1.

```
+----------------------------------+
| ← Practice                       |  <- header
+----------------------------------+
| ● ● ◐ ○ ○ ○ ○ ○ ○ ○             |  <- dots (kept)
| [██████░░░░░░░░░░░░░]  3 of 10  |  <- NEW progress bar + label
|                                  |
| +----------------------------+   |
| |        Dutch word          |   |
| |     [▶ Play]  [▶ Slow]     |   |
| |   English (when revealed)  |   |
| +----------------------------+   |
|                                  |
| | hint line (when revealed)      |
|                                  |
| [ ✗ Missed it ]  [ ✓ Got it ]    |
+----------------------------------+
```

### 4.5 **SessionComplete → MasteryCard (renamed + redesigned)**
- Purpose: brief reflection card. Replaces the percentage-heavy v3 screen.
- Entry: Session (last advance).
- Exit: Home (single CTA).
- **Change vs v3:** Removes the giant `64px` percentage. Adds reflection lines. See §5.2.

```
+----------------------------------+
|                                  |
|      Nice session.               |  <- heading 20px bold
|                                  |
|   You practiced 8 words today.   |  <- 18px
|                                  |
|   Category: Food & Drink         |  <- 18px (or "Pasted vocab")
|                                  |
|   ✓ 6 got it                     |  <- kept from v3, smaller
|   ✗ 2 missed                     |
|                                  |
|   [    Back home    ]            |  <- 64px CTA
+----------------------------------+
```

> No percentage. No "come back tomorrow". No streak. (Per Dyslexia Expert §11.2 "what is *not* shown".)

### 4.6 MinimalPairs (unchanged structure — pair list edited; see §8)
- Purpose: discriminate `word_a` vs `word_b` by listening.
- Entry: Home.
- Exit: Back to Home.

### 4.7 **Sounds (modified — card density fix)**
- Purpose: browse Dutch sounds.
- Entry: Home.
- Exit: Back to Home.
- **Change vs v3:** `.sound-desc` gets `-webkit-line-clamp: 2`. A "Show more" / "Show less" toggle is added per card. See §5.3.

```
+----------------------------------+
| ★ = no English equivalent...     |
|                                  |
| SINGLE VOWELS                    |
| +----------------------------+   |
| | a                          |   |
| | Like "a" in "cat" — short, |   |  <- clamped to 2 lines
| | tongue forward             |   |
| | Show more                  |   |  <- NEW toggle (only if truncated)
| | [▶ Sound] [▶ kat]   cat    |   |
| +----------------------------+   |
```

### 4.8 Progress (unchanged)
- Purpose: stats + recent sessions list.
- Entry: Home.
- Exit: Back to Home.

---

## 5. Component contracts (new + modified)

### 5.1 ProgressBar (new)

Used on the Session screen, between dots row and card.

| Prop | Type | Required | Notes |
|------|------|----------|-------|
| `total` | number | yes | `S.sessionWords.length` |
| `current` | number | yes | `S.sessionIndex` (0-based; bar fill = `current / total` until last advance, then full) |

**Visual states:** single state — no hover, no tap.

**Tokens consumed** (per Dyslexia Expert §11.1):
- Track background: `#E8DFC4`
- Fill: `#2E6DA4` (Accent Blue)
- Height: `6px`
- Border radius: `3px`
- Width transition: `300ms ease-out`
- Label: `16px`, colour `#6B6B6B`, left-aligned, sentence case, format `"{current+1} of {total}"` while in-progress, `"{total} of {total}"` on the complete state.
- Layout: bar takes remaining width; label is to the right with `8px` gap. Container `margin-top: 0; margin-bottom: 8px`.

### 5.2 MasteryCard (new — replaces v3 SessionComplete content)

| Prop | Type | Required | Notes |
|------|------|----------|-------|
| `wordsPracticed` | number | yes | `out.correct + out.incorrect + out.skipped` |
| `categoryName` | string \| null | yes | `S.sessionCategoryName`. If null → render "Pasted vocab" |
| `correct` | number | yes | from `getSessionOutcomes()` |
| `incorrect` | number | yes | from `getSessionOutcomes()` |
| `skipped` | number | yes | from `getSessionOutcomes()` |

**Visual states:** single state.

**Tokens consumed** (per Dyslexia Expert §11.2):
- Heading "Nice session.": `20px` bold, colour `#1A1A1A`, sentence case, centred.
- Body line 1 "You practiced {N} words today.": `18px`, `#1A1A1A`.
- Body line 2 "Category: {name}" or "Pasted vocab": `18px`, `#1A1A1A`.
- Outcome rows (kept from v3, restyled smaller): `18px`, ticks/crosses keep `#3A7D44` / `#D94F3D`.
- CTA "Back home": uses existing `.home-btn` (already 64px, `#2E6DA4`, white text).
- **No `.pct` element. No percentage. No "%".**
- Section gap: `lg` (24px) between heading block and outcomes; `md` (16px) within blocks.

**Hex codes summary** — all already present in v3 tokens; no new colours needed beyond reusing existing.

### 5.3 SoundCard (modified — line-clamp + toggle)

| Prop | Type | Required | Notes |
|------|------|----------|-------|
| `sound` | string | yes | unchanged |
| `desc` | string | yes | wrapped in `.sound-desc` |
| `star` | boolean | yes | unchanged |
| `expanded` | boolean | yes | NEW. Default `false`. Per-card state. |
| ...other fields | — | — | unchanged |

**Behaviour:**
- When `expanded === false`: `.sound-desc` is line-clamped to 2 lines via CSS.
- A "Show more" button appears **only when** the text would overflow at 2 lines. Implementation: render the button unconditionally as a span styled like a link; on render, after insertion, hide it if `element.scrollHeight <= element.clientHeight` (a small `requestAnimationFrame` pass).
- Tap "Show more" → toggle `S.soundExpanded[soundKey] = true` → re-render → label changes to "Show less" → tap again collapses.

**State storage:** `S.soundExpanded: { [section + ':' + sound]: boolean }`. Initialised to `{}`. Does **not** persist across sessions (intentionally; v4 keeps it simple).

**Tokens:**
- Toggle text: `16px`, colour `#2E6DA4`, no underline (per Dyslexia Expert §11.4 conventions for inline action), tap target `min-height: 36px`, left-aligned, sentence case.
- Description line height: `26px` (already in v3) — preserved.

### 5.4 ProgressDots (unchanged)

Kept from v3 — micro-position indicator. Visual is preserved; the new progress bar lives beside it.

---

## 6. Exercise type definitions (unchanged)

`flashcard`, `listen_and_repeat` (treated identically to flashcard for now — the radio selection is recorded but currently both render the same Session UI; that is **not** changing in v4), and `minimal_pair_discrimination`. See `nederly.html` v3 §sessionHtml + §minimalPairsHtml. No exercise-type contract changes for v4.

---

## 7. Design tokens

All v3 tokens are preserved. Additions are **bolded**.

### 7.1 Colours

| Token | Hex | Use | Source |
|-------|-----|-----|--------|
| `bg` | `#FAF3E0` | Page background | Dyslexia §2 |
| `text` | `#1A1A1A` | Primary text | Dyslexia §2 |
| `helper` | `#6B6B6B` | IPA, helper, labels | Dyslexia §2 / §10 |
| `accent.blue` | `#2E6DA4` | Long vowels, links, primary CTA, **progress fill** | Dyslexia §2, §11.1 |
| `accent.orange` | `#E07B39` | Diphthongs | Dyslexia §2 |
| `accent.red` | `#D94F3D` | Clusters, errors | Dyslexia §2 |
| `accent.green` | `#3A7D44` | Success | Dyslexia §2 |
| `accent.purple` | `#6B4FA0` | Hints, slow-play | Dyslexia §2 |
| `border` | `#E0D8C8` | Card borders, dividers | v3 in-place |
| **`progressTrack`** | **`#E8DFC4`** | **Progress bar track** | **Dyslexia §11.1** |

### 7.2 Typography

| Token | Value | Source |
|-------|-------|--------|
| Body size | 18px | Dyslexia §1 |
| Vocab word | 26px | Dyslexia §1 |
| IPA / helper | 16px | Dyslexia §1 |
| Title | 20px | Dyslexia §1 |
| Line height | 1.6 | Dyslexia §1 |
| Letter spacing | 0.04em | Dyslexia §1 |
| Font family | `'OpenDyslexic', system-ui, sans-serif` | Dyslexia §1 |
| Casing | Sentence case only | Dyslexia §1 |

### 7.3 Spacing

| Token | Value |
|-------|-------|
| xs | 4px |
| sm | 8px |
| md | 16px |
| lg | 24px |
| xl | 40px |

### 7.4 Touch targets

| Element | Min |
|---------|-----|
| Tappable | 48×48 |
| Primary action | 64 height |
| Play button | 48 height |

---

## 8. Content changes — exact before / after

### 8.1 CATEGORIES — `Food & Drink`

**Before** (lines ~296–305 of v3):
```js
{
  name: 'Food & Drink',
  words: [
    { dutch: 'water', english: 'water' },
    { dutch: 'koffie', english: 'coffee' },
    { dutch: 'brood', english: 'bread' },
    { dutch: 'kaas', english: 'cheese' },
    { dutch: 'appel', english: 'apple' },
  ],
},
```

**After** (per Dutch Expert §2.5, §8 item 1):
```js
{
  name: 'Food & Drink',
  words: [
    { dutch: 'water',   english: 'water' },
    { dutch: 'koffie',  english: 'coffee' },
    { dutch: 'thee',    english: 'tea' },
    { dutch: 'melk',    english: 'milk' },
    { dutch: 'bier',    english: 'beer' },
    { dutch: 'brood',   english: 'bread' },
    { dutch: 'kaas',    english: 'cheese' },
    { dutch: 'appel',   english: 'apple' },
    { dutch: 'vlees',   english: 'meat' },
    { dutch: 'groente', english: 'vegetables' },
  ],
},
```

### 8.2 CATEGORIES — `Transport & Directions`

**Before:**
```js
{
  name: 'Transport & Directions',
  words: [
    { dutch: 'de trein', english: 'the train' },
    { dutch: 'de bus', english: 'the bus' },
    { dutch: 'het station', english: 'the station' },
    { dutch: 'links', english: 'left' },
    { dutch: 'rechts', english: 'right' },
  ],
},
```

**After** (per Dutch Expert §2.7, §8 item 2):
```js
{
  name: 'Transport & Directions',
  words: [
    { dutch: 'de trein',         english: 'the train' },
    { dutch: 'de bus',           english: 'the bus' },
    { dutch: 'de fiets',         english: 'the bicycle' },
    { dutch: 'het station',      english: 'the station' },
    { dutch: 'het vliegveld',    english: 'the airport' },
    { dutch: 'links',            english: 'left' },
    { dutch: 'rechts',           english: 'right' },
    { dutch: 'rechtdoor',        english: 'straight ahead' },
    { dutch: 'Hoe kom ik bij?',  english: 'How do I get to?' },
  ],
},
```

> Note: the question phrase `'Hoe kom ik bij?'` ends with `?` — TTS handles it fine. The original ellipsis form (*Hoe kom ik bij...?*) is shortened because the `…` rendering through Web Speech is noisy.

### 8.3 CATEGORIES — `Places`

**Before:**
```js
{
  name: 'Places',
  words: [
    { dutch: 'de supermarkt', english: 'the supermarket' },
    { dutch: 'het ziekenhuis', english: 'the hospital' },
    { dutch: 'de school', english: 'the school' },
    { dutch: 'het centrum', english: 'the city centre' },
    { dutch: 'de straat', english: 'the street' },
  ],
},
```

**After** (per Dutch Expert §2.8, §8 item 3):
```js
{
  name: 'Places',
  words: [
    { dutch: 'de supermarkt',  english: 'the supermarket' },
    { dutch: 'het ziekenhuis', english: 'the hospital' },
    { dutch: 'de apotheek',    english: 'the pharmacy' },
    { dutch: 'de bibliotheek', english: 'the library' },
    { dutch: 'de school',      english: 'the school' },
    { dutch: 'het centrum',    english: 'the city centre' },
    { dutch: 'de straat',      english: 'the street' },
  ],
},
```

### 8.4 CATEGORIES — Numbers (new category, not append)

**Designer decision: NEW category called `Numbers 21+ (Inversion)`.** Justification: the inversion rule is a discrete pedagogical concept (Dutch Expert §3.13, Trap 4 in §4 of Dutch Expert), and bundling it into `Numbers 1–20` (already 20 items) would push that category to 25 items — exceeding the "5–8 items per session" guidance (Dutch Expert §6). A separate small category lets the learner drill the inversion rule in isolation, which is precisely how the Dutch Expert frames it in §8 item 5 ("This teaches the inversion rule from §3.13 with the smallest viable set").

**Insert immediately after the existing `Numbers 1–20` block:**

```js
{
  name: 'Numbers 21+ (Inversion)',
  words: [
    { dutch: 'eenentwintig',  english: '21 (one-and-twenty)' },
    { dutch: 'tweeëntwintig', english: '22 (two-and-twenty)' },
    { dutch: 'vijfendertig',  english: '35 (five-and-thirty)' },
  ],
},
```

> Per brief: "a small set of inversion examples". Three items is the minimum that demonstrates the pattern across two decades and across the `ë`-diaeresis form (per Phonetics §11.1). The English gloss includes the literal "X-and-Y" form so the learner sees the inversion explicitly.

### 8.5 MINIMAL_PAIRS — replace `huis/hijs` with `uit/ijs`

**Before** (line ~482 of v3):
```js
{ word_a: 'huis', word_b: 'hijs', english_a: 'house', english_b: 'he hoists', contrast: 'ui /œy/ vs ij /ɛi/', tricky_sound: 'ui vs ij' },
```

**After** (per Phonetics §3.1, §3.2):
```js
{ word_a: 'uit', word_b: 'ijs', english_a: 'out', english_b: 'ice', contrast: 'ui /œy/ vs ij /ɛi/', tricky_sound: 'ui vs ij' },
```

### 8.6 MINIMAL_PAIRS — remove `neus/noos`

**Before** (line ~476 of v3):
```js
{ word_a: 'neus',  word_b: 'noos',  english_a: 'nose',       english_b: '(non-word)',        contrast: 'eu vs oo',            tricky_sound: 'eu vs oo' },
```

**After:** **delete this line entirely.** Per Phonetics §3.3: `deur/door` (still in the array) already covers the eu/oo contrast with two real words; `noos` is a non-word and must not be presented to the learner.

### 8.7 CATEGORIES + MINIMAL_PAIRS — no other content edits in v4

Specifically **NOT in scope this version** (carried forward to v5):
- Adding `Hoe heet u?` to Introducing Yourself (Dutch Expert §8 item 4). Defer.
- Diminutives reference card (Dutch Expert §8 item 7). Defer.
- Adding `Mag ik in het Nederlands oefenen?` to Les 1: Zinnen (Dutch Expert §8 item 8). Defer.

These are listed in §10 with rationale.

---

## 9. Code changes — exact before / after

### 9.1 VERSION bump

**File:** `nederly.html`, function `initStorage()`.

**Before:**
```js
const VERSION = '3'; // bump this when you add new lesson data above
```

**After:**
```js
const VERSION = '4'; // bump this when you add new lesson data above
```

This triggers a one-time re-seed of `nederly_words`, `nederly_categories`, `nederly_minimal_pairs`, `nederly_sessions`, `nederly_attempts` on next load.

### 9.2 CSS — add progress bar styles

**Insert into `<style>` block, immediately after the existing `.dots` / `.dot.active` rules (~line 70):**

```css
/* Category progress bar — Per Dyslexia Expert §11.1 */
.progress-row {
  display: flex; align-items: center; gap: 8px;
  margin-top: 0; margin-bottom: 8px;
}
.progress-track {
  flex: 1;
  height: 6px;
  background: #E8DFC4;
  border-radius: 3px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: #2E6DA4;
  border-radius: 3px;
  transition: width 300ms ease-out;
}
.progress-label {
  font-size: 16px;
  color: #6B6B6B;
  flex-shrink: 0;
}
```

### 9.3 CSS — sound-card line clamp + "Show more" toggle

**Modify `.sound-desc` and add a `.sound-toggle` rule:**

**Before:**
```css
.sound-desc { font-size: 16px; color: #1A1A1A; line-height: 26px; }
```

**After:**
```css
.sound-desc {
  font-size: 16px; color: #1A1A1A; line-height: 26px;
}
.sound-desc.clamped {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.sound-toggle {
  background: none; border: none; padding: 4px 0;
  color: #2E6DA4; font-size: 16px; cursor: pointer;
  min-height: 36px; text-align: left; font-family: inherit;
  letter-spacing: 0.04em;
}
```

> Per Dyslexia Expert §9 still-required item.

### 9.4 JS — add `sessionHtml()` progress bar

**Modify `sessionHtml()` to insert the progress bar between dots and card.**

**Before** (line ~826):
```js
return `
    <div class="screen">
      ${dotsHtml(words.length, S.sessionIndex)}
      <div class="card ${revealed ? 'revealed' : ''}" ...
```

**After:**
```js
const totalWords = words.length;
const currentPos = Math.min(S.sessionIndex + (revealed ? 1 : 0), totalWords);
const pctFill = (currentPos / totalWords) * 100;
return `
    <div class="screen">
      ${dotsHtml(words.length, S.sessionIndex)}
      <div class="progress-row">
        <div class="progress-track">
          <div class="progress-fill" style="width:${pctFill}%"></div>
        </div>
        <span class="progress-label">${currentPos} of ${totalWords}</span>
      </div>
      <div class="card ${revealed ? 'revealed' : ''}" ...
```

> Fill advances **on reveal** (so the learner sees motion as they engage), not only after pressing Got it / Missed.

### 9.5 JS — track category name on session start

**Add new state field** in `S` (state object, ~line 697):

```js
sessionCategoryName: null,
```

**Modify `select-category` handler** (~line 1061) — after `const words = getWordsByCategory(catId);`:

```js
const cat = getCategories().find(c => c.id === catId);
S.sessionCategoryName = cat ? cat.name : null;
```

**Modify `start-session` handler** (paste flow) — set to null explicitly:

```js
S.sessionCategoryName = null;
```

### 9.6 JS — replace `sessionCompleteHtml()` with mastery card

**Before** (lines ~842–874): the full `sessionCompleteHtml()` function with `.pct`, `pct-label`, and percentage calculation.

**After:**
```js
function sessionCompleteHtml() {
  const out = getSessionOutcomes(S.sessionId);
  const total = out.correct + out.incorrect + out.skipped;
  const categoryLine = S.sessionCategoryName
    ? `Category: ${S.sessionCategoryName}`
    : 'Pasted vocab';
  const skippedRow = out.skipped > 0 ? `
    <div class="outcome-row-item">
      <span style="color:#6B6B6B;font-size:18px;width:24px;text-align:center">–</span>
      <span style="flex:1;font-size:18px">Skipped</span>
      <strong style="color:#6B6B6B;font-size:18px">${out.skipped}</strong>
    </div>` : '';
  return `
    <div class="complete-screen">
      <h2 style="font-size:20px;font-weight:600">Nice session.</h2>
      <p style="font-size:18px;color:#1A1A1A;margin-top:16px">
        You practiced ${total} word${total !== 1 ? 's' : ''} today.
      </p>
      <p style="font-size:18px;color:#1A1A1A">${categoryLine}</p>
      <div style="width:100%;display:flex;flex-direction:column;gap:8px;margin-top:24px">
        <div class="outcome-row-item">
          <span style="color:#3A7D44;font-size:18px;width:24px;text-align:center">✓</span>
          <span style="flex:1;font-size:18px">Got it</span>
          <strong style="color:#3A7D44;font-size:18px">${out.correct}</strong>
        </div>
        <div class="outcome-row-item">
          <span style="color:#D94F3D;font-size:18px;width:24px;text-align:center">✗</span>
          <span style="flex:1;font-size:18px">Missed</span>
          <strong style="color:#D94F3D;font-size:18px">${out.incorrect}</strong>
        </div>
        ${skippedRow}
      </div>
      <button class="home-btn" data-action="go-home">Back home</button>
    </div>`;
}
```

> The `.pct` and `.pct-label` CSS rules become dead — **leave them in v4** (other code may reference them in future; harmless). No CSS removal.

CTA label change: "Back to home" → **"Back home"** per Dyslexia Expert §11.2 ("Back home" is the spec'd label).

### 9.7 JS — Sounds screen line-clamp toggle

**Add state field** in `S`:
```js
soundExpanded: {},
```

**Modify `soundsHtml()`** card render. Replace:
```js
<p class="sound-desc">${s.desc}</p>
```

With:
```js
const key = `${s.section}:${s.sound}`;
const expanded = !!S.soundExpanded[key];
const descClass = expanded ? 'sound-desc' : 'sound-desc clamped';
const toggleLabel = expanded ? 'Show less' : 'Show more';
// Note: the toggle button is rendered unconditionally;
// post-render JS hides it on cards that don't actually overflow.
return `
  <div class="sound-card">
    <div class="sound-card-top">
      <span class="sound-spelling">${colorHtml(s.sound)}</span>
      ${starHtml}
    </div>
    <p class="${descClass}" data-sound-key="${key}">${s.desc}</p>
    <button class="sound-toggle" data-action="toggle-sound" data-key="${key}">${toggleLabel}</button>
    <div class="sound-example-row">
      ...
```

**Add click handler** (in the `document.addEventListener('click', ...)` block, before the final `}`):
```js
if (action === 'toggle-sound') {
  const key = btn.dataset.key;
  S.soundExpanded[key] = !S.soundExpanded[key];
  render();
  return;
}
```

**Add post-render hide pass.** In `render()`, after `document.getElementById('app').innerHTML = ...`:
```js
// Hide "Show more" on sound cards that don't actually overflow
if (currentScreen() === 'Sounds') {
  requestAnimationFrame(() => {
    document.querySelectorAll('.sound-desc.clamped').forEach(el => {
      if (el.scrollHeight <= el.clientHeight + 1) {
        const key = el.dataset.soundKey;
        const toggle = document.querySelector(`.sound-toggle[data-key="${key}"]`);
        if (toggle) toggle.style.display = 'none';
      }
    });
  });
}
```

### 9.8 JS — content edits in CATEGORIES and MINIMAL_PAIRS

Per §8.1 through §8.6. The Builder makes these edits literally in the constants at the top of the `<script>` block.

### 9.9 No other code touched

- `homeHtml`, `addVocabHtml`, `categoriesHtml`, `minimalPairsHtml`, `progressHtml`, `colorHtml`, `getHint`, `speak`, `initStorage` body (only VERSION literal), storage helpers, event handlers other than the additions above: **unchanged**.
- Header, back navigation, dots helper: **unchanged**.
- Existing token CSS rules: **unchanged** (only additions in §9.2, §9.3).

---

## 10. Out of scope — explicit (not in v4)

Listed with the upstream doc that proposed each, plus the reason for deferral.

| Item | Upstream | Why deferred |
|------|----------|--------------|
| Grammar reference screen (subordinate-clause verb-final, diminutives, number inversion grammar) | Dutch Expert §3.5, §3.7, §3.13 | Per brief: "keep the app practice-focused, grammar lives in the Dutch Expert doc only" for v4. Add in a future version once the practice loop is stable. The Numbers 21+ category in §8.4 covers the *practice* angle of inversion; the rule itself stays in the Dutch Expert doc. |
| Non-decaying mastery badges (the 20px green circle on a mastered word) | Dyslexia Expert §11.3 | More ambitious — requires a per-word mastery score across sessions. Defer to v5. |
| Rotating daily prompt picker on Home | Dyslexia Expert §11.4 | More ambitious — needs daily rotation logic + persistent shuffle seed. Defer to v5. |
| Opt-in short-term goal nudge ("Want to focus on one sound today?") | Dyslexia Expert §11.5 | More ambitious — needs session-counter logic + sound-weighting in session generator. Defer to v6+. |
| Adding `Hoe heet u?` to Introducing Yourself | Dutch Expert §8 item 4 | Low priority per Dutch Expert; defer. |
| Diminutives reference card (`bier/biertje`, etc.) | Dutch Expert §8 item 7 | Reference content; needs a new screen type or section. Defer. |
| Adding `Mag ik in het Nederlands oefenen?` to Les 1: Zinnen | Dutch Expert §8 item 8 | One-line content add; deliberately bundled with future content pass. |
| Clock-time vocabulary (`Hoe laat is het?`, `kwart over`, `half`, `kwart voor`) | Dutch Expert §8 deferred | A0/A1 boundary content; defer. |
| Subordinate-clause example sentences | Dutch Expert §8 deferred | Defer until V2 word order is stable for this learner (week 7+). |
| Per-phoneme pronunciation scoring (Azure-style) | Designer Brief §1, Dyslexia Expert §6 | Explicitly not in v1. v2 path. |
| Spaced-repetition session generator (mix of recent + older items) | Dyslexia Expert §8 "Spaced practice over massed" | Needs a per-word last-seen timestamp + scheduler. Defer to v5+. |
| OpenDyslexic Bold `@font-face` | Dyslexia Expert §9 new observation | Requires shipping `OpenDyslexic-Bold.woff2` alongside the HTML. Not blocking; defer. |
| 320px viewport overflow check (drop letter-spacing to 0.03em if vocab word wraps) | Dyslexia Expert §9 new observation | Verification step, not a code change unless overflow occurs. Builder tests on 320px viewport — if no wrap, no change. |
| **Streaks, lives/hearts, XP/levels, leaderboards, push-notifications-about-streaks, time-of-day escalating reminders, percentage scores at session end** | Dyslexia Expert §11.6, §7 | **POLICY — never build.** Embedded here as a permanent boundary, not a deferral. |

---

## 11. Verification checklist for the Builder

After implementing §8 + §9, the Builder confirms:

1. Opening `nederly.html` with stale `nederly_initialized = '3'` in localStorage triggers a one-time re-seed (no visible error).
2. **Food & Drink** category shows 10 items including thee, melk, bier, vlees, groente.
3. **Transport & Directions** shows 9 items including de fiets, het vliegveld, rechtdoor, Hoe kom ik bij?.
4. **Places** shows 7 items including de apotheek, de bibliotheek.
5. A new category **Numbers 21+ (Inversion)** appears with 3 items.
6. Minimal-pair drill includes `uit / ijs` and **does not** include `huis / hijs` or `neus / noos`.
7. Starting any category session shows a thin blue progress bar between the dots row and the card; label reads "1 of N" → advances on reveal/advance → reaches "N of N" on the last card.
8. Completing a session lands on a screen titled "Nice session." with no percentage, showing "You practiced N words today.", the category name (or "Pasted vocab"), and the ✓/✗ counts.
9. Sound guide cards show ≤2 lines of description. A "Show more" link appears on cards whose description would overflow; it expands to full text and toggles to "Show less".
10. Cards whose description fits in 2 lines do **not** show a "Show more" link.
11. No console errors. No layout breakage at 320px width.
12. `localStorage.getItem('nederly_initialized')` reads `'4'` after first load.

---

*End of design_spec.md. Hand off to: Builder.*
