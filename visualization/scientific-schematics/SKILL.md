---
name: scientific-schematics
description: >
  Designs and emits technical diagrams (system architecture, block diagrams,
  workflows, data flow, experimental setup) as EDITABLE native PowerPoint
  shapes and connectors via the pptx engine's `diagram` slide type. Every
  component in a diagram must exist in the audited project's Evidence Ledger.
---

# Scientific Schematics (Native-Shape Diagrams)

## Purpose

Produce technical diagrams for Phase 2 (and Phase 3 workflow/progress visuals)
that render inside the PPTX as editable shapes and connectors — not images —
so the student can adjust them.

## THE cardinal rule: derive, never invent

A component may appear in a diagram ONLY if the Evidence Ledger contains a
corresponding IMPLEMENTED (or clearly labeled PARTIAL) entry — e.g. verified
frontend, verified API layer, verified database. If Redis, Docker, AI services,
queues, auth providers, etc. are NOT verified in the audited repository, they
MUST NOT appear, no matter how typical they are for similar projects.
Planned-but-not-implemented components may appear only in an explicitly labeled
"Planned / Future Work" diagram context, never mixed silently into the as-built
architecture.

## Supported diagram types

- System architecture / block diagram (boxes + directed connectors)
- Data-flow diagram (nodes + labeled edges)
- Workflow / process diagram (steps, optional swimlane grouping via panels)
- Experimental/technical setup (components + connections, with software stack
  table on the same or adjacent slide)

## Contract with the pptx engine

Diagrams are emitted as a `diagram` slide in the deck spec:

```json
{
  "type": "diagram",
  "title": "System Architecture (as implemented)",
  "nodes": [
    {"id": "fe", "label": "React frontend", "x": 0.7, "y": 2.2, "w": 2.6, "h": 1.0, "kind": "rounded"},
    {"id": "db", "label": "PostgreSQL", "x": 9.9, "y": 2.2, "w": 2.4, "h": 1.0, "kind": "cylinder"}
  ],
  "edges": [
    {"from": "fe", "to": "db", "label": "SQL via API", "dashed": false}
  ],
  "notes": "Ledger: FE=IMPLEMENTED (src/...), DB=IMPLEMENTED (schema/...)."
}
```

Coordinates are inches on a 13.333 x 7.5 canvas. `kind`: `rect`, `rounded`,
`ellipse`, `cylinder` (use cylinder for databases/stores). Every edge gets a
label describing the actual data/control flow observed in code.

## Layout rules

- Grid discipline: align nodes on a consistent grid; equal spacing.
- Flow direction: left→right or top→bottom, consistently, matching the real
  request/data flow in the code.
- Labels inside nodes; edge labels short (≤ 4 words); font sizes from the theme.
- No crossings where avoidable; no overlapping nodes; keep ≥ 0.4" gutters.
- Group related components visually (position clusters); do not add decorative
  containers the codebase does not justify.
- Slide notes must cite the ledger entries each node is based on.

## Validation checklist (before QA handoff)

[ ] Every node maps to a ledger entry (or an explicit PLANNED label)
[ ] Every edge corresponds to a real observed data/control path
[ ] Diagram matches the Technology Stack in the Fact Sheet exactly
[ ] Titles say "as implemented" (or "Planned" where applicable)
[ ] Renders legibly at slide size (no tiny text, no overflow)
