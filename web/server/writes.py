"""The only code that writes to the repo. It writes files the learner authors,
atomically, and refuses when the file on disk is not the one the editor loaded."""
from __future__ import annotations

import os
import secrets
from pathlib import Path

from . import content
from .paths import Repo

MAX_WRITE_CHARS = 1_000_000


class Stale(Exception):
    """The file changed on disk since it was loaded."""

    def __init__(self, disk: bytes | None):
        super().__init__("file changed on disk")
        self.disk = disk


class BadInput(Exception):
    pass


def _normalise(text: str) -> bytes:
    if not isinstance(text, str) or len(text) > MAX_WRITE_CHARS:
        raise BadInput("content is missing or too large")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text and not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8")


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{secrets.token_hex(6)}.tmp")
    try:
        with open(tmp, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def _check_base(path: Path, base_sha256: str | None) -> bytes | None:
    disk = content.read_bytes(path)
    disk_sha = None if disk is None else content.sha256(disk)
    if disk_sha != base_sha256:
        raise Stale(disk)
    return disk


def save_authored(repo: Repo, state: dict, rel: str, text: str, base_sha256: str | None) -> dict:
    path = repo.write_path(rel, content.open_slugs(state))
    data = _normalise(text)
    _check_base(path, base_sha256)
    _atomic_write(path, data)
    return {"path": rel, "sha256": content.sha256(data)}


def append_heuristic(repo: Repo, state: dict, pattern: str, verify: str, evidence: str,
                     base_sha256: str | None) -> dict:
    """Append one entry in the spec/SCHEMAS.md §5 format. The module comes
    from STATE.json, never from the request."""
    fields = []
    for value in (pattern, verify, evidence):
        if not isinstance(value, str) or not value.strip() or len(value) > 600 or "\n" in value.strip() or "\r" in value:
            raise BadInput("each field must be one non-empty line")
        fields.append(" ".join(value.split()))
    pattern, verify, evidence = fields
    module_id = state["current_module"]
    path = repo.read_path("HEURISTICS.md")
    disk = _check_base(path, base_sha256)
    if disk is None:
        raise BadInput("HEURISTICS.md does not exist")
    existing = content.heuristics(repo)["entries"]
    n = max([h["n"] for h in existing if h["module"] == module_id], default=0) + 1
    entry_id = f"H-{module_id:02d}-{n}"
    entry = (f"### {entry_id}  (Module {module_id:02d})\n"
             f"If {pattern.rstrip('.')} → then verify {verify.rstrip('.')}.\n"
             f"Evidence: {evidence}\n")
    text = disk.decode("utf-8").replace("\r\n", "\n")
    data = (text.rstrip("\n") + "\n\n" + entry).encode("utf-8")
    _atomic_write(path, data)
    return {"id": entry_id, "sha256": content.sha256(data)}
