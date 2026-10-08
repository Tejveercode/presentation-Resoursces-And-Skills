#!/usr/bin/env python3
"""Build an editable .pptx from a deck-spec JSON.

Usage:
  python3 build_deck.py <deck.json> [-o out.pptx] [-t theme.json]
Defaults: -o deck.pptx, -t ../templates/academic_theme.json
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pptx_engine import build_deck, load_json  # noqa: E402

DEFAULT_THEME = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "..", "templates", "academic_theme.json")


def main():
    ap = argparse.ArgumentParser(description="Build an editable academic PPTX from a deck spec.")
    ap.add_argument("spec", help="deck-spec JSON path")
    ap.add_argument("-o", "--out", default="deck.pptx")
    ap.add_argument("-t", "--theme", default=DEFAULT_THEME)
    args = ap.parse_args()
    spec = load_json(args.spec)
    theme = load_json(args.theme)
    try:
        out = build_deck(spec, theme, args.out)
    except ValueError as exc:
        print(f"BUILD FAILED: {exc}")
        sys.exit(1)
    print(f"BUILT: {out}")


if __name__ == "__main__":
    main()
