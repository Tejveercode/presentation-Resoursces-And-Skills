---
name: design-system
description: >
  Presentation design intelligence: builds the internal Presentation Design
  Brief (audience, purpose, tone, visual direction, layout system, typography,
  semantic color system, contrast, density, animation policy) from the audited
  content + user preferences, and enforces the anti-AI-slop prohibited-pattern
  rules before and after deck generation.
---

# Design System — Presentation Design Intelligence

## Purpose

Make every deck intentionally designed, not template-stamped, and prevent
AI-look decoration. Facts first: design never outranks accuracy, readability,
contrast, accessibility, or teacher requirements.

## 1. Presentation Design Brief (create BEFORE slide generation)

`_audit/<project>/design_brief.md` — must state, each with a one-line rationale
tied to the Fact Sheet:

- **Audience** — who evaluates/attends; expert level; projection context.
- **Purpose** — inform/evaluate/defend; decision the audience must be able to make.
- **Tone** — academic/technical register; restrained, evidence-forward.
- **Visual direction** — flat, grid-disciplined, whitespace-forward; prohibited
  patterns listed (see §4).
- **Layout system** — one grid (13.333×7.5 canvas, fixed margins), consistent
  title/rule/content zones; per-slide content forms vary, chrome does not.
- **Typography** — one heading face + one body face (universally available);
  title 40pt, section heading 28pt, body 16pt, small 12pt, caption 11pt; no
  body text below 12pt.
- **Color system** — semantic roles only (see §2); contrast ≥ 4.5:1 for body
  text on background; color never the sole carrier of meaning.
- **Density** — max ~5 bullets/slide, one idea per slide; neither overcrowded
  nor decorative-empty.
- **Animation policy** — static deck (editable PPTX); no animations required.
- **User preferences** — captured verbatim in `_audit/<project>/design_prefs.json`
  (theme, light/dark, creativity level, colors, dislikes, examples) with source
  flags (user|agent-default).

## 2. Color intelligence (semantic roles, never random)

| Role | Use | Example |
|---|---|---|
| background | slide surface | white |
| primary | titles, section bands, table headers | deep academic blue |
| accent | thin rules, key highlights (sparingly) | teal |
| text (ink) | body content | near-black |
| muted | captions, footers, edge labels | grey |
| neutral | panels/alternation | light blue-grey |
| success | IMPLEMENTED badges | green |
| warning | PARTIAL/PLANNED badges | amber |
| error | UNKNOWN/NOT VERIFIED | red |

Rules: ≤ 1 accent color in active use; badges are the only filled color blocks
besides the section band and table header; projected-screen check — darken any
color that fails contrast at distance; never select colors by mood alone.

## 3. Typography & layout rules

- Reading order: title → badge (status, when present) → content → footer.
- Line length: body text boxes ≤ ~90 characters/line; avoid full-width slabs.
- Align on the grid: consistent margins (0.6" L/R), title baseline consistent,
  footer bottom-aligned on every content slide.
- Balance: no slide may be > 80% filled or < 30% filled (excluding section/title).
- Consistency: identical title placement and rule across content slides;
  diagram canvas uses the same margins.

## 4. Anti-AI-slop prohibited patterns (deterministic checks in `check_deck.py`)

Banned: meaningless gradients; glow effects; excessive glassmorphism; decorative
blobs; generic purple/blue "AI aesthetic"; repetitive card grids serving no
comparison; meaningless giant numbers; decorative icon rows; fake dashboards;
unnecessary 3D; stock-image filler; random arrows; decorative diagrams; heavy
shadows; unnecessary animations; any visual element that fails the question
**"What information does this communicate?"**.

Rejection rule: if a proposed visual communicates nothing informational, remove
it. Anti-slop ≠ boring: creativity is permitted where it carries structure —
vary slide forms by content type (architecture→diagram, workflow→process
diagram, comparison→two-column/table, results→chart, challenge→problem/solution,
prototype→real screenshot). One form per content need; never the same card grid
everywhere.

## 5. UX cognitive path (every slide)

Each slide must answer, in visual order: Where am I (phase/section) → main point
(title) → evidence (content/badges/figures) → why it matters (speaker notes).
Slides requiring the audience to decode structure fail Design QA.

## 6. Preference precedence (binding)

User preferences influence the design system but NEVER override: factual
accuracy, readability, accessibility/contrast, teacher rubric requirements,
technical correctness. If a preference conflicts with one of these, the
preference loses and the conflict is noted in the design brief.
