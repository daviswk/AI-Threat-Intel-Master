"""Fail if any tracked instruction file contains a machine-specific path.

The repo must clone and run on any machine. Everything in CLAUDE.md, spec/,
.claude/ and scripts/ must use repo-relative paths and OS-neutral commands.

Usage (from the repo root):
    uv run python scripts/check_portable.py

Exit code 0 = clean. 1 = at least one hit (printed as file:line).
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

TARGETS = ["CLAUDE.md", "HEURISTICS.md", "STATE.json", "Makefile", "pyproject.toml", "labs", "assurance-harness",
           "spec", ".claude", "scripts", "literature/convert.py"]
TEXT_SUFFIXES = {".md", ".json", ".py", ".sh", ".toml", ".yml", ".yaml", ".txt", ""}

# Each pattern is assembled from pieces so this file does not match itself.
SEP = r"[\\/]"
PATTERNS = [
    ("Windows drive path", re.compile(r"(?<![A-Za-z])[A-Za-z]:" + SEP + r"(?!/)[\w .%-]")),
    ("Git-Bash drive path", re.compile(r"(?<![\w.])/[a-z]/(?:Users|Program Files|Windows)\b")),
    ("POSIX home path", re.compile(r"(?<![\w.])/(?:Users|home)/[\w.-]+")),
    ("Windows env path", re.compile(r"%(?:LOCALAPPDATA|APPDATA|USERPROFILE|HOMEPATH)%", re.I)),
    ("home-relative path", re.compile(r"(?<![\w.])~" + SEP + r"\.?\w")),
    ("OS-specific venv path", re.compile(r"\.venv" + SEP + r"(?:Scripts|bin)" + SEP)),
]
# Lines allowed to mention an OS-specific venv path: the pip-fallback helper,
# which has to probe both layouts.
ALLOW = {("scripts/_lib.sh", "OS-specific venv path")}


def files():
    for target in TARGETS:
        p = ROOT / target
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and f.suffix.lower() in TEXT_SUFFIXES and "__pycache__" not in f.parts:
                    yield f


def main() -> int:
    hits = []
    for f in files():
        rel = f.relative_to(ROOT).as_posix()
        if rel == "scripts/check_portable.py":
            continue
        try:
            lines = f.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for n, line in enumerate(lines, 1):
            for name, pat in PATTERNS:
                if (rel, name) in ALLOW:
                    continue
                m = pat.search(line)
                if m:
                    hits.append(f"{rel}:{n}: {name}: {m.group(0)!r}")
    if hits:
        print("NOT PORTABLE")
        for h in hits:
            print(" -", h)
        return 1
    print("portable: no machine-specific paths in instruction files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
