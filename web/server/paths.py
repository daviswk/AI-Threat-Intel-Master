"""Path policy. Every file the backend touches goes through this module.

Three layers, applied in order to the requested path and again to whatever it
resolves to on disk (so a link or a Windows short name cannot sidestep them):

1. shape    repo-relative, forward slashes, no traversal, no drive or root
2. never    sealed material, hidden paths, generators, bulk data, secrets
3. allow    an explicit read allowlist; a narrower write allowlist
"""
from __future__ import annotations

import fnmatch
import os
import re
from pathlib import Path, PurePosixPath
from typing import Callable, Iterable, Iterator


class PathRefused(Exception):
    """The path is not one the app may touch. `reason` is safe to show."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


MODULE_DIR = re.compile(r"^m(\d{2})-[a-z0-9-]+$")
MODULE_SHORT = re.compile(r"^m\d{2}$")
TEXT_SUFFIXES = {".md", ".csv", ".json", ".txt", ".yaml", ".yml"}
SECRET_GLOBS = (
    ".env", ".env.*", "*.pem", "*.key", "*.p12", "*credentials*.json",
    "*service-account*.json", "*-sa-key*.json", "*.tfstate", "*.tfstate.*", "*.tfvars",
)
READ_FILES = {
    ("STATE.json",), ("HEURISTICS.md",), ("spec", "CURRICULUM.md"),
    ("spec", "MODULE_LOOP.md"), ("literature", "SOURCES.md"),
}
LAB_READ_FILES = {"README.md", "SYSTEM.md", "NOTES.md"}
LAB_READ_DIRS = {"evidence", "incubation", "procedures", "findings", "gate", "redteam", "register"}

# Files the learner authors. Paths come from spec/MODULE_LOOP.md (stages 1, 3
# and 5) and spec/SCHEMAS.md §3. The four brief names are the ones the learner
# approved; the spec fixes only their folder.
INCUBATION_FILES = ("cold_attempt.md", "retrospective.md")
GATE_BRIEFS = ("a-raw-trace.md", "b-engineer-walkthrough.md", "c-legal-brief.md", "d-executive-pitch.md")
PROCEDURE_FILE = re.compile(r"^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-(?:tod|toe)\.md$")
FINDING_FILE = re.compile(r"^F-(\d{2})-\d{1,3}\.md$")


def split(rel: object) -> tuple[str, ...]:
    """Shape check. Returns the path's parts or raises PathRefused."""
    if not isinstance(rel, str) or not rel or len(rel) > 400:
        raise PathRefused("empty or overlong path")
    if "\x00" in rel or "\\" in rel or ":" in rel:
        raise PathRefused("backslashes, drive letters and NUL are not allowed")
    if rel.startswith("/"):
        raise PathRefused("absolute paths are not allowed")
    parts = tuple(rel.split("/"))
    for part in parts:
        if part in ("", ".", ".."):
            raise PathRefused("path traversal is not allowed")
        if part != part.strip() or part.endswith(".") or "~" in part:
            raise PathRefused("ambiguous file name")
    return parts


def never(parts: Iterable[str]) -> None:
    """Refuse anything the app must not read, list, serve, watch or diff."""
    low = tuple(p.casefold() for p in parts)
    if any(p == ".sealed" or p.startswith("sealed_") for p in low):
        raise PathRefused("sealed material is never served")
    if any(p.startswith(".") for p in low):
        raise PathRefused("hidden paths are never served")
    if low[:2] in (("assurance-harness", "generators"), ("assurance-harness", "data")):
        raise PathRefused("generators and generated data are off-limits")
    if len(low) > 2 and low[0] == "labs" and low[2] == "data":
        raise PathRefused("generated lab data is off-limits")
    if any(fnmatch.fnmatchcase(low[-1], g) for g in SECRET_GLOBS):
        raise PathRefused("secrets are never served")


def is_blocked_name(name: str) -> bool:
    """True for a single directory or file name that `never` would refuse."""
    try:
        never((name,))
    except PathRefused:
        return True
    return False


def read_ok(parts: tuple[str, ...]) -> bool:
    n = len(parts)
    suffix = PurePosixPath(parts[-1]).suffix.lower()
    if parts in READ_FILES:
        return True
    if n == 3 and parts[0] == "literature" and MODULE_SHORT.match(parts[1]) and suffix == ".md":
        return True
    if n == 2 and parts[0] == "flashcards" and suffix == ".csv":
        return True
    if n == 2 and parts[0] == "portfolio" and suffix == ".md":
        return True
    if n == 4 and parts[:2] == ("assurance-harness", "results") and MODULE_SHORT.match(parts[2]) and suffix == ".json":
        return True
    if n >= 3 and parts[0] == "labs" and MODULE_DIR.match(parts[1]) and suffix in TEXT_SUFFIXES:
        return parts[2] in LAB_READ_FILES if n == 3 else parts[2] in LAB_READ_DIRS
    return False


def write_ok(parts: tuple[str, ...], open_slugs: Iterable[str]) -> bool:
    """Learner-authored files only, inside a lab whose module is not locked."""
    if len(parts) != 4 or parts[0] != "labs" or parts[1] not in set(open_slugs):
        return False
    slug = MODULE_DIR.match(parts[1])
    if not slug:
        return False
    folder, name = parts[2], parts[3]
    if folder == "incubation":
        return name in INCUBATION_FILES
    if folder == "procedures":
        return bool(PROCEDURE_FILE.match(name))
    if folder == "findings":
        m = FINDING_FILE.match(name)
        return bool(m) and m.group(1) == slug.group(1)
    if folder == "gate":
        return name in GATE_BRIEFS
    return False


class Repo:
    """A repository root plus the policy above."""

    def __init__(self, root: os.PathLike | str):
        self.root = Path(root).resolve()

    def _locate(self, rel: object, allowed: Callable[[tuple[str, ...]], bool]) -> Path:
        parts = split(rel)
        never(parts)
        if not allowed(parts):
            raise PathRefused("not on the allowlist")
        resolved = self.root.joinpath(*parts).resolve()
        try:
            back = tuple(resolved.relative_to(self.root).parts)
        except ValueError:
            raise PathRefused("resolves outside the repository") from None
        if tuple(p.casefold() for p in back) != tuple(p.casefold() for p in parts):
            # A link, junction or short name led somewhere else. Judge the target.
            never(back)
            if not allowed(back):
                raise PathRefused("link target is not on the allowlist")
        return resolved

    def read_path(self, rel: object) -> Path:
        return self._locate(rel, read_ok)

    def write_path(self, rel: object, open_slugs: Iterable[str]) -> Path:
        slugs = tuple(open_slugs)
        return self._locate(rel, lambda parts: write_ok(parts, slugs))

    def rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def walk(self, rel_dir: str) -> Iterator[str]:
        """Readable files under an allowlisted directory, as repo-relative
        paths. Blocked directories are pruned before they are entered, so
        sealed folders are never listed."""
        parts = split(rel_dir)
        never(parts)
        base = self.root.joinpath(*parts)
        if not base.is_dir() or base.is_symlink():
            return
        for current, dirs, files in os.walk(base, followlinks=False):
            dirs[:] = sorted(d for d in dirs if not is_blocked_name(d)
                             and not (Path(current) / d).is_symlink())
            for name in sorted(files):
                rel = (Path(current) / name).relative_to(self.root).as_posix()
                try:
                    self.read_path(rel)
                except PathRefused:
                    continue
                yield rel

    def watch_dirs(self, tops: Iterable[str]) -> list[Path]:
        """Every directory to watch, each non-recursively, with blocked
        directories left out. Sealed folders never get a watch handle."""
        out: list[Path] = [self.root]
        for top in tops:
            base = self.root / top
            if not base.is_dir() or base.is_symlink():
                continue
            for current, dirs, _ in os.walk(base, followlinks=False):
                cur = Path(current)
                rel_parts = cur.relative_to(self.root).parts
                try:
                    never(rel_parts + ("x",))
                except PathRefused:
                    dirs[:] = []
                    continue
                dirs[:] = [d for d in dirs if not is_blocked_name(d) and not (cur / d).is_symlink()]
                out.append(cur)
        return out
