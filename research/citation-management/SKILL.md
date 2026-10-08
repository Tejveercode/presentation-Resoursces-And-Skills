---
name: citation-management
description: >
  Manages source records, claim-to-source traceability, and bibliography
  generation. A bibliography entry may only be generated from a SOURCE VERIFIED
  record. Rejects unverified sources in strict mode.
---

# Citation Management

## Purpose

Own the single source-of-truth list for the presentation, enforce the
claim → source relationship, and generate the References slide content. Core
guarantee: **no unverifiable source may ever appear in the deck or bibliography.**

## Source record schema

`_audit/sources.json` — an array of:

```json
{
  "id": "S1",
  "title": "Observed exact title",
  "authors": ["Only observed authors"],
  "year": 2024,
  "venue": "Journal / conference / publisher / site",
  "url": "https://...",
  "doi": "10.xxxx/... (only if observed)",
  "verification": "SOURCE VERIFIED",
  "verified_via": "URL opened and title/venue matched",
  "supports_claims": ["C3", "C7"]
}
```

`verification` must be exactly one of: `SOURCE FOUND`, `SOURCE VERIFIED`.
Claims reference sources by id; each claim in the literature notes carries the
ids of sources that support it, plus a supported flag mapping to
CLAIM SUPPORTED / CLAIM NOT SUPPORTED.

## Rules

1. A bibliography entry may be generated ONLY from `verification ==
   "SOURCE VERIFIED"`.
2. A claim may be presented as research only if it maps to at least one SOURCE
   VERIFIED record with CLAIM SUPPORTED.
3. If verification fails or is unclear → the source is dropped or kept out of
   the deck entirely; do not reword it into a weaker fake citation.
4. Never merge two sources into one reference. Never invent page numbers,
   volumes, or DOIs.
5. In-slide citation style: numbered `[n]` markers mapping to the References
   slide; every `[n]` must resolve to a verified entry.

## Bibliography generation

Run:

```
python3 research/citation-management/scripts/build_bibliography.py \
  _audit/sources.json [--strict] [--format text|json]
```

- Emits numbered references from SOURCE VERIFIED records only.
- `--strict`: exits non-zero if any source referenced by a claim is not SOURCE
  VERIFIED (use before final delivery).
- Embedded `--selftest` verifies that an unverified source is rejected.
