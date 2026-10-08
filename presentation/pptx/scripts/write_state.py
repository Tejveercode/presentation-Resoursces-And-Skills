#!/usr/bin/env python3
"""write_state.py — write/update presentation/presentation-state.json.

Collects generation state for a deck: slide inventory (ids/purposes/types),
QA status, canonical file metadata (size + sha256), with optional project
identity merged from an intake manifest.

Usage:
  python3 write_state.py --deck presentation/project-presentation.pptx \
      [-o presentation/presentation-state.json] \
      [--manifest _audit/intake/project_manifest.json] \
      [--qa '{"design_qa":"PASS","factual_qa":"PASS","anti_slop_qa":"PASS"}'] \
      [--rubric-mapping '{"phase_1": [1,2,3], "phase_2": [4,5], "phase_3": [6,7,8]}'] \
      [--selftest]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def slide_inventory(deck_path):
    from pptx import Presentation
    prs = Presentation(deck_path)
    out = []
    for i, slide in enumerate(prs.slides, start=1):
        title = ""
        purpose = ""
        for shp in slide.shapes:
            if shp.has_text_frame and shp.text_frame.text.strip():
                text = shp.text_frame.text.strip().splitlines()[0]
                if not title:
                    title = text
                elif not purpose and shp.top is not None:
                    purpose = text
                    break
        out.append({"index": i, "title": title, "purpose_hint": purpose})
    return out


def build_state(deck_path, manifest=None, qa=None, rubric=None):
    st = {
        "schema_version": 1,
        "deck_path": os.path.abspath(deck_path),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "slide_inventory": slide_inventory(deck_path),
        "qa": {
            "design_qa": None, "factual_qa": None, "technical_qa": None,
            "visual_qa": None, "anti_slop_qa": None, "pptx_validation": None,
        },
        "rubric_mapping": rubric or {},
        "design_system": {"design_brief": None, "design_prefs": None},
        "canonical": None,
    }
    if qa:
        st["qa"].update(qa)
    if manifest:
        st["project_identity"] = {k: manifest.get(k) for k in
                                  ("project_name", "source_url", "source_kind",
                                   "branch", "commit", "audit_timestamp_utc")}
    st["canonical"] = {
        "path": os.path.abspath(deck_path),
        "size_bytes": os.path.getsize(deck_path),
        "sha256": sha256(deck_path),
    }
    return st


def selftest():
    here = HERE
    spec = {
        "project": "STATE SELFTEST",
        "slides": [
            {"type": "title", "title": "State Test", "notes": "n"},
            {"type": "bullets", "title": "Point Slide",
             "bullets": ["alpha", "beta"], "notes": "n"},
        ],
    }
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        sys.path.insert(0, os.path.join(here))
        from pptx_engine import build_deck, load_json
        theme = load_json(os.path.join(here, "..", "templates", "academic_theme.json"))
        out = os.path.join(td, "deck.pptx")
        build_deck(spec, theme, out)
        st = build_state(out, qa={"design_qa": "PASS", "pptx_validation": "PASS"})
        assert st["canonical"]["sha256"] and len(st["canonical"]["sha256"]) == 64
        assert st["slide_inventory"][0]["title"] == "State Test"
        assert st["qa"]["design_qa"] == "PASS"
        # write to file and re-read
        sp = os.path.join(td, "state.json")
        with open(sp, "w", encoding="utf-8") as f:
            json.dump(st, f, indent=2)
        loaded = json.load(open(sp, encoding="utf-8"))
        assert loaded["canonical"]["size_bytes"] > 0
    print("SELFTEST PASS: state builder + slide inventory + sha256 + round-trip")
    return 0


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    ap = argparse.ArgumentParser(description="Write presentation-state.json for a deck.")
    ap.add_argument("--deck", required=True)
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--manifest", help="intake manifest JSON to merge identity fields")
    ap.add_argument("--qa", help="QA status JSON (inline)")
    ap.add_argument("--rubric-mapping", help="rubric mapping JSON (inline)")
    args = ap.parse_args()
    manifest = None
    if args.manifest:
        with open(args.manifest, encoding="utf-8") as f:
            manifest = json.load(f)
    qa = json.loads(args.qa) if args.qa else None
    rubric = json.loads(args.rubric_mapping) if args.rubric_mapping else None
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.deck)),
                                   "presentation-state.json")
    st = build_state(args.deck, manifest=manifest, qa=qa, rubric=rubric)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=2)
    print(f"STATE WRITTEN: {out}")
    print(f"slides: {len(st['slide_inventory'])}; sha256: {st['canonical']['sha256'][:16]}...")


if __name__ == "__main__":
    main()
