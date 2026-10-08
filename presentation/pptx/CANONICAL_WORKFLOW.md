# Canonical Presentation & Update Policy

## Canonical location (§19)

The generated presentation belongs to the **target project**, not this toolbox.
For each target project run, outputs live in the target project directory:

```
<target-project>/
└── presentation/
    ├── project-presentation.pptx       ← THE canonical deck (exactly one)
    ├── presentation-state.json         ← generation state (identity/state/QA)
    ├── assets/
    │   ├── screenshots/                ← real, verified screenshots only
    │   └── diagrams/                   ← diagram source data if exported
    ├── evidence/
    │   └── evidence-ledger.json        ← Evidence Ledger for the target project
    └── sources/
        └── sources.json                ← verified source records
```

The canonical PPTX file name is always `project-presentation.pptx`.

## One deck only (§20)

No `final.pptx`, `final-final.pptx`, `presentation-v2.pptx`,
`presentation_latest.pptx`, `presentation_copy.pptx` — unless the user
explicitly asks for versions. If the canonical deck exists, you **update it**,
never create a sibling duplicate.

## Safe update process (§21)

Enforced by `scripts/deck_update.py`:

1. Build to `project-presentation.__working__.pptx` (never touch the canonical
   file until the new version passes QA).
2. Run QA on the **working** file (`check_deck.py`).
3. QA pass → atomic replace (`os.replace`) of the canonical file, followed by
   verification that the replacement exists and is non-empty; on any failure,
   the previous canonical file is restored (rollback) and the working copy is
   deleted.
4. QA fail → working file deleted, canonical **not replaced**.
5. Temporary/working files (`__working__`, `__working__.new`, `__working__.old`)
   never survive either outcome.

## Presentation state (§22)

After a successful canonical replacement, write/update
`presentation/presentation-state.json` with the fields the director requires:
project identity (name/source/branch/commit from the intake manifest), audit
timestamp, generation timestamp, slide ids/purposes, rubric mapping, evidence
references (ledger entry refs), source references, asset references,
implementation-status dependencies, design-system metadata (design brief path +
preference source flags), QA status (per gate), canonical file path + size
+ sha256.

## QA gate order (§27)

PROJECT TRUTH → RESEARCH EVIDENCE → RUBRIC COVERAGE → (Design QA + UX +
color/contrast) → TECHNICAL ACCURACY → VISUAL QA (render loop, LibreOffice) →
ANTI-AI-SLOP → PPTX VALIDATION (`check_deck.py` + open-test). All gates must
pass before canonical replacement.
