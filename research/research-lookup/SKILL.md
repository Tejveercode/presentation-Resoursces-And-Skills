---
name: research-lookup
description: >
  Conducts domain research and literature discovery for the audited project:
  background, existing solutions, related work, and honest gap framing.
  Enforces source verification before any source may support a claim. Never
  fabricates papers, authors, statistics, URLs, or findings.
---

# Research Lookup

## Purpose

Ground Phase 1 content (problem definition, literature review, research gap,
innovation) and Phase 2 feasibility context in verifiable external sources.

## When to use

After the project audit has produced the Fact Sheet (you need the RESEARCH
DOMAIN and PROBLEM fields).

## Workflow

1. Define research questions from the Fact Sheet (what problem domain, what
   existing approaches, what standards, what known limits).
2. Search credible sources in this priority order: academic papers (peer
   reviewed), official documentation, standards bodies, government/official
   statistics, reputable technical publications, established project docs.
3. For every candidate source record ONLY what you actually saw: exact title,
   authors, venue/publisher, year, URL. If any field could not be observed,
   leave it out — do not guess.
4. Hand candidate sources to `research/citation-management/` for verification.
   A source becomes usable only when it reaches SOURCE VERIFIED there.
5. Extract findings as explicit claim records: each claim states what the source
   says, with the source id attached.

## Source states (used with citation-management)

- SOURCE FOUND — a candidate was located but not yet verified.
- SOURCE VERIFIED — title/venue/URL observed and consistent.
- CLAIM SUPPORTED — a verified source actually states the claim.
- CLAIM NOT SUPPORTED — the source does not say what was hoped; drop or reword.

## Absolute prohibitions

Never fabricate: papers, authors, publication dates, journals, DOIs, statistics,
URLs, research findings. Never present SOURCE FOUND as SOURCE VERIFIED. Never
present a blog opinion as peer-reviewed literature. If you cannot verify a
source, discard it — a smaller honest literature review beats a fabricated one.

## Gap and innovation framing (honest)

Do not manufacture novelty. If the project is not highly novel, present its
contribution honestly as one or more of: integration of existing techniques,
improved workflow, better usability, automation, accessibility, educational
application, system integration, performance improvement, security improvement,
localized solution. The gap statement must be derivable from: the verified
literature + the audited project's actual limitations. Separate clearly:

- RESEARCH: "Existing studies have explored Y."
- INTERPRETATION: "This suggests a potential gap around Z."
- FUTURE: "The project could address Z in a future iteration."

## Output

`_audit/research_sources.json` (candidates for citation-management) and
`_audit/literature_notes.md` (claim records with source ids and quotes/paraphrases
traceable to those ids). Claims without a source id may not be used in slides as
research statements.
