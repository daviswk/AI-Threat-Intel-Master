"""Validate STATE.json against the schema embedded in spec/SCHEMAS.md.

Usage (from the repo root):
    uv run python scripts/validate_state.py

Exit code 0 = valid. 1 = schema violation or broken invariant.
The schema lives only in spec/SCHEMAS.md (fenced json block after the
`schema:state` marker). Do not copy it here.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_schema() -> dict:
    text = (ROOT / "spec" / "SCHEMAS.md").read_text(encoding="utf-8")
    m = re.search(r"<!-- schema:state -->\s*```json\s*\n(.*?)\n```", text, re.S)
    if not m:
        sys.exit("spec/SCHEMAS.md: no json block after the schema:state marker")
    return json.loads(m.group(1))


def invariants(state: dict) -> list[str]:
    errs: list[str] = []
    mods = state["modules"]
    cur = state["current_module"]
    spent = {m["id"]: 0.0 for m in mods}
    for entry in state["time_log"]:
        spent[entry["module"]] = spent.get(entry["module"], 0.0) + entry["hours"]
    for i, m in enumerate(mods):
        n = i + 1
        if m["id"] != n:
            errs.append(f"modules[{i}].id is {m['id']}, expected {n}")
            continue
        if not m["slug"].startswith(f"m{n:02d}-"):
            errs.append(f"module {n}: slug {m['slug']} does not start with m{n:02d}-")
        if n < cur and m["status"] != "complete":
            errs.append(f"module {n} precedes current module {cur} but is {m['status']}")
        if n > cur and m["status"] != "locked":
            errs.append(f"module {n} follows current module {cur} but is {m['status']}")
        if n == cur and m["status"] == "locked":
            errs.append(f"current module {n} is locked")
        gate_all_pass = all(m["gate"][k] == "pass"
                            for k in ("edge_case", "pushback", "compression", "artifact_check"))
        if m["status"] == "complete" and not gate_all_pass:
            errs.append(f"module {n} is complete but its gate is not all pass")
        if abs(m["hours_spent"] - spent[n]) > 1e-6:
            errs.append(f"module {n}: hours_spent {m['hours_spent']} != time_log sum {spent[n]}")
        if n != 3 and m["telemetry_source"] is not None:
            errs.append(f"module {n}: telemetry_source applies only to module 3")
        if n == 3 and m["status"] == "complete" and m["telemetry_source"] is None:
            errs.append("module 3 is complete but telemetry_source is null")
        stages = [s["stage"] for s in m["stage_history"]]
        if not m["expanded"] and any(s != "preflight" for s in stages):
            errs.append(f"module {n} is not expanded but has moved past preflight")
    cur_mod = mods[cur - 1]
    if cur_mod["stage_history"] and cur_mod["stage_history"][-1]["stage"] != state["current_stage"]:
        errs.append("current_stage does not match the last entry of the current module's stage_history")
    return errs


def main() -> int:
    state = json.loads((ROOT / "STATE.json").read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(load_schema())
    errors = [f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
              for e in validator.iter_errors(state)]
    if not errors:
        errors = invariants(state)
    if errors:
        print("STATE.json INVALID")
        for e in errors:
            print(" -", e)
        return 1
    total = sum(m["timebox_hours"] for m in state["modules"])
    print(f"STATE.json valid | module {state['current_module']} / {state['current_stage']} | "
          f"{total:g} h planned at {state['weekly_hours_budget']:g} h/week "
          f"= {total / state['weekly_hours_budget']:.1f} weeks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
