# Skill Index

Catalog of skills available to the presentation-generation agent, grouped by
category, with the audit classification of every candidate reviewed
(`_incoming_skills_zips/`). A skill is "available" only when listed here with
status **Installed**.

## Installed skills

| Category | Skill | Path | Purpose | Status |
|---|---|---|---|---|
| Orchestration | **Project Presentation Director** | `orchestration/project-presentation-director/` | Coordinates the full pipeline (audit → evidence → research → rubric mapping → deck → QA); owns the anti-hallucination policy; one presentation engine only | **Installed** |
| Research | **Project Audit & Evidence Ledger** | `research/project-audit/` | Repository audit; Project Fact Sheet; Evidence Ledger with statuses IMPLEMENTED / PARTIALLY IMPLEMENTED / PLANNED / UNKNOWN-NOT FOUND; ledger validator script | **Installed** (validator selftest + reject-path tested) |
| Research | **Research Lookup** | `research/research-lookup/` | Domain research, literature discovery, honest gap framing; SOURCE FOUND vs SOURCE VERIFIED discipline | **Installed** |
| Research | **Citation Management** | `research/citation-management/` | Source records, claim→source traceability, bibliography from SOURCE VERIFIED only; `build_bibliography.py` with `--strict` rejection of unverified sources | **Installed** (selftest + strict-rejection tested) |
| Presentation | **Presentation Architecture** | `presentation/presentation-skill/` | Rubric→deck mapping (Phase 1/2/3, ~12–14 slides), claim-wording separation (PROJECT FACT / RESEARCH / INTERPRETATION / FUTURE WORK), per-slide evidence requirements | **Installed** |
| Presentation | **PPTX Engine (PRIMARY)** | `presentation/pptx/` | python-pptx generation: editable text, tables, native shapes + connectors, speaker notes, status badges, slide numbering, academic theme; `build_deck.py`; render/QA script | **Installed** (engine test suite passes: 7/7 slide types, editability verified) |
| Visualization | **Scientific Schematics** | `visualization/scientific-schematics/` | Ledger-derived native-shape diagrams (architecture, block, data-flow, workflow, setup) | **Installed** (diagram building tested via engine) |
| Presentation | **Humanizer** (imported) | `presentation/humanizer/` | Controlled final language pass; never changes facts, status, or citations | **Installed** (MIT; provenance in `PROVENANCE.md`) |

## Optional (not installed)

| Item | Notes |
|---|---|
| Exa / You.com MCP literature discovery | External API services; acquire only if runtime permits |
| Screenshot/evidence capture helper | To be authored when a target-project runtime is available |

## External reference (NOT imported — do not copy)

| Candidate | Source | License | Reason |
|---|---|---|---|
| html-ppt-skill | `lewislulu/html-ppt-skill` | MIT | HTML output ≠ editable PPTX; its render/QA pattern is the reference; keep outside to avoid a second engine |
| claude-plugins-official | `anthropics/claude-plugins-official` | Apache-2.0 (repo) | Plugin catalog, per-plugin licenses vary; acquisition directory only |
| guizang-ppt-skill | `op7418/guizang-ppt-skill` | **AGPL-3.0** | Copyleft — must never be copied into this repository |

## Rejected (do not use)

| Candidate | Reason |
|---|---|
| Presentation-master (`hyperoslo/Presentation`) | Deprecated iOS UI library; wrong domain despite the name |
| taste-skill (`leonxlnx/taste-skill`) | Frontend web-UI design (12 sub-skills); wrong domain; redundant design system |

## Unverified (do not import)

| Item | Reason |
|---|---|
| Google-Fonts sub-licenses inside html-ppt-skill | Font license files not bundled in ZIP |
| guizang-ppt-skill bundled image assets | Individual asset provenance undocumented |
| Anthropic `pptx` document skill | Not present in the ZIP staging area; not audited (engine authored in-house instead) |

## Staging area

`_incoming_skills_zips/` retains all six candidate ZIPs as source/reference
material. Nothing from it is installed except the verified-MIT humanizer
(`SKILL.md` + `LICENSE`, byte-identical, provenance recorded).
