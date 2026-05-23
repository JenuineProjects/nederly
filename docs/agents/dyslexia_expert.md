# Nederly — Dyslexia Expert Agent Report
*Focus: professional visual design, phonetic display, dyslexia-optimised UX*
*Netherlands Dutch | A0 beginner | Dyslexic adult English speaker*
*Generated: 2026-05-22*

---

## 1. Typography

Primary font: **OpenDyslexic** — already loaded in `index.html` via `@font-face`. Retain as-is.
Fallback stack: `system-ui, -apple-system, sans-serif` — correct.

### Type Scale

| Role | Element | Size | Line Height | Letter Spacing |
|------|---------|------|-------------|----------------|
| Card word (Dutch) | `.card-word` | 32px | 48px | 0.02em |
| Section heading | `.lesson-detail-title`, `h2` | 22px | 32px | 0.01em |
| Body / UI labels | `body`, `.card-english` | 18px | 29px | 0.04em |
| Secondary / meta | `.card-ipa`, `.card-tap`, `.session-type` | 16px | 26px | 0.03em |
| Tiny / uppercase labels | `.section-label`, `.sound-section-heading` | 13px | 20px | 0.08em |
| IPA / respelling | `.card-phonetic` (new token) | 15px | 24px | 0.03em |

**Current issue:** `.card-word` is 26px — upgrade to 32px. Line height 40px → 48px.
The Dutch target word is the primary cognitive object on every flashcard; it must dominate the visual hierarchy.

### Rules
- Never set text below 13px anywhere in the app (Researcher §4, §6)
- Uppercase labels only for short category names (≤ 20 characters), never for body copy (Researcher §4)
- OpenDyslexic's weighted bottom on each glyph means line-height must be at least 1.5× font-size — current `line-height: 1.6` on body is correct, preserve it
- Do not italicise. OpenDyslexic has no true italic variant; browsers synthesise a slant that degrades readability for dyslexic users

---

## 2. Color & Contrast

### Background and Text

| Token | Hex | Role |
|-------|-----|------|
| `--bg` | `#F7F2E8` | Page background (warmer, lower blue-light than pure white; current `#FAF3E0` is acceptable — slight refinement) |
| `--surface` | `#FFFFFF` | Card surfaces, modal panels |
| `--surface-raised` | `#F0EBE0` | Hover states on nav buttons |
| `--text-primary` | `#1A1A1A` | Body text — current value, keep |
| `--text-secondary` | `#5C5C5C` | Meta labels, secondary info — upgrade from `#6B6B6B` for better contrast on white surfaces |
| `--border` | `#D4CBBA` | Card borders — slightly darker than current `#E0D8C8` for crisper definition on white cards |

**Contrast check — text-primary on bg:**
`#1A1A1A` on `#F7F2E8` → contrast ratio ≈ 17.5:1 — passes WCAG AAA (≥ 7:1). (Researcher §6)

**Contrast check — text-secondary on surface:**
`#5C5C5C` on `#FFFFFF` → contrast ratio ≈ 7.7:1 — passes WCAG AA Large and AA Normal.
Current `#6B6B6B` on `#FAF3E0` → ≈ 5.5:1 — marginal for 16px text; `#5C5C5C` closes the gap.

### Accent Palette

Professional, calm — Babbel-register, not Duolingo-bright. (Researcher §6)

| Token | Hex | Role |
|-------|-----|------|
| `--accent-blue` | `#2E6DA4` | Primary CTA, links, active states — current value, keep |
| `--accent-blue-light` | `#E8F0F9` | Blue chip backgrounds, info banners |
| `--accent-green` | `#2F7A3B` | Success / "got it" button — darken from `#3A7D44` for better contrast on white |
| `--accent-green-light` | `#EBF5EC` | Success card background tint |
| `--accent-red` | `#C0392B` | Error / "missed" state — darken from `#D94F3D` for contrast |
| `--accent-red-light` | `#FDECEA` | Error card background tint |
| `--accent-amber` | `#B35C00` | Warning / star audio-required flag — replaces `#E07B39` which is too bright |
| `--accent-amber-light` | `#FDF3E6` | Warning chip background |
| `--accent-purple` | `#5C3F8F` | Hint / phonetic accent — darken from `#6B4FA0` for contrast |
| `--accent-purple-light` | `#F0EBF9` | Phonetic chip background |

**Contrast check — accent-blue on white surface:**
`#2E6DA4` on `#FFFFFF` → ≈ 5.5:1 — passes WCAG AA for text ≥ 18px and for UI components.

**Contrast check — accent-green on surface:**
`#2F7A3B` on `#FFFFFF` → ≈ 6.4:1 — passes WCAG AA.
`#3A7D44` on `#FAF3E0` → ≈ 5.0:1 — borderline; `#2F7A3B` on white cards is safer.

### States

| State | Background | Border | Text |
|-------|-----------|--------|------|
| Success | `#EBF5EC` | `#2F7A3B` 2px | `#1A1A1A` |
| Error | `#FDECEA` | `#C0392B` 2px | `#1A1A1A` |
| Warning / audio-required | `#FDF3E6` | `#B35C00` 1px | `#1A1A1A` |
| Disabled | `#F0EBE0` | `#D4CBBA` 1px | `#9A9A9A` |
| Focused (keyboard/tap) | same bg | `#2E6DA4` 3px | same text |

**Principle:** state colour lives on the border and tinted background — never on the body text. This preserves reading contrast regardless of state. (Researcher §6)

---

## 3. Layout Principles

### Screen Density

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max items per list screen | 6 visible without scrolling | Cognitive load limit for working memory (Researcher §4) |
| Max words on a single flashcard | 1 Dutch word + 1 English translation | One concept per card |
| Max phonetic lines per card | 2 lines (respelling + audio button) | Prevent symbol overload (Researcher §7) |
| Screen side padding | 24px | Prevents text touching the viewport edge |
| Card internal padding | 24px all sides | Breathing room around text |
| Gap between stacked elements | 16px standard, 24px between major sections | Vertical rhythm |

**Current `.screen` padding is `24px 40px`** — the 40px horizontal is generous. Keep it: it tightens the reading line length and reduces the visual span a dyslexic reader must track. (Researcher §4)

### Touch Targets

| Element | Min Height | Min Width |
|---------|-----------|-----------|
| All tappable buttons | 56px | 56px |
| Nav category buttons (`.nav-btn`) | 64px | 100% |
| Play/slow audio buttons | 56px | 56px |
| Outcome buttons (got/missed) | 56px | 48% of row |
| Back button | 44px tap area minimum | 44px |

**Current `.play-btn` min-height is 48px — upgrade to 56px.** All other primary buttons already meet 64px.

### Alignment
- Single-column layout throughout — no side-by-side content except the minimal pairs exercise
- Left-align all body text; centre-align only the card word and its phonetic hint
- Consistent left margin for list items: 16px indent + bullet (already correct in `.lesson-section-list`)
- Never right-align text

---

## 4. Audio-First Design

Dyslexic learners rely on multisensory delivery — audio + text together, not as alternatives. (Researcher §4, §7)

### Audio Button Placement

```
[ Dutch word — 32px centred                    ]
[ respelling — 15px centred, muted             ]
[ Play  |  Slow ]  <- always visible           ]
[ English meaning — 18px                       ]
```

- Audio controls are **always visible on the front of the card** — before reveal, not after
- **Do not gate audio behind a tap-to-reveal interaction.** The user should be able to hear the word before attempting to recall its meaning
- Two buttons: normal speed and 0.75x slow; label them with icons + short text ("Play" / "Slow") — icon alone is ambiguous for new users

### Auto-Play Policy
- **First card of a session:** auto-play the audio once on load — gives an immediate audio anchor
- **Subsequent cards:** tap-to-play only — auto-play on every card becomes fatiguing
- No auto-advance based on audio completion — user controls pacing

### Repeat Control
- Single tap replays at normal speed
- Slow button: always present; 0.75x rate via Web Audio API `playbackRate`
- No limit on replays — remove any replay cap if one exists

---

## 5. Exercise Design

Graded for a dyslexic A0 beginner. (Researcher §4, §7)

| Exercise Type | Grade | Reason |
|--------------|-------|--------|
| Audio flashcard (hear → recall meaning) | **Favour** | Multisensory, low reading load, audio-first |
| Minimal pairs (choose which word you heard) | **Favour** | Trains phoneme discrimination; closed response reduces spelling burden |
| Tap-to-reveal self-assessment | **Favour** | Learner controls pacing; no time pressure |
| Matching (word → translation drag) | **Neutral** | Useful for vocabulary but requires visual scanning of a dense grid; keep pairs to max 4 at a time |
| Fill-in-the-blank typing | **Avoid** | Spelling is the primary dyslexia deficit; typing exercises produce shame and avoidance (Researcher §4) |
| Dictation / write what you hear | **Avoid** | High spelling load; evidence shows disproportionate difficulty for dyslexic FL learners (Researcher §4) |
| Multiple choice (4 options) | **Neutral** | Acceptable if font is large and options are widely spaced; avoid if options look visually similar |
| Timed exercises | **Avoid** | Time pressure significantly worsens outcomes for dyslexic learners (Researcher §4) |
| Translation into Dutch (production) | **Avoid at A0** | Productive recall requires orthographic knowledge not yet built; introduce at A1+ |

---

## 6. Feedback Design

**Core principle:** feedback names what happened, not what the learner is. No judgment language. (Researcher §4)

### Correct Response
- Green border on card: `#2F7A3B` 2px
- Background tint: `#EBF5EC`
- Label: "Got it" (current wording is fine — short, neutral)
- No celebratory animation, no sound effects — these disrupt cognitive focus
- Transition immediately to next card (300ms fade)

### Incorrect / Missed Response
- Amber border (not red): `#B35C00` 2px — amber is less punitive than red (Researcher §6)
- Background tint: `#FDF3E6`
- Label: "Practice again" — not "Wrong" or "Incorrect"
- Show the correct answer and replay audio automatically once on miss — the multisensory correction loop
- The missed card re-enters the deck at position +2 (not the end) to provide near-spaced review

### Pronunciation Feedback (future audio analysis)
- If scoring pronunciation, show a simple waveform match indicator — avoid numeric scores or letter grades
- Label feedback as "Close" / "Keep practising" — never "Incorrect pronunciation"
- Always replay the native speaker recording after any pronunciation attempt

### End-of-Session Feedback
- Show percentage correct as a large number (existing `.pct` at 64px — correct)
- Below it: "You practised X words" — factual, not evaluative
- No star ratings, no letter grades, no "You need to do better" language

---

## 7. Anti-Patterns — Banned

These are prohibited in Nederly regardless of general industry use. (Researcher §2, §4)

| Anti-Pattern | Why Banned |
|-------------|-----------|
| **Streaks** | Punish gaps in practice; create anxiety that causes learners to quit (Researcher §2 notes enjoyment sustains engagement — streaks undermine it) |
| **Lives / hearts** | Progress-loss mechanics are punitive and particularly harmful for learners who already struggle (Researcher §4) |
| **Countdown timers** | Time pressure significantly worsens dyslexic performance (Researcher §4) |
| **Session timers** | Same — even ambient timers create urgency that degrades recall |
| **ALL CAPS body text** | OpenDyslexic's weighted characters rely on distinct ascenders/descenders that all-caps eliminates; readability collapses |
| **Walls of text** | Working memory overload; dyslexic learners cannot hold long text and process phonetics simultaneously (Researcher §4) |
| **Score rankings / leaderboards** | Social comparison harms motivation for struggling learners |
| **Pop-up rewards with sound** | Interrupt cognitive state; reward extrinsic not intrinsic motivation |
| **Micro-animations on every interaction** | Cumulative distraction; reserve animation for state changes only |

---

## 8. Phonetic Display Styling

### Decision: Respelling, Not IPA

Use English respelling only. Rationale: (Researcher §7)
- IPA requires learning a second symbol set — high overhead for a beginner
- The user's own lesson notes use English approximations (e.g. "ow", "aaa") with no IPA
- Dyslexic learners perform better with plain-language descriptions than symbol-heavy notation (Researcher §7, IDA source)
- The star system from the Sound Reference Guide (internal) covers IPA's accuracy role by flagging audio-required sounds

### Card Layout — Exact Position

```
+-----------------------------------------+
|                                         |
|   [Dutch word — 32px, centred]          |
|   [respelling chip — 15px, centred]     |
|                                         |
|   [ Play ]   [ Slow ]                   |
|                                         |
|   - - - - - (tap to reveal) - - - - -  |
|                                         |
|   [English meaning — 18px, centred]     |
|   [example hint — 16px, muted]          |
|                                         |
+-----------------------------------------+
```

Phonetic hint is **always visible above the reveal line** — the user should not have to flip the card to see how the word is pronounced. Audio and respelling are pre-reveal tools, not post-reveal rewards.

### CSS Tokens for Phonetic Display

```css
/* Phonetic chip — the respelling displayed below the Dutch word */
.card-phonetic {
  font-size: 15px;
  line-height: 24px;
  letter-spacing: 0.03em;
  color: #5C3F8F;              /* --accent-purple, passes 5.1:1 on white */
  background: #F0EBF9;         /* --accent-purple-light */
  border-radius: 6px;
  padding: 2px 10px;
  display: inline-block;
  font-style: normal;          /* never italic */
  text-align: center;
  max-width: 100%;
}

/* star audio-required badge */
.phonetic-star {
  color: #B35C00;              /* --accent-amber */
  font-size: 14px;
  margin-left: 4px;
  vertical-align: middle;
}

/* Dutch word on card — upgrade from current 26px */
.card-word {
  font-size: 32px;
  line-height: 48px;
  letter-spacing: 0.02em;
  text-align: center;
  color: #1A1A1A;
}

/* English meaning — shown after reveal */
.card-english {
  font-size: 18px;
  line-height: 29px;
  color: #1A1A1A;
  text-align: center;
}

/* Existing .card-ipa rename to .card-phonetic; remove current #6B6B6B grey */
/* Grey fails to distinguish the phonetic hint from secondary metadata */
```

### Contrast Verification

| Token | Foreground | Background | Ratio | Pass |
|-------|-----------|-----------|-------|------|
| `.card-phonetic` text | `#5C3F8F` | `#F0EBF9` | 5.1:1 | AA |
| `.phonetic-star` | `#B35C00` | `#F0EBF9` | 4.7:1 | AA Large |
| `.card-word` | `#1A1A1A` | `#FFFFFF` (card surface) | 19:1 | AAA |

### Preventing Phonetic Overwhelm

- **Size ratio rule:** phonetic text (15px) is never more than 47% of the Dutch word size (32px) — the word always visually dominates
- **Colour isolation:** phonetic chip uses a distinct purple chip background — it reads as a separate information layer, not competing with the word
- **One line maximum:** if the respelling is longer than approximately 16 characters, truncate with an expand-tap; do not wrap to two lines
- **Hidden by default? No.** Research shows that hiding phonetic hints behind a tap-to-reveal creates extra steps for learners who need them most (Researcher §7). The hint is small and chipped enough that it does not overwhelm confident readers, while remaining immediately accessible for those who need it.
- **IPA as secondary option:** if IPA is added later, render it inside the chip in parentheses after the respelling at 13px, making it subordinate to the respelling

---

## 9. Professional Polish Checklist

Concrete visual improvements referenced against Researcher §6 (Babbel/Duolingo design patterns). Each item maps to the current `index.html` CSS.

### Cards

| Item | Current | Target |
|------|---------|--------|
| Card background | `#FAF3E0` (same as page) | `#FFFFFF` — cards must read as raised surfaces distinct from the page |
| Card border | `2px solid #E0D8C8` | `1px solid #D4CBBA` + `box-shadow: 0 2px 8px rgba(0,0,0,0.08)` |
| Card border-radius | `12px` | `16px` — rounder feels more approachable (Researcher §6) |
| Card min-height | `200px` | `220px` — more breathing room |
| Card padding | `24px` | `28px 24px` — extra vertical gives text more air |

```css
.card {
  background: #FFFFFF;
  border: 1px solid #D4CBBA;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  padding: 28px 24px;
  min-height: 220px;
}
.card.revealed {
  border-color: #2E6DA4;
  box-shadow: 0 2px 12px rgba(46, 109, 164, 0.15);
}
```

### Nav Buttons

| Item | Current | Target |
|------|---------|--------|
| Background | `#FAF3E0` (page bg) | `#FFFFFF` |
| Border | `1px solid #E0D8C8` | `1px solid #D4CBBA` |
| Shadow | none | `0 1px 4px rgba(0,0,0,0.06)` |
| Border-radius | `8px` | `12px` |
| Hover | `#F0E8D0` | `#F0EBF9` (subtle blue-purple tint — consistent with accent) |

### Buttons

| Item | Current | Target |
|------|---------|--------|
| Primary (`.start-btn`, `.home-btn`) border-radius | `8px` | `12px` |
| Primary button shadow | none | `0 2px 6px rgba(46,109,164,0.25)` |
| Play button padding | `8px 16px` | `10px 20px` — fatter tap zone |
| Got button (`.got-btn`) radius | `8px` | `12px` |
| Missed button (`.missed-btn`) radius | `8px` | `12px` |
| Disabled state | `background: #A0A0A0` | `background: #D4CBBA; color: #9A9A9A` — less harsh |

### Spacing Rhythm

All spacing should be multiples of 8px. Current `gap: 6px` in `.dots` and `gap: 6px` in `.sound-card` break the rhythm — upgrade to 8px.

| Token | Value |
|-------|-------|
| `--space-xs` | 4px |
| `--space-sm` | 8px |
| `--space-md` | 16px |
| `--space-lg` | 24px |
| `--space-xl` | 40px |

### Color Consistency Audit

| Current inconsistency | Fix |
|----------------------|-----|
| `.pair-word-a` uses `#E07B39` (orange) for one word | Change to `#1A1A1A` — colour-coding two words in a pair requires the user to learn a colour key; remove it |
| `.pair-word-b` uses `#2E6DA4` (blue) for other word | Change to `#1A1A1A` — same reason |
| `.sound-star` uses `#E07B39` | Change to `#B35C00` — consistent with `--accent-amber` |
| `.card-ipa` uses `#6B6B6B` | Refactor to `.card-phonetic` with purple chip styling (section 8) |
| `.progress-fill` uses `#2E6DA4` (blue) | Keep — blue progress is consistent with accent-blue |
| `.dot.done` uses `#3A7D44` | Update to `#2F7A3B` — consistent with `--accent-green` |

### Icon Use
- Use text + icon together on all audio buttons: "Play" and "Slow" (SVG icons or Unicode symbols paired with labels)
- Back button: use left arrow not angle bracket — more universally readable
- Do not use icons as the sole affordance for any action — always pair with a text label (Researcher §6)
- No decorative illustrations — Babbel-register is clean and text-forward, not character-mascot-heavy

### Header

```css
.header {
  background: #FFFFFF;
  border-bottom: 1px solid #D4CBBA;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  padding: 14px 20px;
}
```

Current header background matches the page (`#FAF3E0`) — it does not visually separate from the content. White header with a subtle shadow creates a clear navigation layer. (Researcher §6)

---

## 10. Nederly-Specific Recommendations

### Cold-Start UX (First Launch)

The first screen a new user sees sets trust permanently. Babbel's onboarding research shows first-impression polish directly affects retention. (Researcher §6)

**Recommended first screen structure:**

```
+-----------------------------------------+
|  Nederly                                |  <- header, white bg
+-----------------------------------------+
|                                         |
|  [Lesson 1: Dutch Sounds]               |  <- card, white surface, shadow
|  [Lesson 2: Cafe]                       |
|                                         |
|  [Dutch Sound Reference]                |  <- secondary card, distinct style
|                                         |
|  [My Progress]                          |  <- text-btn, tertiary
|                                         |
+-----------------------------------------+
```

- **No onboarding modal.** The first action is immediate — a card, tappable, obvious
- Label each lesson card with the topic name AND a one-line summary (e.g. "Lesson 1 — Sounds and greetings") — context reduces the "what is this?" cognitive cost
- Show a subtle progress indicator on each lesson card only if the user has started it — do not show empty progress bars on first launch (empty bars feel like failure before you have begun)

### First Screen Feel
- Background: `#F7F2E8` — warm, not clinical; signals a calm learning environment
- Cards: `#FFFFFF` with `box-shadow: 0 2px 8px rgba(0,0,0,0.08)` — visibly elevated, clickable
- One clear primary action per screen — never two equally weighted CTAs competing
- No placeholder text in empty states that apologises — instead, use a neutral instruction ("Start a lesson above to track your progress")
- The app title "Nederly" in the header should be set at 22px, font-weight 700 — currently 20px/600, upgrade for presence
- First-time hint: one tooltip on the first flashcard only — "Tap to reveal the meaning" — dismissed on first tap, never shown again

### Navigation Predictability (Researcher §6)
- Back button: always top-left, always visible, always does the same thing (go up one level)
- No swipe-to-navigate — swipe gestures are not discoverable and conflict with scroll
- Progress dots (`.dots`) show current position within a session — retain them, they are a good implementation of "where am I?" feedback
- Session complete screen: single large "Home" button — do not offer multiple exit options that require a decision after a cognitive workout

---

*End of Dyslexia Expert Report*
*Cite this document as: Nederly Dyslexia Expert Agent, 2026-05-22*
