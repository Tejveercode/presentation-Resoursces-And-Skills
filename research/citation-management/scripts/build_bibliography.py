#!/usr/bin/env python3
"""Generate a numbered bibliography from a sources.json file.

Only records with verification == "SOURCE VERIFIED" are emitted.
With --strict, exits 1 if any source referenced by claims is unverified.

sources.json schema: array of
  { id, title, authors[], year, venue, url, doi?, verification, verified_via?,
    supports_claims?[] }

Usage:
  python3 build_bibliography.py <sources.json> [--strict] [--format text|json]
  python3 build_bibliography.py --selftest
"""
import json
import sys


def split(sources):
    verified = [s for s in sources if s.get("verification") == "SOURCE VERIFIED"]
    unverified = [s for s in sources if s.get("verification") != "SOURCE VERIFIED"]
    return verified, unverified


def format_ref(n, s):
    authors = ", ".join(s.get("authors", [])) or "Author(s) not recorded"
    year = s.get("year", "n.d.")
    venue = s.get("venue", "")
    url = s.get("url", "")
    doi = s.get("doi", "")
    parts = [f"[{n}] {authors} ({year}). {s.get('title', 'Untitled')}."]
    if venue:
        parts.append(f" {venue}.")
    if doi:
        parts.append(f" doi:{doi}.")
    if url:
        parts.append(f" {url}")
    return "".join(parts)


def build(sources, fmt="text"):
    verified, unverified = split(sources)
    refs = [format_ref(i + 1, s) for i, s in enumerate(verified)]
    if fmt == "json":
        return {"references": refs, "excluded_unverified": [s.get("id") for s in unverified]}
    return "\n".join(refs), [s.get("id") for s in unverified]


def selftest():
    sources = [
        {"id": "S1", "title": "Real Paper", "authors": ["A. Author"], "year": 2023,
         "venue": "Journal of Things", "url": "https://example.org/paper",
         "verification": "SOURCE VERIFIED", "supports_claims": ["C1"]},
        {"id": "S2", "title": "Fabricated Paper", "authors": ["Nobody"], "year": 2099,
         "venue": "Made-up Venue", "url": "https://nowhere.example",
         "verification": "SOURCE FOUND", "supports_claims": ["C2"]},
    ]
    text, excluded = build(sources)
    assert "[1] A. Author (2023). Real Paper." in text, text
    assert "Fabricated" not in text, text
    assert excluded == ["S2"], excluded
    js = build(sources, fmt="json")
    assert js["excluded_unverified"] == ["S2"]
    print("SELFTEST PASS: unverified source excluded from bibliography")
    return 0


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    with open(args[0], "r", encoding="utf-8") as f:
        sources = json.load(f)
    fmt = "json" if "--format json" in " ".join(sys.argv) else "text"
    strict = "--strict" in sys.argv
    verified, unverified = split(sources)
    out = build(sources, fmt=fmt)
    if strict and unverified:
        print("STRICT MODE: unverified sources referenced by claims present:",
              [s.get("id") for s in unverified])
        print("Remove or verify these sources before final delivery. Exit 1.")
        sys.exit(1)
    if fmt == "json":
        print(json.dumps(out, indent=2))
    else:
        print(out[0])
        if unverified:
            print(f"\nNOTE: {len(unverified)} unverified source(s) excluded from bibliography:")
            for sid in out[1]:
                print(f"  - {sid}")
    sys.exit(0)


if __name__ == "__main__":
    main()
