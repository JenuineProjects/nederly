# Nederly — Designer Agent Report
*Focus: professional visual polish, phonetic display, flashcard UX*
*Version bump: 5 → 6 | Generated: 2026-05-22*

---

## 1. Architecture Decision

Nederly remains a fully offline single-page application. No network requests, no backend, no API keys. All vocabulary, phonetic data, and logic are hardcoded in `index.html`. Storage is `localStorage`. Speech is the browser's built-in Web Speech API (`lang: nl-NL`). The file opens by double-click or GitHub Pages — no build step, no server.

---

## 2. Tech Stack

| Layer | Technology |
|-------|-----------|
| Markup | Single `index.html` — HTML5 |
| Style | `<style>` block inside `index.html` — plain CSS, no preprocessor |
| Logic | `<script>` block inside `index.html` — vanilla ES6+ JS, no framework |
| Font | `OpenDyslexic` loaded via `@font-face` from local `woff2` file |
| Speech | `window.speechSynthesis` — Web Speech API, `lang: nl-NL` |
| Storage | `localStorage` — keys prefixed `nederly_` |
| Hosting | GitHub Pages (static file delivery) |

No changes to the tech stack in this version.

---

## 3. Data Model Changes

### 3a. New fields on each word object in `CATEGORIES`

Every word object gains the following new fields. Fields marked `[new]` do not exist in v5.

| Field | Type | Required for nouns? | Required for verbs/phrases? | Source |
|-------|------|--------------------|-----------------------------|--------|
| `article` | `string\|null` | Yes — `"de"` or `"het"` | `null` | Dutch Expert §6 |
| `respelling` | `string` | Yes | Yes | Dutch Expert §6 IPA + Respelling Table |
| `audioRequired` | `boolean` | Yes | Yes | Dutch Expert §6 — `true` for all ★ entries |
| `articulatoryHint` | `string` | Yes | Yes | Phonetics §4 (on-screen hints) |
| `ipa` | `string` | Yes | Yes | Dutch Expert §6 — stored, not shown by default |
| `trapRank` | `number\|null` | Yes | Yes | Phonetics §2 — 1–10; `null` if not a trap sound |
| `soundCategory` | `string` | Yes | Yes | Phonetics §2 — e.g. `"ui-diphthong"`, `"eu-vowel"`, `"g-initial"`, `"default"` |
| `syllableCount` | `number` | Yes | Yes | Phonetics §6 — integer |
| `phraseChunks` | `string[]\|null` | `null` | For multi-word phrases: array of respelling chunks | Phonetics §6 |

**Note on `audioFile`:** Phonetics §6 includes `audioFile` in the spec. Since v6 uses Web Speech API only (offline, no audio assets), this field is **omitted** from the v6 data model. The Builder does not add it. It is reserved for a future version when recorded audio files are available.

### 3b. Minimal example — single noun

```js
{
  dutch: 'de keuken',
  english: 'the kitchen',
  article: 'de',
  respelling: 'KUR-kun',
  audioRequired: true,
  articulatoryHint: "Shape your lips into an 'oo' circle, then say 'ay' without moving your lips — keep both at once.",
  ipa: '/də ˈkøːkən/',
  trapRank: 3,
  soundCategory: 'eu-vowel',
  syllableCount: 2,
  phraseChunks: null,
}
```

### 3c. Minimal example — phrase

```js
{
  dutch: 'Mag ik de rekening, alstublieft?',
  english: 'May I have the bill, please?',
  article: null,
  respelling: 'makh ik duh RAY-kun-ing al-stuu-BLEEFT',
  audioRequired: false,
  articulatoryHint: "The article 'de' is a very short 'duh' — do not say 'day'.",
  ipa: '/mɑx ɪk də ˈreːkənɪŋ ˌɑlstyˈbliːft/',
  trapRank: 9,
  soundCategory: 'schwa',
  syllableCount: 9,
  phraseChunks: ['makh', 'ik', 'duh', 'RAY-kun-ing', 'al-stuu-BLEEFT'],
}
```

### 3d. How data is seeded

All new fields are hardcoded directly in the `CATEGORIES` array in `index.html`. The complete values come from Dutch Expert §6 (IPA + Respelling Table). The Builder must add the fields to every word object across all 20 categories before the VERSION bump. Words that are not in Dutch Expert §6 use `respelling: ""`, `audioRequired: false`, `articulatoryHint: ""`, `ipa: ""`, `trapRank: null`, `soundCategory: "default"`, `syllableCount: 1`, `phraseChunks: null`.

### 3e. Storage seeding changes

`initStorage()` currently seeds `K.words` with objects that have only `id`, `dutch`, `english`, `categoryId`, `sessionId`, `createdAt`. The Builder must add the new fields to the seeded word objects so that `getWordsByCategory()` and `getWordsByIds()` return objects that include `respelling`, `audioRequired`, `articulatoryHint`, `ipa`, `trapRank`, `soundCategory`, `syllableCount`, `phraseChunks`, and `article`.

### 3f. VERSION bump

```js
const VERSION = '6'; // was '5'
```

---

## 4. Screen Changes

### 4a. Session screen (flashcard mode) — PRIMARY CHANGE

This is the main deliverable. Current `sessionHtml()` shows: Dutch word → Play button → tap-to-reveal → English. The hint (`getHint()`) is shown **after** reveal only.

**New card layout:** the respelling chip and audio controls are **always visible** (pre-reveal). The English meaning and article chip appear **after** tap-to-reveal. The articulatory hint is hidden behind a tap on the ★ badge.

#### ASCII wireframe — card face BEFORE reveal

```
+-----------------------------------------------+
|  [progress dots]                              |
|  [progress bar ████░░░░░░░░  3 of 10]         |
|                                               |
|  +-------------------------------------------+
|  |                                           |
|  |   de keuken                               |  <- .card-word 32px centred, colour-coded
|  |                                           |
|  |   [ KUR-kun ★ ]                           |  <- .card-phonetic chip, purple, centred
|  |                                           |
|  |   [ ▶ Play ]  [ ▶ Slow ]                  |  <- .play-row always visible
|  |                                           |
|  |   - - - - - tap to reveal - - - - - - -   |  <- .card-tap 16px muted
|  |                                           |
|  +-------------------------------------------+
+-----------------------------------------------+
```

#### ASCII wireframe — card face AFTER reveal

```
+-----------------------------------------------+
|  [progress dots]                              |
|  [progress bar ████████░░░░  4 of 10]         |
|                                               |
|  +-------------------------------------------+  <- .card.revealed (blue border)
|  |                                           |
|  |   de keuken                               |  <- .card-word 32px centred, colour-coded
|  |                                           |
|  |   [ KUR-kun ★ ]                           |  <- .card-phonetic chip, always visible
|  |                                           |
|  |   [ ▶ Play ]  [ ▶ Slow ]                  |  <- both buttons always visible
|  |                                           |
|  |   ─────────────────────────────────────   |  <- visual divider <hr>
|  |                                           |
|  |   [de]  the kitchen                       |  <- article chip + .card-english 18px
|  |                                           |
|  +-------------------------------------------+
|                                               |
|  [ ✗ Practice again ]  [ ✓ Got it ]           |  <- .outcome-row
+-----------------------------------------------+
```

If word has `audioRequired: true`, the chip reads `KUR-kun ★` where ★ is tappable:
- Tap ★ badge → reveals `.articulatory-hint` paragraph below chip (one line, 16px, `#5C5C5C`)
- Tap ★ again → hides hint
- Hint is shown **above** the reveal line — it is a pre-reveal tool (Dyslexia Expert §8; Phonetics §6)

#### What the Slow button does

Current code only shows Slow after reveal:
```js
${revealed ? `<button class="play-btn slow" ...>▶ Slow</button>` : ''}
```
**Change:** Slow button is always rendered, not conditionally on `revealed`. (Dyslexia Expert §4.)

#### Auto-play on first card

On the first card of a session (`S.sessionIndex === 0` and `!S.sessionRevealed`), call `speak(word.dutch, false)` once after render. Subsequent cards: no auto-play. (Dyslexia Expert §4.)

#### Missed card re-insertion

Current code advances linearly. When outcome is `"incorrect"`, re-insert the current word at position `current + 2` (or at end if fewer than 2 cards remain) before incrementing index. (Dyslexia Expert §6.)

#### Article chip (post-reveal)

After reveal, show a colour-coded article chip:
- `de` → chip background `#E8F0F9`, text `#2E6DA4` (blue)
- `het` → chip background `#EBF5EC`, text `#2F7A3B` (green)
- `null` (verb/phrase) → no chip, show English only

```
[de]  the kitchen       <- chip + English inline
```

Chip CSS (`.article-chip`):
```css
.article-chip {
  display: inline-block;
  font-size: 15px;
  line-height: 22px;
  padding: 1px 8px;
  border-radius: 4px;
  font-weight: 600;
  margin-right: 6px;
  vertical-align: middle;
}
.article-chip.de  { background: #E8F0F9; color: #2E6DA4; }
.article-chip.het { background: #EBF5EC; color: #2F7A3B; }
```

---

### 4b. Header

**Current:** `background: #FAF3E0` (same as page) — does not visually separate from content.

**Change:**
```css
.header {
  background: #FFFFFF;
  border-bottom: 1px solid #D4CBBA;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  padding: 14px 20px;
}
.header h1 {
  font-size: 22px;  /* was 20px */
  font-weight: 700; /* was 600 */
}
```
Source: Dyslexia Expert §9.

---

### 4c. Home screen

**No structural changes.** Visual polish only:

- `nav-btn` background: `#FFFFFF` (was `#FAF3E0`)
- `nav-btn` border: `1px solid #D4CBBA` (was `1px solid #E0D8C8`)
- `nav-btn` border-radius: `12px` (was `8px`)
- `nav-btn` add shadow: `0 1px 4px rgba(0,0,0,0.06)`
- `nav-btn:hover` background: `#F0EBF9` (was `#F0E8D0`)
- Back button text: `←` (already in current code — keep)

Source: Dyslexia Expert §9.

---

### 4d. Minimal Pairs screen

- `.pair-word-a` colour: `#1A1A1A` (was `#E07B39`) — remove orange, both words same colour
- `.pair-word-b` colour: `#1A1A1A` (was `#2E6DA4`) — remove blue
- `.pair-card` background: `#FFFFFF` (was `#FAF3E0`)
- `.pair-card` border-radius: `16px` (was `12px`)
- `.pair-card.correct` border-color: `#2F7A3B` (was `#3A7D44`)
- `.pair-card.incorrect` border-color: `#B35C00` (was `#D94F3D`) — amber not red (Dyslexia Expert §6)
- `.pair-card.incorrect` background: `#FDF3E6` (was `#FDF0EF`) — amber tint not red tint

Source: Dyslexia Expert §9; Phonetics §5.

---

### 4e. Progress dots and progress bar

- `.dot.done` background: `#2F7A3B` (was `#3A7D44`) — consistent with `--accent-green`
- `.dots` gap: `8px` (was `6px`) — 8px rhythm (Dyslexia Expert §9)
- `.progress-label` color: `#5C5C5C` (was `#6B6B6B`) — better contrast

---

### 4f. Session complete screen

- Green checkmark colour: `#2F7A3B` (was `#3A7D44`)
- Red cross colour: `#C0392B` (was `#D94F3D`)
- `.home-btn` border-radius: `12px` (was `8px`)
- `.home-btn` color: `#FFFFFF` (was `#FAF3E0`)

---

### 4g. Sound cards

- `.sound-card` background: `#FFFFFF` (was `#FAF3E0`)
- `.sound-card` gap: `8px` (was `6px`)
- `.sound-star` color: `#B35C00` (was `#E07B39`) — consistent with `--accent-amber`

---

## 5. Component Contracts

### 5a. Flashcard component (`sessionHtml()`)

**Input (word object):** now includes `respelling`, `audioRequired`, `articulatoryHint`, `article`, `ipa`.

**Visual states:**

| State | Card border | Card bg | Phonetic chip | Audio buttons | English | Article chip | Outcome buttons |
|-------|------------|---------|--------------|--------------|---------|-------------|----------------|
| Pre-reveal | `#D4CBBA` 1px | `#FFFFFF` | Visible, purple | Play + Slow both visible | Hidden | Hidden | Hidden |
| Pre-reveal, ★ tapped | `#D4CBBA` 1px | `#FFFFFF` | Visible, purple | Play + Slow both visible | Hidden | Hidden | Hidden; articulatory hint shown below chip |
| Revealed | `#2E6DA4` 2px | `#FFFFFF` | Visible, purple | Play + Slow both visible | Visible | Visible (if noun) | Visible |
| Got it pressed | Navigate to next card | | | | | | |
| Missed pressed | Re-insert at +2, navigate to next | | | | | | |

### 5b. Phonetic chip (`.card-phonetic`)

**Props used:** `word.respelling`, `word.audioRequired`

**Render rules:**
- If `respelling` is empty string (`""`): render nothing (no chip)
- If `audioRequired === true`: append `<span class="phonetic-star" data-action="toggle-hint" data-word-id="${word.id}">★</span>` after the respelling text inside the chip
- The chip is always present above the reveal line (pre-reveal and post-reveal)

### 5c. Articulatory hint (`.articulatory-hint`)

**Props used:** `word.articulatoryHint`, `S.hintExpanded[word.id]`

**Render rules:**
- Hidden by default — class `.articulatory-hint` without `.visible`
- Shown when user taps ★ badge — class `.articulatory-hint.visible`
- Positioned between chip and Play/Slow row
- If `articulatoryHint` is an empty string, do not render the element at all (no empty box)

**New state field required in initial `S` object:**
```js
hintExpanded: {},  // { [wordId]: boolean }
```

### 5d. Article chip (`.article-chip`)

**Props used:** `word.article`

**Render rules:**
- Only rendered post-reveal
- `null` → no chip; only `.card-english` text rendered
- `"de"` → `<span class="article-chip de">de</span>`
- `"het"` → `<span class="article-chip het">het</span>`
- Chip renders inline before the English text in the same `<div>`

---

## 6. Design Tokens (Complete)

Copy this `:root` block verbatim into the `<style>` section at the very top of the existing CSS rules, before any selector rules.

```css
:root {
  /* Backgrounds */
  --bg:             #F7F2E8;
  --surface:        #FFFFFF;
  --surface-raised: #F0EBE0;

  /* Text */
  --text-primary:   #1A1A1A;
  --text-secondary: #5C5C5C;

  /* Borders */
  --border:         #D4CBBA;
  --border-light:   #E0D8C8;

  /* Accent — Blue (primary CTA, active states) */
  --accent-blue:       #2E6DA4;
  --accent-blue-light: #E8F0F9;

  /* Accent — Green (success) */
  --accent-green:       #2F7A3B;
  --accent-green-light: #EBF5EC;

  /* Accent — Red (error — use sparingly) */
  --accent-red:       #C0392B;
  --accent-red-light: #FDECEA;

  /* Accent — Amber (audio-required flag, missed state) */
  --accent-amber:       #B35C00;
  --accent-amber-light: #FDF3E6;

  /* Accent — Purple (phonetic chip) */
  --accent-purple:       #5C3F8F;
  --accent-purple-light: #F0EBF9;

  /* Spacing — 8px rhythm */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 40px;
}
```

### Typography (literal values — not tokens)

| Role | Selector | px size | Line-height | Letter-spacing |
|------|---------|---------|-------------|----------------|
| Card Dutch word | `.card-word` | 32px | 48px | 0.02em |
| App title | `.header h1` | 22px | — | — |
| Section heading | `h2`, `.lesson-detail-title` | 22px | 32px | 0.01em |
| Body / UI labels | `body`, `.card-english` | 18px | 29px | 0.04em |
| Secondary / meta | `.card-tap`, `.session-type`, `.progress-label` | 16px | 26px | 0.03em |
| Phonetic chip text | `.card-phonetic` | 15px | 24px | 0.03em |
| Section labels (caps) | `.section-label`, `.sound-section-heading` | 13px | 20px | 0.08em |

### Card styling

| Property | Value |
|----------|-------|
| background | `#FFFFFF` |
| border | `1px solid #D4CBBA` |
| border-radius | `16px` |
| box-shadow | `0 2px 8px rgba(0,0,0,0.08)` |
| padding | `28px 24px` |
| min-height | `220px` |
| revealed border | `2px solid #2E6DA4` |
| revealed shadow | `0 2px 12px rgba(46,109,164,0.15)` |

### Phonetic chip styling (exact CSS)

```css
.card-phonetic {
  font-size: 15px;
  line-height: 24px;
  letter-spacing: 0.03em;
  color: #5C3F8F;
  background: #F0EBF9;
  border-radius: 6px;
  padding: 2px 10px;
  display: inline-block;
  font-style: normal;
  text-align: center;
  max-width: 100%;
}
.phonetic-star {
  color: #B35C00;
  font-size: 14px;
  margin-left: 4px;
  vertical-align: middle;
  cursor: pointer;
}
```

### Articulatory hint styling (exact CSS)

```css
.articulatory-hint {
  font-size: 16px;
  line-height: 26px;
  color: #5C5C5C;
  text-align: center;
  padding: 4px 8px;
  display: none;
}
.articulatory-hint.visible {
  display: block;
}
```

---

## 7. Changes Summary Table

| # | Area | Change | Source |
|---|------|--------|--------|
| 1 | Data | Add `article`, `respelling`, `audioRequired`, `articulatoryHint`, `ipa`, `trapRank`, `soundCategory`, `syllableCount`, `phraseChunks` to every word object in `CATEGORIES` | Phonetics §6; Dutch Expert §6 |
| 2 | Data | Seed all new fields in `initStorage()` when building word objects pushed to `K.words` | Phonetics §6 |
| 3 | Data | Bump `VERSION` constant from `'5'` to `'6'` | — |
| 4 | CSS | Add `:root` custom properties block at top of `<style>` | §6 tokens |
| 5 | CSS | `body` background: `#FAF3E0` → `#F7F2E8` | Dyslexia Expert §2 |
| 6 | CSS | `theme-color` meta tag: `#FAF3E0` → `#F7F2E8` | Dyslexia Expert §2 |
| 7 | CSS | `.header` background: `#FAF3E0` → `#FFFFFF`; add `box-shadow: 0 1px 3px rgba(0,0,0,0.06)`; border `#E0D8C8` → `#D4CBBA` | Dyslexia Expert §9 |
| 8 | CSS | `.header h1` font-size: `20px` → `22px`; font-weight: `600` → `700` | Dyslexia Expert §10 |
| 9 | CSS | `.card` background: `#FAF3E0` → `#FFFFFF`; border: `2px solid #E0D8C8` → `1px solid #D4CBBA`; border-radius: `12px` → `16px`; add `box-shadow: 0 2px 8px rgba(0,0,0,0.08)`; min-height: `200px` → `220px`; padding: `24px` → `28px 24px` | Dyslexia Expert §9 |
| 10 | CSS | `.card.revealed` add `box-shadow: 0 2px 12px rgba(46,109,164,0.15)` | Dyslexia Expert §9 |
| 11 | CSS | `.card-word` font-size: `26px` → `32px`; line-height: `40px` → `48px`; add `letter-spacing: 0.02em` | Dyslexia Expert §1 |
| 12 | CSS | Remove `.card-ipa` rule entirely | Dyslexia Expert §8 |
| 13 | CSS | Add `.card-phonetic` rule (purple chip — see §6 exact CSS) | Dyslexia Expert §8 |
| 14 | CSS | Add `.phonetic-star` rule (amber, 14px, pointer cursor) | Dyslexia Expert §8 |
| 15 | CSS | Add `.articulatory-hint` and `.articulatory-hint.visible` rules | Phonetics §6 |
| 16 | CSS | Add `.article-chip`, `.article-chip.de`, `.article-chip.het` rules | Phonetics §5; Dutch Expert §3 |
| 17 | CSS | `.play-btn` min-height: `48px` → `56px`; padding: `8px 16px` → `10px 20px`; border-radius: `8px` → `12px`; add `box-shadow: 0 2px 6px rgba(46,109,164,0.25)` | Dyslexia Expert §3, §9 |
| 18 | CSS | `.play-btn.slow` background: `#6B4FA0` → `#5C3F8F` | Dyslexia Expert §2 |
| 19 | CSS | `.missed-btn` border: `1px solid #D94F3D` → `2px solid #B35C00`; background: `#FAF3E0` → `#FDF3E6`; min-height: `48px` → `56px`; border-radius: `8px` → `12px` | Dyslexia Expert §6, §9 |
| 20 | CSS | `.got-btn` background: `#3A7D44` → `#2F7A3B`; color: `#FAF3E0` → `#FFFFFF`; min-height: `48px` → `56px`; border-radius: `8px` → `12px` | Dyslexia Expert §2, §9 |
| 21 | CSS | `.nav-btn` background: `#FAF3E0` → `#FFFFFF`; border `#E0D8C8` → `#D4CBBA`; border-radius: `8px` → `12px`; add `box-shadow: 0 1px 4px rgba(0,0,0,0.06)` | Dyslexia Expert §9 |
| 22 | CSS | `.nav-btn:hover` background: `#F0E8D0` → `#F0EBF9` | Dyslexia Expert §9 |
| 23 | CSS | `.start-btn` border-radius: `8px` → `12px`; add `box-shadow: 0 2px 6px rgba(46,109,164,0.25)` | Dyslexia Expert §9 |
| 24 | CSS | `.start-btn:disabled` background: `#A0A0A0` → `#D4CBBA`; add `color: #9A9A9A` | Dyslexia Expert §9 |
| 25 | CSS | `.home-btn` border-radius: `8px` → `12px`; color: `#FAF3E0` → `#FFFFFF` | Dyslexia Expert §9 |
| 26 | CSS | `.dots` gap: `6px` → `8px` | Dyslexia Expert §9 |
| 27 | CSS | `.dot.done` background: `#3A7D44` → `#2F7A3B` | Dyslexia Expert §9 |
| 28 | CSS | `.progress-label` color: `#6B6B6B` → `#5C5C5C` | Dyslexia Expert §2 |
| 29 | CSS | `.pair-word-a` color: `#E07B39` → `#1A1A1A` | Dyslexia Expert §9 |
| 30 | CSS | `.pair-word-b` color: `#2E6DA4` → `#1A1A1A` | Dyslexia Expert §9 |
| 31 | CSS | `.pair-card` background: `#FAF3E0` → `#FFFFFF`; border-radius: `12px` → `16px` | Dyslexia Expert §9 |
| 32 | CSS | `.pair-card.correct` border-color: `#3A7D44` → `#2F7A3B`; background: `#F0FBF1` → `#EBF5EC` | Dyslexia Expert §2 |
| 33 | CSS | `.pair-card.incorrect` border-color: `#D94F3D` → `#B35C00`; background: `#FDF0EF` → `#FDF3E6` | Dyslexia Expert §6 |
| 34 | CSS | `.sound-card` background: `#FAF3E0` → `#FFFFFF`; gap: `6px` → `8px` | Dyslexia Expert §9 |
| 35 | CSS | `.sound-star` color: `#E07B39` → `#B35C00` | Dyslexia Expert §9 |
| 36 | CSS | `.stat-box` border-radius: `8px` → `12px`; add `background: #FFFFFF` | Dyslexia Expert §9 |
| 37 | CSS | `.lesson-card` background: `#FAF3E0` → `#FFFFFF`; border-radius: `10px` → `12px`; add `box-shadow: 0 1px 4px rgba(0,0,0,0.06)` | Dyslexia Expert §9 |
| 38 | CSS | `.lesson-card:hover` background: `#F0E8D0` → `#F0EBF9` (surface-raised tint) | Dyslexia Expert §9 |
| 39 | JS data | Update `COLOR_PATTERNS` hex `#E07B39` (diphthong orange) → `#B35C00` in JS array | Dyslexia Expert §9 |
| 40 | JS data | Update `COLOR_PATTERNS` hex `#D94F3D` (consonant cluster red) → `#C0392B` in JS array | Dyslexia Expert §2 |
| 41 | JS render | `sessionHtml()`: add `.card-phonetic` chip HTML block below `.card-word`, always rendered (pre- and post-reveal) | Dyslexia Expert §8; Phonetics §6 |
| 42 | JS render | `sessionHtml()`: render `.articulatory-hint` element (hidden by default); class `.visible` added/removed by toggle-hint action | Phonetics §6; Dyslexia Expert §8 |
| 43 | JS render | `sessionHtml()`: Slow button always rendered (remove `revealed ?` conditional around it) | Dyslexia Expert §4 |
| 44 | JS render | `sessionHtml()`: post-reveal block — render `.article-chip.de` or `.article-chip.het` chip before `.card-english` if `word.article` is non-null | Phonetics §5; Dutch Expert §3 |
| 45 | JS render | `sessionHtml()`: add `<hr style="width:100%;border:none;border-top:1px solid #D4CBBA;margin:0">` between audio row and revealed content | Dyslexia Expert §8 |
| 46 | JS state | Add `hintExpanded: {}` to initial `S` state object | — |
| 47 | JS events | Add handler for `data-action="toggle-hint"`: read `data-word-id`, flip `S.hintExpanded[id]`, call `render()` | Phonetics §6 |
| 48 | JS events | Auto-play: after render when `S.sessionIndex === 0 && !S.sessionRevealed`, call `speak(word.dutch, false)` | Dyslexia Expert §4 |
| 49 | JS events | Missed re-insertion: on `advance` with outcome `"incorrect"`, splice the current word object into `S.sessionWords` at `Math.min(S.sessionIndex + 2, S.sessionWords.length)` before advancing `S.sessionIndex` | Dyslexia Expert §6 |
| 50 | JS cleanup | Remove `getHint()` function and `HINTS` constant — replaced by per-word `articulatoryHint` data field | — |

---

## 8. Out of Scope

| Feature | Status |
|---------|--------|
| Audio file recording / playback (`audioFile` field) | Deferred to v7+ — no audio assets; Web Speech API used for all TTS |
| IPA display in the UI | Stored in data model but hidden; Settings toggle is a future enhancement |
| Pronunciation scoring / waveform analysis | Future — requires microphone API and audio analysis library |
| Chunk highlighting during slow playback | Deferred — requires audio timestamps; `phraseChunks` stored for future use |
| Listen-and-repeat exercise screen updates | Not in this run; only flashcard session screen is changed |
| Streaks, lives, timers, leaderboards | Permanently banned (Dyslexia Expert §7) |
| New lesson content categories | Data scope fixed for v6; future lessons are new `CATEGORIES` entries |
| Dark mode / high-contrast mode | Future accessibility enhancement |
| Settings screen | Future — needed once IPA toggle is added |
| AI-generated content | Not applicable — app is offline-only |
| Onboarding modal / tooltip | Not added in v6; first-screen UX is adequate at current scale |

---

*End of Designer Agent Report*
*Cite as: Nederly Designer Agent, 2026-05-22*
*Inputs: Researcher §6–§7 | Dutch Expert §6 | Dyslexia Expert §1–§10 | Phonetics §4–§6 | index.html v5*
