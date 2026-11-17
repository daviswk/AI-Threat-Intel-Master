"""Verify that each subagent is served by the model in its frontmatter.

A bad or unavailable model ID usually does not error; it silently falls back to
another model. So this check launches a headless Claude Code session on a main
model that differs from every subagent's model, has it invoke each subagent on
a trivial task, and reads which model actually produced each subagent's reply.
A mismatch is a failure even if the task succeeded.

Usage (from the repo root):
    uv run python scripts/verify_routing.py
    uv run python scripts/verify_routing.py --main-model claude-sonnet-5-5

Exit code 0 = every subagent served by its frontmatter model. 1 = mismatch or error.
Re-run whenever a model ID changes. Record the result in spec/PHASE0.md and STATE.json.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / ".claude" / "agents"
TASK = (
    "Routing check only. Do not create or modify any files. Run ls in the current "
    "directory with Bash and reply with exactly one line: the number of entries you saw."
)


def expected_models() -> dict[str, str]:
    out: dict[str, str] = {}
    for path in sorted(AGENTS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
        if not m:
            sys.exit(f"{path.name}: no frontmatter")
        fm = dict(
            (k.strip(), v.strip())
            for k, v in (line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
        )
        if "name" not in fm or "model" not in fm:
            sys.exit(f"{path.name}: frontmatter needs both name: and model:")
        out[fm["name"]] = fm["model"]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--main-model", default="claude-sonnet-5-5",
                    help="model for the throwaway main session; must differ from every subagent model")
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()

    if os.environ.get("CLAUDE_CODE_SUBAGENT_MODEL"):
        print("FAIL: CLAUDE_CODE_SUBAGENT_MODEL is set; it overrides frontmatter. Unset it.")
        return 1

    expected = expected_models()
    if not expected:
        print("FAIL: no agents found in", AGENTS_DIR)
        return 1
    if "socratic-tutor" in expected:
        print("FAIL: a socratic-tutor agent exists. The tutor runs inline, never as a subagent.")
        return 1
    if args.main_model in expected.values():
        print(f"FAIL: --main-model {args.main_model} equals a subagent model, so inheritance "
              "could not be told apart from correct routing. Pick a different main model.")
        return 1

    claude = shutil.which("claude")
    if not claude:
        print("FAIL: claude CLI not found on PATH")
        return 1

    names = ", ".join(expected)
    prompt = (
        f"Routing check. Invoke each of these subagents once, one after another, each with "
        f"this exact task: '{TASK}' The subagents are: {names}. Then reply with one line per "
        f"subagent giving what it returned. Do nothing else."
    )
    env = {k: v for k, v in os.environ.items()
           if k not in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SUBAGENT_MODEL")}
    cmd = [claude, "-p", prompt, "--model", args.main_model,
           "--output-format", "stream-json", "--verbose",
           "--allowedTools", "Agent", "Task", "Bash(ls:*)"]
    try:
        proc = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=args.timeout)
    except subprocess.TimeoutExpired:
        print("FAIL: headless session timed out")
        return 1

    calls: dict[str, str] = {}
    served: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    main_models: collections.Counter = collections.Counter()
    loaded_agents: list[str] = []
    for line in proc.stdout.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        kind = ev.get("type")
        if kind == "system" and ev.get("subtype") == "init":
            loaded_agents = ev.get("agents") or []
        elif kind == "assistant":
            msg = ev.get("message", {})
            parent = ev.get("parent_tool_use_id")
            if parent:
                served[parent][msg.get("model")] += 1
            else:
                main_models[msg.get("model")] += 1
                for block in msg.get("content", []):
                    if block.get("type") == "tool_use" and block.get("name") in ("Agent", "Task"):
                        calls[block["id"]] = block.get("input", {}).get("subagent_type")

    print(f"main session served by: {dict(main_models) or 'nothing (session failed)'}")
    if proc.returncode != 0:
        print(f"FAIL: claude exited {proc.returncode}: {proc.stderr.strip()[:400]}")
        return 1

    by_agent: dict[str, set] = collections.defaultdict(set)
    for call_id, agent in calls.items():
        by_agent[agent].update(served.get(call_id, {}))

    ok = True
    print(f"{'subagent':<22}{'frontmatter model':<24}{'served by':<28}result")
    for agent, want in expected.items():
        if agent not in loaded_agents:
            print(f"{agent:<22}{want:<24}{'(agent not loaded)':<28}FAIL")
            ok = False
            continue
        got = by_agent.get(agent, set())
        verdict = "PASS" if got == {want} else "FAIL"
        ok &= verdict == "PASS"
        print(f"{agent:<22}{want:<24}{(', '.join(sorted(map(str, got))) or '(never invoked)'):<28}{verdict}")
    print("ROUTING VERIFIED" if ok else "ROUTING NOT VERIFIED: do not substitute a model; ask the learner.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
