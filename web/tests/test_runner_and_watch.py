"""The harness runner's plumbing and the file watcher, without needing uv.

    uv run python -m pytest web/tests -v
"""
from __future__ import annotations

import asyncio
import json
import subprocess
import sys
from pathlib import Path

from fixture_repo import SLUG
from server import runner, watch
from server.paths import Repo


def collect(repo: Repo, cmd: list[str], finish=None) -> list[dict]:
    async def go():
        return [json.loads(chunk) async for chunk in runner.stream(repo, cmd, finish)]
    return asyncio.run(go())


def test_stream_delivers_output_then_the_exit_code(repo_root):
    events = collect(Repo(repo_root), [sys.executable, "-c", "import sys; print('one'); print('two'); sys.exit(3)"])
    assert "".join(e["d"] for e in events if e["t"] == "out") == "one\ntwo\n"
    assert events[-1] == {"t": "exit", "code": 3}


def test_a_command_that_cannot_start_reports_instead_of_raising(repo_root):
    events = collect(Repo(repo_root), ["this-binary-does-not-exist-mc"])
    assert events[-1]["t"] == "exit" and events[-1]["code"] == 127


def test_flags_come_from_pytests_own_report(repo_root, tmp_path):
    """One passing and one failing test: only the passing one is 'pass'."""
    tests = tmp_path / "sample"
    tests.mkdir()
    (tests / "test_sample.py").write_text(
        "import pytest\n\n"
        "@pytest.mark.parametrize('dataset', ['planted', 'clean'])\n"
        "def test_reconciles(dataset):\n    assert dataset == 'clean'\n", encoding="utf-8")
    junit = tmp_path / "report.xml"
    done = subprocess.run([sys.executable, "-m", "pytest", str(tests), f"--junitxml={junit}", "-q",
                           "-p", "no:cacheprovider"], capture_output=True, text=True)
    assert done.returncode == 1
    outcomes = {t["name"]: t["outcome"] for t in runner.parse_junit(junit)}
    assert outcomes == {"test_reconciles[planted]": "fail", "test_reconciles[clean]": "pass"}


def test_harness_narrows_to_the_current_module_only_when_its_folder_exists(repo_root):
    repo = Repo(repo_root)
    assert runner.harness_target(repo, 1) == "assurance-harness"
    (repo_root / "assurance-harness" / "m01").mkdir()
    assert runner.harness_target(repo, 1) == "assurance-harness/m01"
    assert runner.harness_target(repo, 2) == "assurance-harness"


def test_watcher_reports_a_state_change_and_ignores_sealed_files(repo_root):
    repo = Repo(repo_root)
    hub = watch.Hub()

    async def go():
        stop = asyncio.Event()
        queue = hub.subscribe()
        task = asyncio.create_task(watch.run(repo, hub, stop))
        await asyncio.sleep(1.0)
        (repo_root / "labs" / SLUG / ".sealed" / "ANSWER_KEY.md").write_text("changed\n", encoding="utf-8")
        await asyncio.sleep(1.2)
        sealed_seen = not queue.empty()
        (repo_root / "STATE.json").write_text((repo_root / "STATE.json").read_text(encoding="utf-8") + "\n", encoding="utf-8")
        topics = await asyncio.wait_for(queue.get(), timeout=8)
        stop.set()
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        return sealed_seen, topics

    sealed_seen, topics = asyncio.run(go())
    assert not sealed_seen, "a change inside .sealed/ must not produce an event"
    assert "state" in topics


def test_polling_fallback_sees_the_same_change(repo_root):
    repo = Repo(repo_root)
    before = watch._snapshot(repo)
    assert "STATE.json" in before and "HEURISTICS.md" in before
    assert not [p for p in before if ".sealed" in p or "/data/" in p or "generators" in p or p.startswith(".")]
    (repo_root / "HEURISTICS.md").write_text("changed\n", encoding="utf-8")
    after = watch._snapshot(repo)
    changed = {p for p in after if before.get(p) != after[p]}
    assert {watch.topic_for(p) for p in changed} == {"heuristics"}
