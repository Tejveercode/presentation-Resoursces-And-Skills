#!/usr/bin/env python3
"""project_intake.py — establish target-project identity for the audit.

Accepts a local directory (or metadata supplied by the agent for a GitHub URL /
archive) and emits a project manifest with identity fields + audit timestamp.

Usage:
  python3 project_intake.py <target-dir> -o _audit/<project>/project_manifest.json
  python3 project_intake.py --selftest

The manifest records ONLY what is actually established. If a field cannot be
determined (no git, no URL supplied), it is recorded explicitly as null/absent —
never guessed.
"""
import argparse
import datetime as _dt
import json
import os
import subprocess
import sys


def _git(dirpath):
    """Return {branch, commit} if dirpath is inside a git work tree, else None."""
    try:
        inside = subprocess.run(["git", "-C", dirpath, "rev-parse", "--is-inside-work-tree"],
                                capture_output=True, text=True).stdout.strip()
        if inside != "true":
            return None
        branch = subprocess.run(["git", "-C", dirpath, "rev-parse", "--abbrev-ref", "HEAD"],
                                capture_output=True, text=True).stdout.strip() or None
        commit = subprocess.run(["git", "-C", dirpath, "rev-parse", "HEAD"],
                                capture_output=True, text=True).stdout.strip() or None
        return {"branch": branch, "commit": commit}
    except Exception:  # noqa: BLE001 — git absent / not a repo
        return None


def _read_project_name(url_or_path):
    """Best-effort project name from the URL/dir the USER supplied. Never guessed."""
    if url_or_path:
        base = os.path.basename(str(url_or_path).rstrip("/"))
        if base.endswith(".git"):
            base = base[:-4]
        if base:
            return base
    return os.path.basename(os.path.abspath("."))


def build_manifest(local_dir=None, supplied_url=None, supplied_name=None,
                   supplied_archive=None):
    now = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
    git_info = _git(local_dir) if local_dir else None
    manifest = {
        "source_kind": None,          # "local" | "github_url" | "archive" | "unknown"
        "project_name": supplied_name,
        "source_url": supplied_url,
        "local_dir": os.path.abspath(local_dir) if local_dir else None,
        "archive": supplied_archive,
        "branch": None,
        "commit": None,
        "audit_timestamp_utc": now,
        "auditor": "presentation-Resources-And-Skills toolbox",
        "notes": [],
    }
    if supplied_archive:
        manifest["source_kind"] = "archive"
    elif supplied_url and supplied_url.startswith(("http://", "https://")):
        manifest["source_kind"] = "github_url"
    elif local_dir:
        manifest["source_kind"] = "local"
    else:
        manifest["source_kind"] = "unknown"
        manifest["notes"].append("No local directory, URL, or archive supplied.")
    if git_info:
        manifest["branch"] = git_info["branch"]
        manifest["commit"] = git_info["commit"]
    else:
        manifest["notes"].append("Git metadata not available at intake — branch/commit recorded as absent.")
    if not manifest["project_name"]:
        manifest["project_name"] = _read_project_name(supplied_url or local_dir or supplied_archive)
        manifest["notes"].append("project_name derived from supplied path/url basename; override if wrong.")
    return manifest


def validate_manifest(m):
    errs = []
    for key in ("source_kind", "project_name", "audit_timestamp_utc"):
        if not m.get(key):
            errs.append(f"missing required field: {key}")
    if m.get("source_kind") not in (None, "local", "github_url", "archive", "unknown"):
        errs.append(f"invalid source_kind {m.get('source_kind')!r}")
    return errs


def selftest():
    tmp = "/tmp/intake_selftest_proj"
    os.makedirs(tmp, exist_ok=True)
    m = build_manifest(local_dir=tmp, supplied_name="fixture-proj")
    errs = validate_manifest(m)
    assert errs == [], errs
    assert m["source_kind"] == "local" and m["project_name"] == "fixture-proj"
    assert m["audit_timestamp_utc"].endswith("Z") or "+" in m["audit_timestamp_utc"]
    m2 = build_manifest(supplied_url="https://github.com/someone/their-project.git",
                        supplied_name="their-project")
    assert m2["source_kind"] == "github_url" and m2["branch"] is None
    m3 = build_manifest(local_dir=tmp)  # name derived, flagged in notes
    assert any("derived" in n for n in m3["notes"])
    print("SELFTEST PASS: intake manifest identity fields, source_kind, derived-name flagging")
    return 0


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    ap = argparse.ArgumentParser(description="Establish target-project intake manifest.")
    ap.add_argument("target", nargs="?", help="local target-project directory")
    ap.add_argument("--url", help="GitHub/remote URL of the target project (if known)")
    ap.add_argument("--name", help="project display name (recommended override)")
    ap.add_argument("--archive", help="path to project archive file")
    ap.add_argument("-o", "--out", default="_audit/intake/project_manifest.json")
    args = ap.parse_args()
    if not args.target and not args.url and not args.archive:
        print(__doc__)
        sys.exit(2)
    m = build_manifest(local_dir=args.target, supplied_url=args.url,
                       supplied_name=args.name, supplied_archive=args.archive)
    errs = validate_manifest(m)
    if errs:
        print("MANIFEST INVALID:", "; ".join(errs))
        sys.exit(1)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2)
    print(f"INTAKE MANIFEST: {args.out}")
    print(json.dumps({k: m[k] for k in ("source_kind", "project_name", "source_url",
                                         "branch", "commit", "audit_timestamp_utc")}, indent=2))
    for n in m["notes"]:
        print(f"note: {n}")


if __name__ == "__main__":
    main()
