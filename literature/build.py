"""Fetch and convert every source declared in literature/sources.json.

Each entry is a source that was verified before it was listed. Raw downloads go
to literature/_raw/ (not tracked); converted Markdown goes to literature/mNN/
(tracked), so ingestion can run fully offline after a clone.

Usage (from the repo root):
    uv run python literature/build.py                 # everything not yet converted
    uv run python literature/build.py --module 2      # one module
    uv run python literature/build.py --only stix-2-1 # one source
    uv run python literature/build.py --force         # re-download and re-convert

Downloads use plain `curl` with its default identity. A site that refuses
automated clients is reported as BLOCKED and left for a manual save:
open the URL in a browser, save as PDF into literature/_inbox/<slug>.pdf, and
re-run. This script never disguises itself as a browser.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import convert as conv  # noqa: E402

LIT = conv.LIT
RAW = LIT / "_raw"
INBOX = LIT / "_inbox"
EXT = {"pdf": ".pdf", "html": ".html", "text": ".txt", "json": ".json"}


def snapshot(e: dict, raw: pathlib.Path) -> None:
    """Keep a JSON dataset byte-exact (optionally gzipped) and write a small
    Markdown record describing it, so it appears in SOURCES.md."""
    import datetime
    import gzip
    import hashlib

    data = raw.read_bytes()
    doc = json.loads(data)                      # also proves the download is real JSON
    out_dir = LIT / f"m{e['module']:02d}"
    snap_dir = out_dir / "snapshots"
    snap_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    if e.get("compress"):
        target = snap_dir / f"{e['slug']}.json.gz"
        with open(target, "wb") as fh, gzip.GzipFile(fileobj=fh, mode="wb", mtime=0, filename="") as gz:
            gz.write(data)                      # mtime=0: identical input gives identical bytes
    else:
        target = snap_dir / f"{e['slug']}.json"
        target.write_bytes(data)
    facts = []
    if isinstance(doc, dict):
        for key, value in doc.items():
            if isinstance(value, (str, int, float)) and len(str(value)) < 80:
                facts.append(f"- `{key}`: {value}")
            elif isinstance(value, list):
                facts.append(f"- `{key}`: {len(value)} entries")
    front = [
        "---", f'title: "{e["title"]}"', f'publisher: "{e["publisher"]}"', f"source_url: {e['url']}",
        f"retrieved: {today}", f"sha256: {hashlib.sha256(data).hexdigest()}",
        "converter: none (byte-exact snapshot)", "source_format: json",
        f'licence: "{e.get("licence", "unstated")}"', f"module: {e['module']}", "verified: true", "---", "",
    ]
    body = [
        f"# {e['title']}", "",
        f"Dataset snapshot retrieved {today}. The `sha256` above is of the uncompressed download.", "",
        f"- File: `snapshots/{target.name}` ({target.stat().st_size / 1024:.0f} KB on disk, "
        f"{len(data) / 1024:.0f} KB uncompressed)",
        *facts, "",
        "This is a point-in-time copy for offline work. Cite it with its retrieval date, and",
        "refresh it from `source_url` when a connection is available.", "",
    ]
    (out_dir / f"{e['slug']}.md").write_text("\n".join(front + body), encoding="utf-8", newline="\n")


def fetch(url: str, dest: pathlib.Path) -> str | None:
    """Download url to dest. Return None on success, or a short reason."""
    curl = shutil.which("curl")
    if not curl:
        return "curl not found"
    tmp = dest.with_suffix(dest.suffix + ".part")
    proc = subprocess.run(
        [curl, "-L", "--fail", "-sS", "--max-time", "180", "--retry", "2", "-o", str(tmp), url],
        capture_output=True, text=True)
    if proc.returncode != 0:
        tmp.unlink(missing_ok=True)
        return (proc.stderr.strip().splitlines() or ["curl failed"])[-1][:160]
    tmp.replace(dest)
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", type=int)
    ap.add_argument("--only", help="slug of a single source")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    entries = json.loads((LIT / "sources.json").read_text(encoding="utf-8"))["sources"]
    RAW.mkdir(parents=True, exist_ok=True)
    results: list[tuple[str, str, str]] = []
    for e in entries:
        if args.module and e["module"] != args.module:
            continue
        if args.only and e["slug"] != args.only:
            continue
        slug, fmt = e["slug"], e["format"]
        out = LIT / f"m{e['module']:02d}" / f"{slug}.md"
        if out.exists() and not args.force:
            results.append((slug, "ok (cached)", ""))
            continue
        raw = RAW / f"{slug}{EXT[fmt]}"
        inbox = next((p for p in (INBOX / f"{slug}.pdf", INBOX / f"{slug}.html") if p.is_file()), None)
        expect = fmt
        if inbox:
            raw, expect = inbox, None          # a manual save may be PDF even for an HTML source
        elif e.get("manual"):
            results.append((slug, "MANUAL", e["manual"]))
            continue
        elif args.force or not raw.exists():
            reason = fetch(e["url"], raw)
            if reason:
                results.append((slug, "BLOCKED", reason))
                continue
        try:
            if fmt == "json":
                snapshot(e, raw)
            else:
                conv.convert(raw, module=e["module"], title=e["title"], publisher=e["publisher"],
                             url=e["url"], slug=slug, pages=e.get("pages"),
                             licence=e.get("licence", "unstated"), expect=expect)
            results.append((slug, "ok", ""))
        except Exception as exc:  # report and continue with the other sources
            results.append((slug, "FAILED", str(exc)[:200]))

    conv.reindex()
    width = max((len(s) for s, _, _ in results), default=10)
    for slug, status, note in results:
        print(f"{slug:<{width}}  {status:<12} {note}")
    bad = [r for r in results if r[1] in ("BLOCKED", "FAILED")]
    manual = [r for r in results if r[1] == "MANUAL"]
    print(f"\n{len(results) - len(bad) - len(manual)} converted, {len(manual)} need a manual save, {len(bad)} failed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
