"""Repo-to-app change notifications.

A file watcher (watchfiles) drives server-sent events. Every directory is
watched non-recursively and blocked directories are skipped, so sealed folders
never get a watch handle. If the watcher cannot run, a polling loop over the
same directories takes over. Either way events are debounced, and the client
only ever learns which *topics* changed, never file contents.
"""
from __future__ import annotations

import asyncio
import os
from pathlib import Path

from .paths import PathRefused, Repo, never, split

WATCH_TOPS = ("labs", "flashcards", "portfolio", "assurance-harness", "spec", "literature")
ROOT_FILES = {"STATE.json", "HEURISTICS.md"}
DEBOUNCE_MS = 400
POLL_SECONDS = 2.0


def topic_for(rel: str) -> str | None:
    """Map a changed path to a UI topic. None means: not something the app shows."""
    try:
        parts = split(rel)
        never(parts)
    except PathRefused:
        return None
    if rel.endswith(".tmp"):
        return None
    if len(parts) == 1:
        return {"STATE.json": "state", "HEURISTICS.md": "heuristics"}.get(parts[0])
    top = parts[0]
    if top == "labs":
        return "lab"
    if top in ("flashcards", "portfolio", "literature"):
        return top
    if top == "assurance-harness":
        return "results" if len(parts) > 1 and parts[1] == "results" else "harness"
    if top == "spec":
        return "curriculum"
    return None


class Hub:
    """Fans change events out to every connected browser tab."""

    def __init__(self):
        self.queues: set[asyncio.Queue] = set()

    def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=64)
        self.queues.add(q)
        return q

    def unsubscribe(self, q: asyncio.Queue) -> None:
        self.queues.discard(q)

    def publish(self, topics: set[str]) -> None:
        if not topics:
            return
        for q in list(self.queues):
            try:
                q.put_nowait(sorted(topics))
            except asyncio.QueueFull:
                pass


def _snapshot(repo: Repo) -> dict[str, tuple[int, int]]:
    snap: dict[str, tuple[int, int]] = {}
    for directory in repo.watch_dirs(WATCH_TOPS):
        try:
            entries = list(os.scandir(directory))
        except OSError:
            continue
        for entry in entries:
            try:
                if not entry.is_file(follow_symlinks=False):
                    continue
                rel = Path(entry.path).relative_to(repo.root).as_posix()
                if directory == repo.root and entry.name not in ROOT_FILES:
                    continue
                st = entry.stat(follow_symlinks=False)
                snap[rel] = (st.st_mtime_ns, st.st_size)
            except (OSError, ValueError):
                continue
    return snap


async def _poll(repo: Repo, hub: Hub, stop: asyncio.Event) -> None:
    before = await asyncio.to_thread(_snapshot, repo)
    while not stop.is_set():
        try:
            await asyncio.wait_for(stop.wait(), timeout=POLL_SECONDS)
            return
        except asyncio.TimeoutError:
            pass
        after = await asyncio.to_thread(_snapshot, repo)
        changed = {p for p in set(before) | set(after) if before.get(p) != after.get(p)}
        before = after
        hub.publish({t for t in map(topic_for, changed) if t})


async def _watch(repo: Repo, hub: Hub, stop: asyncio.Event) -> None:
    from watchfiles import awatch

    force_polling = os.environ.get("MISSION_CONTROL_POLL") == "1"
    while not stop.is_set():
        dirs = await asyncio.to_thread(repo.watch_dirs, WATCH_TOPS)
        watched = {str(d) for d in dirs}
        restart = False
        async for changes in awatch(*dirs, recursive=False, debounce=DEBOUNCE_MS, step=100,
                                    stop_event=stop, force_polling=force_polling,
                                    watch_filter=None):
            topics: set[str] = set()
            for _, raw in changes:
                path = Path(raw)
                try:
                    rel = path.relative_to(repo.root).as_posix()
                except ValueError:
                    continue
                if path.parent == repo.root and path.name not in ROOT_FILES:
                    # A new or removed top-level folder: re-plan the watch set.
                    if path.name in WATCH_TOPS:
                        restart = True
                    continue
                topic = topic_for(rel)
                if topic is None:
                    continue
                if path.is_dir() or str(path) in watched:
                    restart = True   # folder created or removed: re-plan
                    topics.add(topic)
                    continue
                topics.add(topic)
            hub.publish(topics)
            if restart:
                break


async def run(repo: Repo, hub: Hub, stop: asyncio.Event) -> None:
    """Watch until stopped. Falls back to polling if the watcher fails."""
    try:
        await _watch(repo, hub, stop)
    except asyncio.CancelledError:
        raise
    except Exception:
        await _poll(repo, hub, stop)
