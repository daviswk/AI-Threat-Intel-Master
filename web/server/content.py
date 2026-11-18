"""Readers for repo content. Every path goes through Repo (paths.py)."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import time
from pathlib import Path

import yaml

from .paths import (GATE_BRIEFS, INCUBATION_FILES, MODULE_DIR, PROCEDURE_FILE,
                    FINDING_FILE, PathRefused, Repo)

MAX_READ_BYTES = 4 * 1024 * 1024
FRONT_MATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.S)
HEUR_MARKER = "<!-- entries start below this line -->"
HEUR_ENTRY = re.compile(
    r"^### (H-(\d{2})-(\d+))[ \t]+\(Module (\d{2})\)[ \t]*\n(.+?)\nEvidence:[ \t]*(.+?)[ \t]*$", re.M | re.S)
PAIR_SUFFIX = re.compile(r"^(.*?)[ _-]?([AB])$")


class TooLarge(Exception):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_bytes(path: Path) -> bytes | None:
    """File bytes, or None if the file does not exist."""
    try:
        if path.stat().st_size > MAX_READ_BYTES:
            raise TooLarge(path.name)
        return path.read_bytes()
    except FileNotFoundError:
        return None


def read_text(repo: Repo, rel: str) -> str | None:
    data = read_bytes(repo.read_path(rel))
    return None if data is None else data.decode("utf-8", errors="replace")


def read_state(repo: Repo) -> dict:
    """STATE.json. Retried briefly: it may be read while it is being written."""
    last: Exception | None = None
    for _ in range(6):
        try:
            data = read_bytes(repo.read_path("STATE.json"))
            if data is None:
                raise FileNotFoundError("STATE.json")
            return json.loads(data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, PermissionError) as exc:
            last = exc
            time.sleep(0.08)
    raise ValueError(f"STATE.json could not be parsed: {last}")


def split_front_matter(text: str) -> tuple[dict | None, str]:
    m = FRONT_MATTER.match(text)
    if not m:
        return None, text
    try:
        meta = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None, text
    if not isinstance(meta, dict):
        return None, text
    return json.loads(json.dumps(meta, default=str)), text[m.end():]


def open_slugs(state: dict) -> list[str]:
    return [m["slug"] for m in state["modules"] if m["status"] != "locked"]


# ---------- literature ----------
def literature(repo: Repo, module_id: int) -> list[dict]:
    out = []
    for rel in repo.walk(f"literature/m{module_id:02d}"):
        text = read_text(repo, rel) or ""
        meta, _ = split_front_matter(text)
        meta = meta or {}
        out.append({"path": rel, "name": rel.rsplit("/", 1)[-1],
                    "title": meta.get("title"), "publisher": meta.get("publisher")})
    return out


# ---------- heuristics ----------
def heuristics(repo: Repo) -> dict:
    data = read_bytes(repo.read_path("HEURISTICS.md"))
    if data is None:
        return {"exists": False, "sha256": None, "entries": []}
    text = data.decode("utf-8", errors="replace").replace("\r\n", "\n")
    body = text.split(HEUR_MARKER, 1)[1] if HEUR_MARKER in text else text
    entries = [{"id": m.group(1), "module": int(m.group(2)), "n": int(m.group(3)),
                "rule": " ".join(m.group(5).split()), "evidence": m.group(6)}
               for m in HEUR_ENTRY.finditer(body)]
    return {"exists": True, "sha256": sha256(data), "entries": entries}


# ---------- flashcards ----------
def flashcards(repo: Repo) -> list[dict]:
    cards = []
    for rel in repo.walk("flashcards"):
        m = re.match(r"^flashcards/m(\d{2})\.csv$", rel)
        text = read_text(repo, rel) or ""
        rows = [line for line in text.splitlines() if line.strip() and not line.startswith("#")]
        for row in csv.reader(rows):
            if len(row) >= 3:
                cards.append({"file": rel, "module": int(m.group(1)) if m else None,
                              "front": row[0], "back": row[1], "tags": row[2].split()})
    return cards


def cert_counts(cards: list[dict]) -> list[dict]:
    """Cards per cert, from the tags actually present. No tag is invented."""
    counts: dict[str, int] = {}
    for card in cards:
        for cert in {t.split("::", 1)[0] for t in card["tags"] if "::" in t}:
            counts[cert] = counts.get(cert, 0) + 1
    order = ["CISA", "AAIA", "AIGP"]
    return [{"cert": c, "cards": counts[c]}
            for c in sorted(counts, key=lambda c: (order.index(c) if c in order else len(order), c))]


# ---------- portfolio ----------
def portfolio(repo: Repo) -> list[dict]:
    out = []
    for rel in repo.walk("portfolio"):
        text = read_text(repo, rel) or ""
        first = next((ln[2:].strip() for ln in text.splitlines() if ln.startswith("# ")), None)
        out.append({"path": rel, "title": first})
    return out


# ---------- harness result records ----------
def results(repo: Repo, module_id: int) -> list[dict]:
    out = []
    for rel in repo.walk(f"assurance-harness/results/m{module_id:02d}"):
        try:
            record = json.loads(read_text(repo, rel) or "")
        except json.JSONDecodeError:
            out.append({"path": rel, "error": "not valid JSON"})
            continue
        for item in record if isinstance(record, list) else [record]:
            if isinstance(item, dict):
                out.append({"path": rel, **{k: item.get(k) for k in (
                    "control_id", "dataset", "population_size", "population_reconciled",
                    "exceptions", "exception_rate", "conclusion", "evidence_type", "run_at")}})
    return out


# ---------- lab ----------
def lab(repo: Repo, state: dict, module: dict) -> dict:
    slug = module["slug"]
    base = f"labs/{slug}"
    exists = MODULE_DIR.match(slug) is not None and (repo.root / "labs" / slug).is_dir()
    files = list(repo.walk(base)) if exists else []
    inside = [f[len(base) + 1:] for f in files]
    writable = slug in open_slugs(state)
    nn = f"{module['id']:02d}"

    authored = [{"group": "Incubation", "path": f"{base}/incubation/{n}"} for n in INCUBATION_FILES]
    procs = sorted(f for f in inside if f.startswith("procedures/") and PROCEDURE_FILE.match(f.split("/", 1)[1]))
    authored += [{"group": "Procedures", "path": f"{base}/{f}"} for f in procs]
    finds = sorted(f for f in inside if f.startswith("findings/") and FINDING_FILE.match(f.split("/", 1)[1]))
    if not finds:
        finds = [f"findings/F-{nn}-1.md"]
    authored += [{"group": "Finding", "path": f"{base}/{f}"} for f in finds]
    authored += [{"group": "Gate briefs", "path": f"{base}/gate/{n}"} for n in GATE_BRIEFS]
    for item in authored:
        item["exists"] = item["path"] in files

    return {
        "slug": slug, "exists": exists, "writable": writable and exists, "files": files,
        "pairs": _pairs(base, inside), "authored": authored if exists else [],
        "has_trace": "redteam/TRACE.md" in inside,
        "has_cold_attempt": "incubation/cold_attempt.md" in inside,
    }


def _pairs(base: str, inside: list[str]) -> list[dict]:
    """Contrastive pairs: two sibling folders under evidence/ whose names
    differ only by a trailing A or B. Which one is effective is not known
    to this code and is never shown."""
    groups: dict[tuple[str, str], dict[str, list[str]]] = {}
    for f in inside:
        parts = f.split("/")
        if parts[0] != "evidence":
            continue
        for depth in range(1, len(parts) - 1):
            m = PAIR_SUFFIX.match(parts[depth])
            if m:
                key = ("/".join(parts[:depth]), m.group(1))
                groups.setdefault(key, {}).setdefault(m.group(2), []).append("/".join(parts[depth:]))
                break
    out = []
    for (parent, stem), sides in sorted(groups.items()):
        if set(sides) != {"A", "B"}:
            continue
        dir_a, dir_b = sides["A"][0].split("/")[0], sides["B"][0].split("/")[0]
        names_a = {p.split("/", 1)[1] for p in sides["A"]}
        names_b = {p.split("/", 1)[1] for p in sides["B"]}
        out.append({
            "name": parent.split("/", 1)[1] if "/" in parent else stem,
            "a": f"{base}/{parent}/{dir_a}", "b": f"{base}/{parent}/{dir_b}",
            "files": sorted(names_a | names_b),
            "only_a": sorted(names_a - names_b), "only_b": sorted(names_b - names_a),
        })
    return out


def file_payload(repo: Repo, rel: str, state: dict) -> dict:
    """One readable file, with its hash for the stale-write check."""
    path = repo.read_path(rel)
    data = read_bytes(path)
    try:
        repo.write_path(rel, open_slugs(state))
        writable = True
    except PathRefused:
        writable = False
    if data is None:
        if not writable:
            raise FileNotFoundError(rel)
        return {"path": rel, "exists": False, "content": "", "sha256": None,
                "writable": True, "front_matter": None, "body": ""}
    text = data.decode("utf-8", errors="replace")
    meta, body = split_front_matter(text) if rel.endswith(".md") else (None, text)
    return {"path": rel, "exists": True, "content": text, "sha256": sha256(data),
            "writable": writable, "front_matter": meta, "body": body}
