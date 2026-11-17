"""Rebuild local data artifacts that are not tracked in Git.

DuckDB files, synthetic telemetry, vector stores and fine-tuned adapters are
ignored by Git. They are rebuilt here, deterministically, from seeded
generators, so a fresh clone ends up with byte-for-byte the same lab data the
sealed answer keys were written against.

Generator contract (every file matching assurance-harness/generators/m*.py):
  * `python <generator> --rehydrate` rebuilds its artifacts under
    assurance-harness/data/ (or labs/mNN-*/data/) and exits 0.
  * The seed is fixed inside the generator. No wall-clock time, no unseeded
    randomness, no dependence on dict/set iteration order or the OS.
  * It is idempotent: if the artifacts exist and match, it does nothing.
  * It verifies its own output against the content checksums it committed to
    assurance-harness/generators/checksums/<name>.json and exits non-zero on a
    mismatch. A mismatch means the rebuild is not the dataset the answer key
    describes; do not proceed with the lab until it is resolved.
  * `--force` rebuilds even if artifacts exist.

Usage (from the repo root):
    uv run python scripts/rehydrate.py            # build what is missing
    uv run python scripts/rehydrate.py --force    # rebuild everything
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
GEN_DIR = ROOT / "assurance-harness" / "generators"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="rebuild even if artifacts exist")
    args = ap.parse_args()

    generators = sorted(GEN_DIR.glob("m*.py")) if GEN_DIR.is_dir() else []
    if not generators:
        print("no generators yet (expected before the first lab); nothing to re-hydrate")
        return 0

    failed = []
    for gen in generators:
        cmd = [sys.executable, str(gen), "--rehydrate"] + (["--force"] if args.force else [])
        rel = gen.relative_to(ROOT).as_posix()
        print(f"-> {rel}")
        rc = subprocess.run(cmd, cwd=ROOT).returncode
        if rc != 0:
            failed.append((rel, rc))
    if failed:
        for rel, rc in failed:
            print(f"FAIL: {rel} exited {rc}")
        print("Local lab data does not match what the answer keys expect. Stop and investigate.")
        return 1
    print(f"re-hydrated from {len(generators)} generator(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
