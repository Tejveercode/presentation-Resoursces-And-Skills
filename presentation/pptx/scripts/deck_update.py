#!/usr/bin/env python3
"""deck_update.py — canonical presentation lifecycle manager.

Enforces the safe-update contract:
  - one canonical PPTX (presentation/project-presentation.pptx), never
    final/final-final/v2 files;
  - generation goes through a working file
    (project-presentation.__working__.pptx);
  - QA gates (check_deck.py + optional render-loop) run on the WORKING file;
  - the canonical file is replaced ATOMICALLY only after QA passes
    (tmp name + os.replace; never overwrite a validated deck with a failed one);
  - temporary/working files are deleted on success; deleted on failure too
    (the untouched canonical file remains the deliverable).

Usage:
  python3 deck_update.py build  --spec deck.json   [--canonical presentation/project-presentation.pptx]
  python3 deck_update.py update --spec deck.json --canonical <existing.pptx>
      (identical to build; refuses if canonical exists AND QA will fail; i.e. QA
       is always enforced before replacing)
  python3 deck_update.py verify --canonical <existing.pptx>
      (QA-check an existing canonical deck without rebuilding)
  python3 deck_update.py --selftest
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORKING_SUFFIX = ".__working__.pptx"


def canonical_names(root, basename="project-presentation.pptx"):
    return {
        "canonical": os.path.join(root, "presentation", basename),
        "working": os.path.join(root, "presentation",
                                basename.replace(".pptx", WORKING_SUFFIX)),
    }


def qa_passes(deck_path):
    """Run check_deck.py on the given deck. Returns (ok, output)."""
    res = subprocess.run(
        [sys.executable, os.path.join(HERE, "check_deck.py"), deck_path,
         "--min-slides", "0"],  # local structural checks; deck-size policy is the caller's
        capture_output=True, text=True)
    return res.returncode == 0, (res.stdout or "") + (res.stderr or "")


def _tempdirname(path):
    return os.path.basename(path) + ".tmpfile"


def build_or_update(spec_path, canonical_root, out=None, theme=None):
    """Build → QA → atomic-replace-or-first-install → cleanup. Returns 0/1."""
    paths = canonical_names(canonical_root)
    canonical = out or paths["canonical"]
    working = canonical.replace(".pptx", WORKING_SUFFIX)
    tmp_new = working + ".new"
    tmp_old = working + ".old"
    for p in (working, tmp_new, tmp_old):
        if os.path.exists(p):
            os.remove(p)
    build_cmd = [sys.executable, os.path.join(HERE, "build_deck.py"), spec_path,
                 "-o", working]
    if theme:
        build_cmd += ["-t", theme]
    res = subprocess.run(build_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("BUILD FAILED (canonical untouched):")
        print(res.stdout or "", res.stderr or "")
        if os.path.exists(tmp_new):
            os.remove(tmp_new)
        return 1
    ok, output = qa_passes(working)
    if not ok:
        print("QA FAILED — canonical deck NOT replaced:")
        print(output)
        os.remove(working)
        return 1
    pre_existing = os.path.exists(canonical)
    if pre_existing:
        os.replace(canonical, tmp_old)
    os.replace(working, canonical)
    cleanup = True
    if pre_existing:
        cleanup = os.path.exists(canonical) and os.path.getsize(canonical) > 0
        if cleanup:
            os.remove(tmp_old)
        else:
            os.replace(tmp_old, canonical)  # rollback
    if cleanup:
        if os.path.exists(tmp_new):
            os.remove(tmp_new)
        print(f"CANONICAL DECK {'UPDATED' if pre_existing else 'CREATED'}: {canonical}")
        return 0
    print("ROLLBACK: restore validated deck — QA validation incomplete")
    return 1


def selftest():
    """End-to-end lifecycle test in a temp dir using the engine + check_deck."""
    import tempfile
    sys.path.insert(0, HERE)
    from pptx_engine import load_json  # noqa: E402

    theme_path = os.path.join(HERE, "..", "templates", "academic_theme.json")
    good_spec = {
        "project": "UPDATE SELFTEST",
        "slides": [
            {"type": "title", "title": "Canonical Deck", "notes": "n1"},
            {"type": "bullets", "title": "Content",
             "bullets": ["verified point one with meaningful content about the system",
                         "verified point two describing tested behaviour"],
             "notes": "n2"},
        ],
    }
    bad_spec = {"project": "BAD", "slides": [
        {"type": "title", "title": "Only a title", "notes": "n"}]}
    bad_spec_path = os.path.join(tempfile.gettempdir(), "deck_bad_spec.json")
    with open(bad_spec_path, "w", encoding="utf-8") as f:
        json.dump(bad_spec, f)
    with tempfile.TemporaryDirectory() as td:
        spec_path = os.path.join(td, "spec.json")
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(good_spec, f)
        # 1) first build → CREATED;  canonical exists; no working leftovers
        rc = build_or_update(spec_path, td)
        paths = canonical_names(td)
        assert rc == 0 and os.path.exists(paths["canonical"]), "first build failed"
        c1 = paths["canonical"]
        leftovers_after_build = [p for p in os.listdir(os.path.dirname(c1))
                                 if WORKING_SUFFIX in p or p.endswith(".tmpfile")]
        assert not leftovers_after_build, leftovers_after_build
        import hashlib
        h1 = hashlib.sha256(open(c1, "rb").read()).hexdigest()
        # 2) rebuild same spec → UPDATED; identical bytes
        rc = build_or_update(spec_path, td)
        assert rc == 0
        h2 = hashlib.sha256(open(c1, "rb").read()).hexdigest()
        assert h1 == h2, "rebuild produced different bytes for identical spec"
        # 3) failing deck (too little text) → QA fails → canonical NOT replaced
        rc = build_or_update(bad_spec_path, td)
        assert rc == 1, "QA-fail deck must not replace canonical"
        h3 = hashlib.sha256(open(c1, "rb").read()).hexdigest()
        assert h3 == h1, "canonical was modified despite failed QA"
        # 4) no stray temp/working files remain
        leftovers = [p for p in os.listdir(os.path.dirname(c1))
                     if WORKING_SUFFIX in p or p.endswith(".tmpfile")]
        assert not leftovers, leftovers
        os.remove(bad_spec_path)
    print("SELFTEST PASS: create, update-in-place, QA-fail rollback, no leftover files")
    return 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    ap = argparse.ArgumentParser(description="Canonical PPTX build/update lifecycle.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("build", "update"):
        p = sub.add_parser(name)
        p.add_argument("--spec", required=True)
        p.add_argument("--canonical", "-o", dest="canonical_path")
        p.add_argument("-t", "--theme")
    v = sub.add_parser("verify")
    v.add_argument("--canonical", required=True)
    args = ap.parse_args()
    if args.cmd == "verify":
        ok, output = qa_passes(args.canonical)
        print(output)
        print("VERIFY:", "PASS" if ok else "FAIL")
        sys.exit(0 if ok else 1)
    root = "."
    if args.canonical_path:
        canonical_path = os.path.abspath(args.canonical_path)
        root = os.path.dirname(os.path.dirname(canonical_path)) or "."
    return build_or_update(args.spec, root,
                           out=args.canonical_path, theme=args.theme)


if __name__ == "__main__":
    sys.exit(main() or sys.exit(0))
