# Dyslexia Expert — Design Principles Document

> UX constraints for Nederly — a dyslexia-friendly Dutch learning app.
> All values are concrete. No Dutch content. No screen mockups. No phonetics.
> Evidence base: see [Researcher §2](./researcher.md#2-engagement-strategies-for-adult-beginners-short-post-lesson-practice) (engagement) and [Researcher §4](./researcher.md#4-dyslexia--language-learning--light-touch-200-words) (dyslexia + L2).

---

## 1. Typography

### Primary Font

**OpenDyslexic** (free, open-source) — strong recommendation, not optional.

- Designed specifically for dyslexic readers
- Bottom-weighted letterforms reduce letter flipping (b/d, p/q)
- Loaded in `nederly.html` via a CSS `@font-face` rule pointing to a WOFF2 file
- Download the WOFF2: https://opendyslexic.org (free; no licence restrictions on web use)

**How to load it in the HTML file:**

```css
@font-face {
  font-family: 'OpenDyslexic';
  src: url('OpenDyslexic-Regular.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

body {
  font-family: 'OpenDyslexic', system-ui, sans-serif;
}
```

`font-display: swap` ensures system-ui renders immediately while the WOFF2 loads, preventing a flash of invisible text.

---

### Fallback Font

**Lexie Readable** (free) — more conventional appearance than OpenDyslexic; some dyslexic users prefer it. Second choice if a user preference toggle is added in future.

### System fallback (if neither loads)

`system-ui, sans-serif` — acceptable last resort; never use a serif or decorative font.

---

### Size Scale

| Element | Size | Notes |
|---------|------|-------|
| Body text | 18px minimum | Vocab items, instructions |
| Dutch vocab word (primary) | 26px minimum | Must be the largest text element on the card |
| IPA / phonetic annotation | 16px | Smaller but still readable; always paired with audio |
| Screen titles | 20px | Bold weight only |
| Button labels | 18px | Never smaller than body text |
| Helper / small text | 16px minimum | Absolute floor — never go below this |

> These values are minimums — go larger, never smaller.

---

### Line Height, Spacing, and Casing

| Property | Value |
|----------|-------|
| Line height (body) | 1.6 |
| Letter spacing (body) | 0.04em |
| Paragraph spacing | `margin-bottom: 1.2em` |
| Word spacing | Default — do not tighten |
| Casing — headings | Sentence case only |
| Casing — buttons | Sentence case |
| Casing — all-caps | **Never.** Removes ascender/descender shape cues. |
| Body alignment | **Left-aligned only.** Never centred, never justified. |
| Single isolated vocab word | Centre-aligned acceptable |

---

### Slow Playback Rate

Slow button uses **0.75× speed**, not 0.5×.

- 0.5× produces unnatural prosody and distorts vowel duration cues
- 0.75× is slow enough to track each sound while remaining recognisably natural speech

Set via Web Speech API: `utterance.rate = 0.75`.

---

## 2. Color & Contrast

### Background

**`#FAF3E0`** — warm off-white / cream.

Justification: pure white (`#FFFFFF`) causes halation on screen, a known difficulty for dyslexic readers. Cream reduces eye strain during 5–15 min sessions without reducing legibility.

### Primary Text

**`#1A1A1A`** — near-black.

Contrast ratio vs `#FAF3E0`: **15.7:1** — exceeds WCAG AAA (7:1).

---

### Accent Palette

| Name | Hex | Use | Contrast vs `#FAF3E0` |
|------|-----|-----|-----------------------|
| Accent Blue | `#2E6DA4` | Long vowels; Play buttons; links | 4.94:1 (AA) |
| Accent Orange | `#E07B39` | Diphthongs | 3.69:1 (large text / decoration only) |
| Accent Red | `#D94F3D` | Consonant clusters; error / missed | 3.69:1 (large text / decoration only) |
| Accent Green | `#3A7D44` | Success / got it | 4.52:1 (AA large) |
| Accent Purple | `#6B4FA0` | Hints; slow play button | 5.83:1 (AA) |

Rules:
- One color per sound category, consistent throughout the app
- Color is never the sole signal — always pair with icon, label, or spatial position
- No more than 2 accent colors on a single screen

---

### State Colors

| State | Hex | Notes |
|-------|-----|-------|
| Success | `#3A7D44` | Same as Accent Green |
| Warning | `#E07B39` | Same as Accent Orange |
| Error / Missed | `#D94F3D` | Same as Accent Red |
| Disabled / Helper | `#6B6B6B` | Contrast ~4.9:1 — passes WCAG AA at all sizes |

---

### Anti-Recommendations

| Combination | Problem |
|-------------|---------|
| Pure white `#FFFFFF` background | Halation; letter swimming for some dyslexic readers |
| Red text on green background | Inaccessible for colour-blind users; visually aggressive |
| Yellow text on white | Near-zero contrast |
| `#A0A0A0` grey text on `#FAF3E0` | 2.36:1 contrast — fails WCAG AA |
| Saturated blue on black | Chromatic aberration on LCD; tiring |
| Any background color change mid-session | Disrupts orientation |

---

## 3. Layout Principles

### Information Density

- **Maximum 5 items visible at once** on any practice screen
- **One primary action per screen**
- **One concept per card** — no card should require two sentences of reading
- Sound guide cards: no paragraph exceeds 2 lines at 18px on a 320px viewport — overflow moves to an expandable area

---

### Spacing

| Token | Value | Use |
|-------|-------|-----|
| xs | 4px | Icon-to-label gap, tight internal padding |
| sm | 8px | Between related items within a card |
| md | 16px | Card internal padding, between list items |
| lg | 24px | Between cards / sections, card padding |
| xl | 40px | Left/right screen margin, section separators |

Use `md` (16px) as the minimum vertical gap between list items.

---

### Touch Targets

| Element | Minimum size |
|---------|-------------|
| Any tappable element | 48×48px |
| Primary action buttons (Play, Start) | `min-height: 64px` |
| Play / audio buttons | `min-height: 48px` |
| Flashcard tap area | Full card width and height |
| Small icon buttons | 48×48px tap area regardless of icon size |

---

### Alignment

- Body and label text: left-aligned. No exceptions for multi-word text.
- Single isolated vocab word on a flashcard: centre acceptable
- Screen titles of 2–3 words: centre acceptable
- Icons paired with text: left of text, vertically centred
- Cards: consistent left/right margin of 40px from screen edge
- Never centre multi-line body text. Never justify.

---

## 4. Audio-First Design

Audio-first is research-supported for adult L2 learners ([Researcher §2.3](./researcher.md#23-audio-first-is-well-supported-for-adults), citing [S39][S40]). For a dyslexic beginner this is doubly relevant — listening bypasses the orthographic-decoding bottleneck ([S41]). **However**, listening is *also* affected by dyslexia, not just reading ([Researcher §4](./researcher.md#4-dyslexia--language-learning--light-touch-200-words), [S41][S62]) — so do not assume audio tasks are "easier"; they need the same affordances (replay, slow, visible control).

### Placement

- Every screen showing a Dutch word/phrase has a **Play button visible without scrolling**
- Play button positioned **above or to the left** of the text it plays
- Never hide audio behind a menu

### Auto-play vs Tap-to-play

**Recommendation: tap-to-play.** Auto-play is startling and removes learner control. Dyslexic learners need multiple repeats and must feel in control of pacing.

### Repeat and Slow Controls

| Control | Behaviour | Web Speech API |
|---------|-----------|----------------|
| Play (primary) | Normal speed | `utterance.rate = 1` |
| Slow (secondary) | 0.75× speed | `utterance.rate = 0.75` |
| Repeat count | Unlimited — no "you've played this N times" warning | Cancel previous utterance before replaying |
| Auto-advance | Off by default | — |

**Implementation note:** Call `window.speechSynthesis.cancel()` before each new `speak()`. Set `utterance.lang = 'nl-NL'`. Select voice inside `speechSynthesis.onvoiceschanged` callback to avoid race conditions where the voice list is empty.

### Availability

Play button remains on screen for the entire interaction with that card. Do not hide or disable it after the learner responds.

---

## 5. Exercise Design — Favor and Avoid

| Exercise Type | Rating | Reason |
|---------------|--------|--------|
| **Flashcards (tap to reveal)** | **Favor** | Low text pressure; learner controls pacing; audio-first compatible |
| **Listen-and-repeat** | **Favor** | Audio-primary; no reading required to attempt; addresses pronunciation goal directly |
| **Minimal-pair discrimination** | **Favor** | Forces active listening; 2 options; minimal text |
| **Multiple choice (select translation)** | **Neutral** | OK with max 3 options, single-word/short-phrase options, audio per option |
| **Matching pairs** | **Neutral** | Max 4 pairs; audio on each item |
| **Tap-to-fill (drag word into blank)** | **Neutral** | OK for short sentences; one blank only; play full sentence first |
| **Type-what-you-hear (spelling from audio)** | **Avoid** | Auditory processing + spelling under pressure = high load; introduces spelling anxiety |
| **Translation (Dutch ↔ English typing)** | **Avoid** | Free-text typing penalises orthographic errors unrelated to the learning goal |

### Spontaneity-deficit consideration

A "language spontaneity deficit" has been proposed for adult dyslexics in L2 — **fluent production under time pressure is disproportionately hard** ([Researcher §4](./researcher.md#4-dyslexia--language-learning--light-touch-200-words), [S63]). Implication: avoid any exercise that combines free production with a clock. Listen-and-repeat is fine because the target is fixed and replayable; timed free-translation is not.

---

## 6. Feedback Design

### Correct Response

- Show: `#3A7D44` (Success Green) border highlight or subtle tint — not a flood
- Sound: short positive tone, ≤500ms
- Text: one short phrase, sentence case — "Nice work" / "That's right"
- Do NOT: show a score, star count, percentage — invites comparison and streak-tracking anxiety
- Transition: 800ms pause then auto-advance, or learner-taps-to-advance (prefer learner-controlled)

### Incorrect Response

- Show: `#D94F3D` (Error Red) subtle border tint — never a full red flood
- Reveal the correct answer immediately in a larger font
- Play the correct audio automatically
- Text: neutral — "Here's the correct answer" not "Wrong!"
- Do NOT: shake the card, play a harsh buzzer, repeat the error back

### Per-Phoneme Pronunciation Feedback

When phoneme scores are available:
- Word shown with each phoneme colour-coded by score:
  - ≥80%: `#3A7D44` (green)
  - 50–79%: `#E07B39` (orange)
  - <50%: `#D94F3D` (red)
- Below the word: one actionable hint for the *lowest-scoring* phoneme only — not all at once
- Label: "Focus on the [sound]" — not "You got [sound] wrong"
- Always include a Play button to hear the correct version

### Language to Avoid

| Avoid | Use instead |
|-------|-------------|
| Wrong! | Here's the correct answer |
| Incorrect | Try again |
| You failed | Not quite — let's hear it again |
| 0 out of 5 | (do not show raw fail scores) |
| Try harder | (never) |

---

## 7. Anti-Patterns — Never Do These

- **Streaks** — externally validated as harmful: streaks shift motivation from intrinsic to loss-aversion, push the striatum into automatic-habit mode, and produce shame/anxiety when broken ([Researcher §2.4](./researcher.md#24-gamification--works-but-the-mechanic-matters), [S44][S45]). Remove entirely.
- **Daily counters / lives / hearts** — same loss-aversion mechanism.
- **Countdown timers** — disadvantage dyslexic learners whose processing speed differs from average; compounded by the spontaneity-deficit finding ([S63]).
- **Whole-paragraph reading** — any screen requiring >2 short sentences before interaction must be redesigned. Instructions = 1 sentence maximum.
- **Decorative italics** — italic letterforms reduce the legibility benefit OpenDyslexic provides. Use bold for emphasis only.
- **Pure-text-no-audio screens** — every Dutch string gets a Play button.
- **Dense vocabulary lists** — max 5 items per session chunk.
- **Small tap targets** — anything below 48×48px causes mis-taps and a sense of failure unrelated to language ability.
- **Passive reading mode** — every screen needs an active task.
- **0.5× slow playback** — distorts vowel length cues; use 0.75×.
- **Inferring ability from L2 reading-task performance** — L2 dyslexia diagnosis is confounded by L2 proficiency ([Researcher §4](./researcher.md#4-dyslexia--language-learning--light-touch-200-words), [S61]). Do not surface "reading speed" or "reading accuracy" metrics that imply learner deficit.

---

## 8. Nederly-Specific Recommendations

### Single HTML file context

Nederly is a single `nederly.html` file opened directly in a mobile browser. No build step, no bundler, no npm. All fonts, styles, and scripts must be:
- Loaded from a relative path alongside `nederly.html`, or
- Embedded directly in the file (base64 data URI for fonts; inline `<style>` for CSS)

The OpenDyslexic WOFF2 (~60 KB) can be embedded as a base64 data URI inside `@font-face` to keep the app fully self-contained.

### Cold-start UX — right after a lesson

The user opens the app immediately after a class session. The first screen should feel like a soft landing, not an intake form. Default: 3–5 buttons labelled with content categories (Greetings, Numbers, Food and Drink, etc.) so the user can tap the topic they just covered without typing. Secondary path on the same screen: a text field to paste a few words or phrases plus a "Start practice" button. No login, no onboarding carousel, no loading animation — under 3 seconds to interactive.

### Real-world / contextual anchoring

Tie practice items to the user's lived NL context (*pinnen* at the supermarkt, *vragen om de rekening*, *mag ik...* requests) rather than generic textbook scenes. This is now research-supported ([Researcher §2.5](./researcher.md#25-real-world--contextual-anchoring), [S46][S47]) — context-embedded vocab outperforms isolated vocab lists in adult studies. The user's own lesson 1 already uses *Mag ik pinnen* as its first whole sentence; that anchoring should be preserved across all generated content.

### Session length

Target session length: 5–15 minutes — microlearning ([Researcher §2.1](./researcher.md#21-session-length--short-and-daily-beats-long-and-sporadic), [S34][S35]). The Babbel "15–30 min daily" sweet spot is the *upper* bound for a Nederly session — the app should make it easy to stop *earlier*. Never nag the user to continue past 15 minutes; surface a soft "good place to stop" affordance from 5 minutes onwards.

### Spaced practice over massed

Items the user has seen should resurface across sessions, not be grouped into one long drill. Spaced > massed for L2 vocab retention ([Researcher §2.2](./researcher.md#22-spaced-practice--massed-practice), [S36][S37]). The Designer should ensure the session generator pulls a mix of recent + older items rather than running through one category back-to-back.

### Audio via Web Speech API

The app uses `window.speechSynthesis` with `lang: 'nl-NL'`. Key constraints:
- Voice availability varies by browser/OS — always check `speechSynthesis.getVoices()` inside the `onvoiceschanged` callback
- On iOS Safari, `speechSynthesis.speak()` must be called from inside a user gesture handler — silently fails outside a gesture
- `speechSynthesis.cancel()` before each new `speak()` to prevent queuing
- `utterance.rate = 0.75` for Slow; `utterance.rate = 1` for normal Play

---

## 9. HTML Implementation Review

Audit of `nederly.html` at **VERSION 3** against the principles above.

### What is done correctly (confirmed shipped in VERSION 3)

| Area | Detail |
|------|--------|
| **Font: OpenDyslexic** | Loaded via `@font-face` — shipped in VERSION 3 |
| **Line height** | 1.6 on `body` — shipped in VERSION 3 |
| **Letter spacing** | 0.04em on `body` — shipped in VERSION 3 |
| **Helper / IPA text color** | `#6B6B6B` (contrast ~4.9:1, passes WCAG AA) — shipped in VERSION 3 |
| **Slow playback rate** | 0.75× — shipped in VERSION 3 |
| Background color | `#FAF3E0` cream |
| Primary text color | `#1A1A1A` — 15.7:1 contrast |
| Dutch vocab font size | 26px |
| IPA/helper font size | 16px |
| Screen title size | 20px |
| Primary button height | `min-height: 64px` |
| Play button height | `min-height: 48px` |
| Card padding | 24px |
| Screen left/right padding | 40px |
| List item gap | 16px |
| Card border-radius | 12px |
| Single vocab word alignment | Centre on flashcard |
| Tap-to-reveal flashcard | Learner-controlled pacing |
| Minimal pairs | 2-option tap card |
| Color-coded sounds | Consistent accent palette on session screen |

---

### What still needs fixing

| Issue | Current state | Required fix |
|-------|--------------|--------------|
| **Sound guide card density** | Long description text fills cards | Cap description text at 2 lines via `-webkit-line-clamp: 2`; move detail into an expandable "Show more" area |
| No visible category-progress indication | Session screen shows current item only | Add a thin progress bar (see §11) showing position within the finite category set |
| No reflection screen at session end | Session ends abruptly after last item | Add a brief reflection card (see §11) before returning to home |

### New observations (VERSION 3)

| Observation | Action |
|-------------|--------|
| OpenDyslexic + 0.04em letter-spacing combined: confirm no horizontal overflow on 320px viewport (OpenDyslexic glyphs are slightly wider than system-ui) | Test on a 320px-wide viewport; if any vocab word wraps, drop letter-spacing to 0.03em **for the vocab word element only**, keep 0.04em on body |
| OpenDyslexic Bold may not be loaded — only Regular | Add a second `@font-face` block for `OpenDyslexic-Bold.woff2` with `font-weight: bold` so headings/buttons get the proper bold glyph rather than a synthesised one |
| `font-display: swap` causes a brief reflow when OpenDyslexic arrives — acceptable, but ensure no layout depends on exact text width | No change needed; flag for designer |

---

### Exact CSS changes still required

```css
/* 1. Sound guide card description density */
.sound-card-description {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 2. Add bold OpenDyslexic face if not already present */
@font-face {
  font-family: 'OpenDyslexic';
  src: url('OpenDyslexic-Bold.woff2') format('woff2');
  font-weight: bold;
  font-style: normal;
  font-display: swap;
}
```

Pair the line-clamped description with a visible "Show more" toggle.

---

### Alignment decisions confirmed

| Element | Alignment | Verdict |
|---------|-----------|---------|
| Single Dutch vocab word on flashcard | Centre | Acceptable |
| English translation below vocab word | Centre | Acceptable if single word / short phrase; if full sentence → left |
| Dutch word with color-coded sound highlights | Centre | Acceptable — single word |
| Sound guide card description text | Left | Required |
| Nav button labels | Centre | Acceptable — single-word labels |
| Instructions / multi-word body text | Left | Required |

---

## 10. Dyslexia + L2 Acquisition — Evidence Base

Source: [Researcher §4](./researcher.md#4-dyslexia--language-learning--light-touch-200-words). Each finding is translated into one concrete UX implication for Nederly.

| Finding | Source | Concrete UX implication for Nederly |
|---------|--------|-------------------------------------|
| Phonological-processing deficits in L1 dyslexia transfer to L2 — decoding, phonological short-term memory, and rapid automatised naming are affected, not just reading | [S41][S59][S60] | Never present a Dutch word in text-only form. Every word ships with a Play button (§4). Never gate progress on the user being able to read a Dutch string aloud without first hearing it. |
| L2 dyslexia diagnosis is confounded by L2 proficiency — poor reading-test performance in L2 may come from limited proficiency, not dyslexia | [S61] | Do not show "reading speed" or "reading accuracy" metrics. Do not infer learner ability from a typing or reading task in Dutch. No "you read this slowly" or "you misread X" surface text. |
| Listening is also affected — dyslexic adults show reduced/atypical neural responses to spoken words and audiovisual word presentation | [S41][S62] | Audio-first is necessary but not sufficient. Audio screens still need: a replay control with unlimited repeats, a 0.75× slow option, and a visible written form *after* the learner has chosen to see it (tap-to-reveal). Do not assume listening is "the easy half". |
| Adult dyslexics with high L2 motivation show better L2 self-perception — motivation/affect work is well-spent | [S60] | Invest in non-punitive feedback (§6), non-streak engagement (§11), and reflection moments. Avoid any UI that frames the user as deficient. |
| "Language spontaneity deficit" proposed for adult dyslexics in L2 — fluent production under time pressure is disproportionately hard | [S63] | Never put a clock on a free-production task. Listen-and-repeat is fine (target is fixed). Free typing under time pressure is banned. The user must be able to take as long as they want on any production task. |

---

## 11. Engagement Features Without Streaks

The Researcher ([§2.4](./researcher.md#24-gamification--works-but-the-mechanic-matters), [§2.6](./researcher.md#26-short-term-goals--visible-progress-instead-of-streaks)) identifies safer mechanics: progress bars, mastery badges, completion of a **known finite set**, surprise/variety, and short-term goals + reflection ([S42][S43][S48]). Streaks are out (§7). Below: concrete recommendations for Nederly with hex codes and sizes.

### 11.1 Category progress bar

A thin progress bar showing position within the *current finite category* (e.g. "Family words: 6 of 10").

| Property | Value |
|----------|-------|
| Height | 6px |
| Track color | `#E8DFC4` (a 10% darker tint of `#FAF3E0`) |
| Fill color | `#2E6DA4` (Accent Blue) |
| Border radius | 3px |
| Position | Top of session screen, 16px below the screen title |
| Label | "6 of 10" in `#6B6B6B`, 16px, sentence case, left-aligned beside the bar |
| Animation | Width transition 300ms ease-out on advancement |

Why: finite-set completion is the safe mechanic. The user can *see* the end. There is no infinite ladder.

### 11.2 Mastery card at session end

After the last item in a session, show a single card before returning to home.

| Element | Spec |
|---------|------|
| Heading | 20px bold, `#1A1A1A`, sentence case: "Nice session." |
| Body line 1 | 18px, `#1A1A1A`: "You practiced {N} words today." |
| Body line 2 | 18px, `#1A1A1A`: "You've heard {category} {M} times this week." |
| Body line 3 (conditional) | 18px, `#3A7D44` (Success Green): "{word} feels solid now." — shown only when a word has crossed an internal mastery threshold |
| CTA button | 64px height, `#2E6DA4` background, white text, label "Back home" |
| What is *not* shown | No streak count. No "come back tomorrow!". No comparison to other users. No percentages. |

Why: this is *reflection*, not loss-aversion ([S48]). It tells the learner what they did, not what they'll lose by stopping.

### 11.3 Mastery badges (finite set)

A small inline badge appears next to a word the *first* time it crosses the mastery threshold (internal: ≥80% pronunciation score across 3 separate sessions).

| Property | Value |
|----------|-------|
| Shape | Circle, 20px diameter |
| Fill | `#3A7D44` (Success Green) |
| Icon inside | Single white checkmark, 12px |
| Position | 8px to the right of the vocab word, vertically centred |
| Persistence | Stays on the word forever — never removed, never decayed (no anxiety on time-away) |
| Tooltip on tap | "Mastered on {date}" in 16px `#6B6B6B` |

Why: badges that **cannot be lost** are safe; badges that decay reintroduce loss-aversion.

### 11.4 Daily prompt picker (variety, not fixed tiles)

The home screen presents 3 category buttons, but the *which 3* rotates daily from the user's known categories. A small "Pick another" link below offers a different shuffle.

| Property | Value |
|----------|-------|
| Category button height | 64px |
| Category button background | `#FAF3E0` with a 1px `#E8DFC4` border |
| Category button label | 18px, `#1A1A1A`, sentence case |
| "Pick another" link | 16px, `#2E6DA4`, underlined, centred, 24px below the last category button |
| Rotation rule | Stable within a single day; reshuffles at the user's local midnight |

Why: surprise/variety is one of the safer mechanics ([§2.4](./researcher.md#24-gamification--works-but-the-mechanic-matters), [S42][S43]). Fixed tiles in the same order every day become a chore.

### 11.5 Short-term goal nudge (opt-in only)

A single soft prompt at session start, only on every third session: "Want to focus on one sound today?" with 3 sound-category chips below. If tapped, the session weights toward that sound. If ignored, normal session proceeds.

| Property | Value |
|----------|-------|
| Prompt text | 18px, `#1A1A1A`, sentence case |
| Chip height | 48px |
| Chip background | `#FAF3E0` |
| Chip border | 1px `#2E6DA4` |
| Chip label | 18px, `#2E6DA4` |
| Dismiss | Tap anywhere outside the chips — no explicit "no thanks" button needed |
| Frequency | Every third session, capped at once per day |

Why: short-term goals + reflection raise motivation in adult ESL ([S48]). Opt-in framing prevents it becoming a daily checklist.

### 11.6 What we explicitly do not build

| Mechanic | Why not |
|----------|---------|
| Day streak counter | Loss-aversion; shame on break ([S44][S45]) |
| Hearts / lives | Same mechanism; punishes mistakes |
| XP / levels | Infinite ladder — no completion feel; invites comparison |
| Leaderboards | Comparison stress; off-mission for a private practice tool |
| Push notifications "you'll lose your streak" | Direct loss-aversion ([S44][S45]) |
| Time-of-day reminders that escalate | Anxiety-inducing |
| Percentage scores at session end | Invites comparison; punishes bad days |

---

*End of dyslexia_expert.md. Hand off to: Designer (§§1–3, §8, §11 for UI specs); Phonetics (§4, §6 for audio + per-phoneme feedback design); implementation pass (§9 fixes still required).*
