---
name: presentation-skill
description: >
  Translates the teacher's Phase 1/2/3 rubric and the audited Evidence Ledger
  into a coherent ~12–14 slide academic presentation architecture with strict
  claim-wording separation (PROJECT FACT / RESEARCH / INTERPRETATION / FUTURE
  WORK) and per-slide evidence requirements.
---

# Academic Presentation Architecture

## Purpose

Convert (a) the teacher rubric, (b) the Project Fact Sheet / Evidence Ledger,
and (c) verified research into a slide plan, then a deck spec for the python-pptx
engine. Accuracy outranks polish; evidence outranks coverage.

## Rubric mapping

PHASE 1 — FOUNDATION (3–6 slides). Must address: Project Title & Background;
Clarity of Problem Definition; Literature Review Quality; Innovativeness of the
Idea; Alignment with Cluster-Specific Objectives. Typical shape: 1) Title +
background, 2) Problem statement + motivation, 3) Existing solutions / literature
review, 4) Research gap + proposed contribution, 5) Innovation + cluster
alignment.

PHASE 2 — TECHNICAL APPROACH (3–6 slides). For Engineering & Science (default
for software projects unless the supplied rubric says otherwise): System
Architecture; Block Diagram / Technical Workflow; Technology Stack + Required
Software; Experimental/Technical Setup; Feasibility + innovative elements of the
approach. All architecture content comes from the audit — never invented.

PHASE 3 — EXECUTION & RESULTS (3–6 slides). Progress relative to initial plan;
current implementation status (with state labels); verified prototype /
screenshots; challenges encountered + solutions implemented; methodology
refinement; demo readiness + future work (clearly separated).

Total: target ~12–14 slides when evidence supports it; adapt to the evidence —
never pad, never invent content to fill a slot. A 3-slide phase with only
verified material beats a 6-slide phase with padding.

## Claim wording separation (mandatory on every slide)

- PROJECT FACT — "The repository contains / implements X." (Evidence Ledger)
- RESEARCH — "Existing studies have explored Y." (verified sources)
- INTERPRETATION — "This suggests a potential gap around Z." (clearly reasoned)
- FUTURE WORK — "The project could address Z in a future iteration." (label:
  Planned / Future Roadmap)

Bad: "The platform supports real-time AI grading" (unverified).
Good: "The repository implements X (Implemented)" / "Planned: X."

## Status labeling

Slides (or bullets) presenting PARTIALLY IMPLEMENTED work must be labeled
"Partially Implemented"; PLANNED items "Planned / Future Roadmap"; never present
UNKNOWN items as capabilities. The deck spec supports a `badge` field per slide
for this label.

## Evidence requirements per slide

Every slide lists in its speaker notes: which ledger claims / which verified
sources it relies on. A slide with zero backing entries must not exist.

## Speaker notes & demo

Notes should let the student explain: the problem, why it matters, how the
architecture works, what is actually implemented, what each screenshot shows,
what remains incomplete. Demo support: DEMO START POINT, KEY FUNCTIONALITY TO
SHOW, EXPECTED RESULT, KNOWN LIMITATIONS — only verified functionality.

## Handoff

Emit a deck-spec JSON consumed by `presentation/pptx/scripts/build_deck.py`
(slide types: title, section, bullets, two_column, table, image, diagram).
Then run the pptx engine's QA loop before delivery.
