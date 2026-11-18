"""Subprocess calls. Every command line is built here from fixed pieces.
No request value is ever placed on a command line: the only thing a request
chooses is which of the named commands below to run."""
from __future__ import annotations

import asyncio
import codecs
import json
import os
import shutil
import subprocess
import tempfile
import threading
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import AsyncIterator, Callable

from .paths import Repo

NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


class Unavailable(Exception):
    """A required tool is missing. The message is shown to the learner as is."""


def find_bash() -> str | None:
    """bash on macOS and Linux; Git Bash on Windows (never the WSL launcher)."""
    if os.name != "nt":
        return shutil.which("bash")
    candidates: list[Path] = []
    git = shutil.which("git")
    if git:
        real = Path(git).resolve()
        candidates += [real.parents[1] / "bin" / "bash.exe", real.parents[2] / "bin" / "bash.exe"]
    for var, sub in (("ProgramFiles", "Git"), ("ProgramFiles(x86)", "Git"), ("LOCALAPPDATA", "Programs/Git")):
        base = os.environ.get(var)
        if base:
            candidates.append(Path(base) / sub / "bin" / "bash.exe")
    return next((str(c) for c in candidates if c.is_file()), None)


def _uv() -> str:
    uv = shutil.which("uv")
    if not uv:
        raise Unavailable("uv was not found on PATH. Install uv (https://docs.astral.sh/uv/), then restart Mission Control.")
    return uv


def _bash() -> str:
    bash = find_bash()
    if not bash:
        raise Unavailable("Git Bash was not found. Install Git for Windows (it includes Git Bash), then restart Mission Control."
                          if os.name == "nt" else "bash was not found on PATH.")
    return bash


def harness_target(repo: Repo, module_id: int) -> str:
    """The current module's tests if that folder exists, else the whole harness."""
    narrowed = f"assurance-harness/m{int(module_id):02d}"
    return narrowed if (repo.root / narrowed).is_dir() else "assurance-harness"


def harness_command(repo: Repo, module_id: int, junit: Path) -> list[str]:
    # `make test`: uv run --frozen python -m pytest assurance-harness
    return [_uv(), "run", "--frozen", "python", "-m", "pytest",
            harness_target(repo, module_id), f"--junitxml={junit}"]


def validate_command() -> list[str]:
    return [_uv(), "run", "--frozen", "python", "scripts/validate_state.py"]


def sync_command(which: str) -> list[str]:
    script = {"sync_down": "scripts/sync_down.sh", "sync_up": "scripts/sync_up.sh"}[which]
    return [_bash(), script]


def git_status(repo: Repo) -> list[str]:
    """What `git add -A` in sync_up.sh would stage. Read-only."""
    git = shutil.which("git")
    if not git:
        raise Unavailable("git was not found on PATH.")
    done = subprocess.run([git, "status", "--porcelain=v1", "--untracked-files=all"], cwd=repo.root,
                          capture_output=True, text=True, encoding="utf-8", errors="replace",
                          timeout=30, creationflags=NO_WINDOW)
    if done.returncode != 0:
        raise Unavailable(done.stderr.strip() or "git status failed")
    return [line for line in done.stdout.splitlines() if line.strip()]


def run_capture(repo: Repo, cmd: list[str], timeout: int = 120) -> tuple[int, str]:
    done = subprocess.run(cmd, cwd=repo.root, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout, env=_env(), creationflags=NO_WINDOW)
    return done.returncode, (done.stdout + done.stderr).strip()


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env.update({"NO_COLOR": "1", "PY_COLORS": "0", "PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8"})
    env.pop("FORCE_COLOR", None)
    return env


def parse_junit(path: Path) -> list[dict]:
    """Per-test outcomes from pytest's own report."""
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError):
        return []
    tests = []
    for case in root.iter("testcase"):
        outcome = "pass"
        if case.find("failure") is not None:
            outcome = "fail"
        elif case.find("error") is not None:
            outcome = "error"
        elif case.find("skipped") is not None:
            outcome = "skip"
        tests.append({"file": case.get("classname", ""), "name": case.get("name", ""), "outcome": outcome})
    return tests


async def stream(repo: Repo, cmd: list[str], finish: Callable[[int], dict] | None = None) -> AsyncIterator[bytes]:
    """Run cmd from the repo root and yield NDJSON lines:
    {"t":"out","d":text} as output arrives, then {"t":"exit","code":n,...}."""
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue = asyncio.Queue()
    holder: dict[str, subprocess.Popen] = {}

    def put(item):
        loop.call_soon_threadsafe(queue.put_nowait, item)

    def pump():
        try:
            proc = subprocess.Popen(cmd, cwd=repo.root, env=_env(), stdin=subprocess.DEVNULL,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0,
                                    creationflags=NO_WINDOW)
        except OSError as exc:
            put(("out", f"could not start: {exc}\n".encode()))
            put(("exit", 127))
            return
        holder["proc"] = proc
        while True:
            chunk = proc.stdout.read(4096)
            if not chunk:
                break
            put(("out", chunk))
        put(("exit", proc.wait()))

    threading.Thread(target=pump, daemon=True).start()
    decoder = codecs.getincrementaldecoder("utf-8")("replace")
    line = lambda obj: (json.dumps(obj) + "\n").encode("utf-8")
    try:
        while True:
            kind, data = await queue.get()
            if kind == "out":
                text = decoder.decode(data).replace("\r\n", "\n")
                if text:
                    yield line({"t": "out", "d": text})
            else:
                extra = finish(data) if finish else {}
                yield line({"t": "exit", "code": data, **extra})
                return
    finally:
        proc = holder.get("proc")
        if proc and proc.poll() is None:
            proc.terminate()


def junit_tempfile() -> Path:
    fd, name = tempfile.mkstemp(prefix="mission-control-junit-", suffix=".xml")
    os.close(fd)
    return Path(name)
