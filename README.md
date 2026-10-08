# presentation-Resources-And-Skills

Resource and skill repository for an AI agent that takes an **existing software
project repository** and produces a professional, **fully editable academic
PowerPoint** aligned with a teacher's Phase 1 / Phase 2 / Phase 3 rubric.

This repository contains **skills and resources only** — no application code.

## Orchestration authority

`orchestration/project-presentation-director/` is the single orchestrator. It
defines the mandatory pipeline (Repository → Audit → Evidence Ledger → Research
→ Rubric Mapping → Deck Architecture → PPTX → Render → Visual/Factual/Technical
QA → Final Deck) and the absolute anti-hallucination policy: functionality is
classified as IMPLEMENTED / PARTIALLY IMPLEMENTED / PLANNED / UNKNOWN-NOT FOUND
and never presented as more than the evidence supports.

## Installed components (v1)

| Component | Path | Role | Status |
|---|---|---|---|
| project-presentation-director | `orchestration/project-presentation-director/` | Orchestrator, anti-hallucination policy | Installed |
| project-audit | `research/project-audit/` | Fact Sheet + Evidence Ledger (4 evidence states) + ledger validator | Installed, tested |
| research-lookup | `research/research-lookup/` | Domain research & literature discovery | Installed |
| citation-management | `research/citation-management/` | Source verification states, claim→source links, bibliography builder (verified sources only) | Installed, tested |
| presentation-skill | `presentation/presentation-skill/` | Rubric→deck mapping, claim-wording separation | Installed |
| pptx-engine (PRIMARY) | `presentation/pptx/` | python-pptx deck generation (editable text/tables/native shapes/connectors, notes, badges, numbering) + build CLI | Installed, tested |
| render / visual QA | `presentation/pptx/scripts/render_deck.py` | LibreOffice headless → PDF → per-slide PNGs for the QA loop | Installed; **NOT TESTED in this environment (LibreOffice absent)** |
| scientific-schematics | `visualization/scientific-schematics/` | Native-shape technical diagrams, ledger-derived only | Installed |
| humanizer | `presentation/humanizer/` | Controlled final language pass | Imported (MIT, provenance recorded) |

Supporting: `_audit/` — per-project audit workspace conventions (Fact Sheet,
Evidence Ledger, sources). `_incoming_skills_zips/` — staging area of candidate
skill ZIPs kept for reference; **not** part of the toolbox.

## Quick use

```bash
pip3 install python-pptx                                   # engine dependency
python3 research/project-audit/scripts/validate_ledger.py _audit/<proj>/evidence_ledger.json
python3 presentation/pptx/scripts/build_deck.py deck.json -o deck.pptx
python3 presentation/pptx/scripts/render_deck.py deck.pptx -o render/   # needs LibreOffice
python3 presentation/pptx/tests/test_engine.py             # engine self-test
```

## Licensing

Installed skills are MIT or authored in-house (see `SKILL_INDEX.md`).
AGPL-licensed material (guizang-ppt-skill) and rejected packages were **not**
imported. See `presentation/humanizer/PROVENANCE.md` for import provenance.
