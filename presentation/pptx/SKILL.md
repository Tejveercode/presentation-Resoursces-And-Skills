---
name: pptx-engine
description: >
  PRIMARY PPTX GENERATION ENGINE (python-pptx). Builds a native, fully
  editable academic PowerPoint from a JSON deck spec: editable text, tables,
  native-shape diagrams with connectors, speaker notes, status badges, slide
  numbering, and a consistent academic theme. Includes render + visual-QA
  scripts (LibreOffice headless). The only presentation engine in this toolbox.
---

# PPTX Engine (python-pptx) — PRIMARY

## Role

The single presentation engine of the toolbox. Converts a deck-spec JSON (from
`presentation/presentation-skill/`) into a real `.pptx` with everything editable:
text in text frames, tables as PowerPoint tables, diagrams as native shapes +
connectors, speaker notes per slide. Never rasterize whole slides; never output
HTML decks; never build a second engine.

## Dependencies

- Python 3.8+ with `python-pptx` (1.0.x) — `pip3 install python-pptx`
- Rendering / visual QA (optional): LibreOffice (`soffice`) + poppler
  (`pdftoppm`). If absent, the render script states exactly what is missing.
- Fonts: theme uses universally available fonts (Calibri / Consolas) so no font
  redistribution or network is required.

## Theme

`templates/academic_theme.json` — one design system: ink/primary/accent palette,
font sizes, margins, footer policy. All slides draw from these tokens; no
per-deck improvisation. Restrained academic style: clear hierarchy, whitespace,
thin rules, no decorative clutter.

## Deck spec (JSON)

```json
{
  "project": "Project Name",
  "slides": [
    {"type": "title", "title": "...", "subtitle": "...", "meta": ["Course", "Date"], "notes": "..."},
    {"type": "section", "phase": "PHASE 1 — FOUNDATION", "title": "...", "notes": "..."},
    {"type": "bullets", "title": "...", "bullets": [{"text": "...", "level": 0}], "badge": "IMPLEMENTED (verified)", "notes": "..."},
    {"type": "two_column", "title": "...", "left_heading": "...", "left_bullets": ["..."], "right_heading": "...", "right_bullets": ["..."], "notes": "..."},
    {"type": "table", "title": "...", "columns": ["Layer", "Technology"], "rows": [["Frontend", "React 19"]], "col_widths": [3.0, 6.0], "notes": "..."},
    {"type": "image", "title": "...", "image": "screenshots/home.png", "caption": "Actual UI (verified)", "badge": "VERIFIED SCREENSHOT", "notes": "..."},
    {"type": "diagram", "title": "...", "nodes": [{"id":"fe","label":"Frontend","x":0.7,"y":2.2,"w":2.6,"h":1.0,"kind":"rounded"}], "edges": [{"from":"fe","to":"db","label":"SQL"}], "notes": "..."}
  ]
}
```

Coordinates are inches on a 13.333 x 7.5 canvas. `badge` (optional) renders a
status label — use exactly the ledger wording, e.g. "IMPLEMENTED (verified)",
"Partially Implemented", "Planned / Future Roadmap".

## Build

```
python3 presentation/pptx/scripts/build_deck.py deck.json -o out.pptx \
    [-t presentation/pptx/templates/academic_theme.json]
```

## Render + visual QA loop

```
python3 presentation/pptx/scripts/render_deck.py out.pptx -o render/
```

Then INSPECT every PNG: overflow, clipping, overlap, contrast, spacing,
alignment, numbering, diagram legibility, empty space, overcrowding. Fix the
spec, rebuild, re-render — repeat until acceptable. A successfully created file
is NOT a finished deck.

## Guarantees & rules

- Text, tables, shapes, connectors remain native/editable (verified by tests).
- Speaker notes are written whenever `notes` is present.
- Diagrams come only from `visualization/scientific-schematics/` derivation
  rules (ledger-backed components).
- One engine only. No HTML. No full-slide images. No fabricated screenshots.
