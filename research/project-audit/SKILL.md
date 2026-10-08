---
name: project-audit
description: >
  Audits an existing software project repository and produces a Project Fact
  Sheet and an Evidence Ledger. Classifies every capability as IMPLEMENTED,
  PARTIALLY IMPLEMENTED, PLANNED, or UNKNOWN / NOT FOUND based on concrete
  repository evidence. No claim without evidence may reach a slide.
---

# Project Audit & Evidence Ledger

## Purpose

Turn an existing software project repository into a structured, evidence-backed
model that every downstream skill (research, slide architecture, diagrams, PPTX
generation, QA) must trace back to. This skill is the anti-hallucination
foundation of the pipeline.

## When to use

FIRST, before any research, slide design, or deck generation.

## Audit process

Inspect the target repository (where applicable): README and docs, source tree,
package manifests / dependency files, configuration, database/schema definitions,
API routes, backend and frontend entry points, authentication, key components and
services, tests, deployment config, assets and screenshots, comments/TODOs, and
any existing reports or diagrams. For each candidate capability, find the concrete
artifact that proves it (code path, config key, schema table, test, runnable
evidence).

## Status classification (exact meanings)

- IMPLEMENTED — verified in actual code/configuration/tests/running evidence.
- PARTIALLY IMPLEMENTED — some implementation exists but is incomplete, limited,
  prototype-level, or missing important parts. Label on slides as
  "Partially Implemented" / "In Progress".
- PLANNED — appears only in roadmap/TODO/design docs/issues without
  implementation evidence. Label as "Future Roadmap".
- UNKNOWN / NOT FOUND — cannot be verified. Never present as a project capability.

Hard rules:

- Never upgrade PLANNED → IMPLEMENTED.
- Never upgrade UNKNOWN → IMPLEMENTED.
- Never infer functionality merely because a library, route, component, database
  table, or documentation mentions it.
- If evidence conflicts, investigate before claiming anything.

## Project Fact Sheet (output)

Produce `_audit/fact_sheet.md` with: PROJECT TITLE, PURPOSE, TARGET USERS,
PROBLEM, CURRENT SOLUTION, IMPLEMENTED / PARTIAL / PLANNED FEATURES, TECHNOLOGY
STACK, ARCHITECTURE, DATABASE / STORAGE, BACKEND, FRONTEND, KEY MODULES,
DEVELOPMENT STATUS, KNOWN LIMITATIONS, VERIFIED RESULTS, AVAILABLE SCREENSHOTS /
DEMO MATERIAL, RESEARCH DOMAIN, HONEST INNOVATION NOTES, GAP NOTES, CLUSTER
ALIGNMENT.

## Evidence Ledger (output)

Produce `_audit/evidence_ledger.json` — an array of entries:

```json
{
  "claim": "System supports real-time monitoring",
  "status": "IMPLEMENTED",
  "evidence_source": "source code + config",
  "evidence_location": "src/monitor/Watcher.ts:40; src/convex/monitoring.ts",
  "confidence": "high",
  "allowed_wording": "The repository implements a file-watcher based monitoring loop.",
  "restrictions": "Do not call it 'real-time AI grading'; no ML component exists."
}
```

Required fields: `claim`, `status`, `evidence_source`,`evidence_location`, `confidence` (high|medium|low), `allowed_wording`, `restrictions` (may be "").
`status` must be exactly one of: `IMPLEMENTED`, `PARTIALLY IMPLEMENTED`,
`PLANNED`, `UNKNOWN / NOT FOUND`. An `IMPLEMENTED` entry MUST have a non-empty
`evidence_location`.

Additional fields (recommended, schema-compatible):

- `presentation_usage` (string) — where this claim may appear, e.g.
  "Phase 2 architecture / Phase 3 prototype".
- `last_verification` (ISO-8601 timestamp) — when the evidence was last
  verified against the repository. Update whenever evidence is re-checked.
- `intake_ref` (string) — id of the project intake manifest this entry was
  audited against (ties ledger entries to the audited branch/commit).

## Validation

Run `python3 research/project-audit/scripts/validate_ledger.py <ledger.json>`
before handing the ledger downstream. It enforces the schema and the
IMPLEMENTED-needs-evidence rule, and has a `--selftest` mode.

## Downstream contract

- Slide architecture uses only `allowed_wording` for project claims.
- Diagrams may contain only components that appear as IMPLEMENTED (or clearly
  labeled PARTIAL/PLANNED) ledger entries.
- Factual QA cross-checks every slide sentence against this ledger.
