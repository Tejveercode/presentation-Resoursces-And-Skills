#!/usr/bin/env python3
"""Validate an Evidence Ledger JSON file produced by the project-audit skill.

Schema: array of entries with keys:
  claim (str, required)
  status (one of IMPLEMENTED | PARTIALLY IMPLEMENTED | PLANNED | UNKNOWN / NOT FOUND)
  evidence_source (str, required)
  evidence_location (str, required for IMPLEMENTED)
  confidence (high | medium | low)
  allowed_wording (str, required)
  restrictions (str, may be "")

Usage:
  python3 validate_ledger.py <ledger.json> [--strict]
  python3 validate_ledger.py --selftest
Exit 0 = valid. Exit 1 = invalid (errors printed).
"""
import json
import sys

STATUSES = {"IMPLEMENTED", "PARTIALLY IMPLEMENTED", "PLANNED", "UNKNOWN / NOT FOUND"}
CONFIDENCES = {"high", "medium", "low"}


def validate(entries):
    errors = []
    if not isinstance(entries, list):
        return ["ledger root must be a JSON array"]
    for i, e in enumerate(entries):
        prefix = f"entry[{i}]"
        if not isinstance(e, dict):
            errors.append(f"{prefix}: not an object")
            continue
        for key in ("claim", "status", "evidence_source", "confidence", "allowed_wording"):
            if key not in e or not str(e.get(key, "")).strip():
                errors.append(f"{prefix}: missing/empty required field '{key}'")
        status = e.get("status")
        if status not in STATUSES:
            errors.append(f"{prefix}: invalid status {status!r}; must be one of {sorted(STATUSES)}")
        conf = e.get("confidence")
        if conf not in CONFIDENCES:
            errors.append(f"{prefix}: invalid confidence {conf!r}; must be one of {sorted(CONFIDENCES)}")
        if status == "IMPLEMENTED" and not str(e.get("evidence_location", "")).strip():
            errors.append(f"{prefix}: IMPLEMENTED requires non-empty evidence_location")
        if status in {"PARTIALLY IMPLEMENTED", "PLANNED", "UNKNOWN / NOT FOUND"} and not str(
            e.get("evidence_location", "")
        ).strip():
            errors.append(f"{prefix}: status {status!r} requires evidence_location describing what WAS found")
    return errors


def selftest():
    good = [
        {"claim": "Auth via email OTP", "status": "IMPLEMENTED",
         "evidence_source": "source code", "evidence_location": "src/convex/auth.ts:12",
         "confidence": "high", "allowed_wording": "Email OTP sign-in is implemented.", "restrictions": ""},
        {"claim": "AI grading", "status": "PLANNED", "evidence_source": "README roadmap",
         "evidence_location": "README.md:88 (roadmap section)", "confidence": "high",
         "allowed_wording": "Planned: AI-assisted grading.", "restrictions": "Future Roadmap only"},
    ]
    bad = [
        {"claim": "Real-time sync", "status": "IMPLEMENTED", "evidence_source": "guess",
         "evidence_location": "", "confidence": "high", "allowed_wording": "x", "restrictions": ""},
        {"claim": "Widget", "status": "MAYBE", "evidence_source": "s", "evidence_location": "a",
         "confidence": "high", "allowed_wording": "x", "restrictions": ""},
    ]
    assert validate(good) == [], validate(good)
    errs = validate(bad)
    assert len(errs) == 2, errs
    print("SELFTEST PASS: ledger validator enforces statuses, evidence_location, and confidence enum")
    return 0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if not args:
        print(__doc__)
        sys.exit(2)
    try:
        with open(args[0], "r", encoding="utf-8") as f:
            entries = json.load(f)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: cannot read ledger: {exc}")
        sys.exit(1)
    errors = validate(entries)
    if errors:
        print("LEDGER INVALID:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    n = len(entries)
    by = {}
    for e in entries:
        by[e["status"]] = by.get(e["status"], 0) + 1
    print(f"LEDGER VALID: {n} entries " + " | ".join(f"{k}={v}" for k, v in sorted(by.items())))
    sys.exit(0)


if __name__ == "__main__":
    main()
