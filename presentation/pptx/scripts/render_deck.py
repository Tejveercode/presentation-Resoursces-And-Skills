#!/usr/bin/env python3
"""Render a .pptx to per-slide PNGs for the visual-QA loop.

Pipeline: PPTX --(soffice headless)--> PDF --(pdftoppm)--> slide PNGs.

Usage:
  python3 render_deck.py <deck.pptx> [-o render_dir] [--dpi 110]

Environment override: SOFFICE=/path/to/soffice
Exit codes: 0 ok; 1 render failed; 2 dependency missing (message says which).
"""
import argparse
import os
import shutil
import subprocess
import sys


def find_soffice():
    cand = os.environ.get("SOFFICE")
    if cand and os.path.exists(cand):
        return cand
    for name in ("soffice", "libreoffice"):
        path = shutil.which(name)
        if path:
            return path
    return None


def run(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write(res.stdout[-2000:] + res.stderr[-2000:])
    return res.returncode


def main():
    ap = argparse.ArgumentParser(description="Render PPTX to per-slide PNGs (visual QA).")
    ap.add_argument("deck")
    ap.add_argument("-o", "--outdir", default="render")
    ap.add_argument("--dpi", type=int, default=110)
    args = ap.parse_args()

    soffice = find_soffice()
    if not soffice:
        print("DEPENDENCY MISSING: LibreOffice ('soffice') not found on PATH. "
              "Install LibreOffice (or set SOFFICE) to enable the visual-QA render loop. "
              "The PPTX itself is unaffected; QA can still review the file in PowerPoint.")
        sys.exit(2)
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        print("DEPENDENCY MISSING: 'pdftoppm' (poppler-utils) not found; needed to convert "
              "the rendered PDF into per-slide PNGs.")
        sys.exit(2)

    os.makedirs(args.outdir, exist_ok=True)
    pdf = os.path.join(args.outdir, os.path.splitext(os.path.basename(args.deck))[0] + ".pdf")
    rc = run([soffice, "--headless", "--convert-to", "pdf", "--outdir", args.outdir, args.deck])
    if rc != 0 or not os.path.exists(pdf):
        print(f"RENDER FAILED: soffice exited {rc}")
        sys.exit(1)
    prefix = os.path.join(args.outdir, "slide")
    rc = run([pdftoppm, "-png", "-r", str(args.dpi), pdf, prefix])
    if rc != 0:
        print(f"RENDER FAILED: pdftoppm exited {rc}")
        sys.exit(1)
    pngs = sorted(f for f in os.listdir(args.outdir) if f.startswith("slide") and f.endswith(".png"))
    print(f"RENDERED: {len(pngs)} slide image(s) in {args.outdir}")
    print("NEXT: inspect every slide for overflow, clipping, overlap, contrast, numbering, "
          "diagram legibility; fix the spec, rebuild, re-render.")


if __name__ == "__main__":
    main()
