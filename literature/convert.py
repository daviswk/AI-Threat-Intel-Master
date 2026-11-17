"""Literature pipeline: one source file (PDF or HTML) -> Markdown with provenance.

Converter: pymupdf4llm for PDFs (chosen in Phase 0; see spec/PHASE0.md),
BeautifulSoup + markdownify for HTML pages.
Only convert sources already verified (spec/CURRICULUM.md or literature/sources.json).

Single file, from the repo root:
    uv run python literature/convert.py <file.pdf|file.html> --module 1 \
        --title "Guide for Conducting Risk Assessments" --publisher NIST \
        --url https://example.org/the-source.pdf [--pages 1-40]

Writes literature/mNN/<slug>.md and refreshes literature/SOURCES.md.
To fetch and convert everything in literature/sources.json, use build.py.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.metadata
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LIT = ROOT / "literature"


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:80]


def parse_pages(spec: str | None) -> list[int] | None:
    """'1-40,55' (1-based, inclusive) -> zero-based page indexes."""
    if not spec:
        return None
    pages: list[int] = []
    for part in spec.split(","):
        lo, _, hi = part.strip().partition("-")
        pages.extend(range(int(lo) - 1, int(hi or lo)))
    return pages


def pdf_to_markdown(path: pathlib.Path, pages: list[int] | None = None) -> tuple[str, str]:
    import pymupdf4llm

    body = pymupdf4llm.to_markdown(str(path), pages=pages, show_progress=False)
    return body, f"pymupdf4llm {importlib.metadata.version('pymupdf4llm')}"


def html_to_markdown(path: pathlib.Path) -> tuple[str, str]:
    from bs4 import BeautifulSoup
    from markdownify import markdownify

    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    for tag in soup(["script", "style", "noscript", "nav", "header", "footer", "aside", "form", "svg", "iframe"]):
        tag.decompose()
    # Prefer <article>, unless it is only a fragment of the page's real content
    # (some sites wrap a teaser or a single card in <article>).
    def text_len(node) -> int:
        return len(node.get_text(" ", strip=True)) if node else 0

    outer = soup.find("main") or soup.find(attrs={"role": "main"}) or soup.body or soup
    article = max(soup.find_all("article"), key=text_len, default=None)
    main = article if article and text_len(article) >= 0.6 * text_len(outer) else outer
    body = markdownify(str(main), heading_style="ATX", strip=["img"])
    body = body.replace("Stay organized with collections Save and categorize content based on your preferences.", "")
    body = re.sub(r"[ \t]+\n", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    return body, f"markdownify {importlib.metadata.version('markdownify')}"


def text_to_markdown(path: pathlib.Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace").replace("\f", "\n")
    return "```text\n" + text.rstrip() + "\n```\n", "verbatim text"


def sniff(path: pathlib.Path) -> str:
    head = path.read_bytes()[:2048].lstrip()
    if head.startswith(b"%PDF"):
        return "pdf"
    if re.search(rb"<!doctype html|<html", head, re.I):
        return "html"
    return "text"


def convert(path: pathlib.Path, *, module: int, title: str, publisher: str, url: str,
            slug: str | None = None, pages: str | None = None, licence: str = "unstated",
            expect: str | None = None, retrieved: str | None = None) -> pathlib.Path:
    kind = sniff(path)
    if expect and kind != expect:
        raise ValueError(f"{path.name}: expected {expect} but the file looks like {kind} "
                         "(a blocked download often saves an HTML error page)")
    if kind == "pdf":
        body, converter = pdf_to_markdown(path, parse_pages(pages))
    elif kind == "html":
        body, converter = html_to_markdown(path)
    else:
        body, converter = text_to_markdown(path)
    if len(body.strip()) < 200:
        raise ValueError(f"{path.name}: conversion produced almost no text (scanned PDF, or a JavaScript-only page)")

    out_dir = LIT / f"m{module:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = slug or slugify(title)
    front = [
        "---",
        f'title: "{title}"',
        f'publisher: "{publisher}"',
        f"source_url: {url}",
        f"retrieved: {retrieved or datetime.date.today().isoformat()}",
        f"sha256: {hashlib.sha256(path.read_bytes()).hexdigest()}",
        f"converter: {converter}",
        f"source_format: {kind}",
    ]
    if pages:
        front.append(f'pages: "{pages}"')
    front += [f'licence: "{licence}"', f"module: {module}", "verified: true", "---", ""]
    out = out_dir / f"{slug}.md"
    out.write_text("\n".join(front) + body, encoding="utf-8", newline="\n")
    return out


def reindex() -> pathlib.Path:
    """Rebuild literature/SOURCES.md from the front matter of every converted file."""
    rows = []
    for md in sorted(LIT.glob("m[0-9][0-9]/*.md")):
        text = md.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not m:
            continue
        fm = {}
        for line in m.group(1).splitlines():
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip().strip('"')
        rows.append((md.parent.name, md.name, fm, len(text)))
    lines = [
        "# Literature index",
        "",
        "Generated by `literature/convert.py` from each file's front matter. Do not edit by hand.",
        "",
        "Converted texts are third-party works kept for private study. **Keep this",
        "repository private.** Only `/portfolio` is written for publication, and it",
        "must not reproduce these texts.",
        "",
        "| Module | File | Title | Publisher | Retrieved | Licence | Size |",
        "|---|---|---|---|---|---|---|",
    ]
    for module, name, fm, size in rows:
        lines.append(
            f"| {module} | [{name}]({module}/{name}) | [{fm.get('title', '')}]({fm.get('source_url', '')}) | "
            f"{fm.get('publisher', '')} | {fm.get('retrieved', '')} | {fm.get('licence', '')} | {size // 1024} KB |"
        )
    out = LIT / "SOURCES.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=pathlib.Path)
    ap.add_argument("--module", type=int, required=True)
    ap.add_argument("--title", required=True, help="exact official title")
    ap.add_argument("--publisher", required=True)
    ap.add_argument("--url", required=True, help="URL the file was retrieved from")
    ap.add_argument("--slug")
    ap.add_argument("--pages", help="PDF only, 1-based inclusive, e.g. 1-40,55")
    ap.add_argument("--licence", default="unstated")
    args = ap.parse_args()
    if not args.source.is_file():
        print(f"not a file: {args.source}")
        return 1
    try:
        out = convert(args.source, module=args.module, title=args.title, publisher=args.publisher,
                      url=args.url, slug=args.slug, pages=args.pages, licence=args.licence)
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1
    reindex()
    print(f"wrote {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
