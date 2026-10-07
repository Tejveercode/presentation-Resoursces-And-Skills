# Skill Index

Catalog of skills available to the presentation-generation agent, grouped by category.
Only skills actually present in this repository are listed; folder names are
placeholders until a skill's `SKILL.md` is populated. **No external skills have been
installed yet.**

| Category | Skill | Status |
|---|---|---|
| Orchestration | **Project Presentation Director** — coordinates the end-to-end flow: project analysis, research, presentation design, PPTX generation, and quality assurance. | Placeholder (SKILL.md pending) |
| Presentation | `presentation/presentation-skill/` | Empty placeholder — content pending |
| Presentation | `presentation/pptx/` | Empty placeholder — content pending |
| Research | `research/research-lookup/` | Empty placeholder — content pending |
| Research | `research/citation-management/` | Empty placeholder — content pending |
| Visualization | `visualization/scientific-schematics/` | Empty placeholder — content pending |

## Categories

- **`orchestration/` — Coordinator skills.** Skills that plan and route work across the
  other categories, deciding which resource to invoke at each stage.
- **`presentation/` — Slide content & deck generation.** Resources covering
  presentation structure, design, and PowerPoint file generation.
- **`research/` — Evidence gathering & sourcing.** Resources for looking up material
  and managing citations/reference accuracy.
- **`visualization/` — Technical diagrams.** Resources for producing scientific and
  schematic figures used inside slides.

## Conventions

- Each installed skill gets one folder under its category with a `SKILL.md` that
  documents what it does and **when** the agent should use it.
- Empty skill directories keep a `.gitkeep` until their skill content is installed.
- This index stays authoritative: a skill is "available" only once it is listed here
  with a status of **Installed**.
