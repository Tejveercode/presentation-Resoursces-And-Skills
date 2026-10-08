# _audit — per-project audit workspace

This directory holds the **outputs of running the toolbox against one specific
project repository**. Nothing here is a skill; it is the evidence layer.

Conventional files (created by the agent at run time, one set per project):

- `fact_sheet.md` — Project Fact Sheet (schema defined in
  `research/project-audit/SKILL.md`).
- `evidence_ledger.json` — Evidence Ledger entries
  (claim / status / evidence_source / evidence_location / confidence /
  allowed_wording / restrictions). Validate with
  `research/project-audit/scripts/validate_ledger.py`.
- `research_sources.json` — candidate sources from `research/research-lookup/`.
- `sources.json` — verified source records from `research/citation-management/`.
- `literature_notes.md` — claim records traceable to source ids.

Rules:

- Everything the presentation asserts about the PROJECT must exist in the
  Evidence Ledger; everything asserted as RESEARCH must trace to a SOURCE
  VERIFIED record.
- Status labels on slides must match ledger statuses
  (IMPLEMENTED / PARTIALLY IMPLEMENTED / PLANNED / UNKNOWN / NOT FOUND).
- Per-project audit sets should be kept in a subdirectory named after the
  project to avoid collisions.
