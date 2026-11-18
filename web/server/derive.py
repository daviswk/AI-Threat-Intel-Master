"""Everything the UI shows as progress is computed here, per request, from the
repo: STATE.json, the flashcard files, HEURISTICS.md, the lab folder. Nothing
is stored and nothing is awarded."""
from __future__ import annotations

from . import content
from .curriculum import STAGES
from .paths import Repo

GATE_CHECKS = ["edge_case", "pushback", "compression", "artifact_check"]


def overview(repo: Repo, state: dict, edge_list: list[list[int]]) -> dict:
    cards = content.flashcards(repo)
    heur = content.heuristics(repo)
    current = state["current_module"]
    modules = []
    for m in state["modules"]:
        mine = [c for c in cards if c["module"] == m["id"]]
        heur_n = sum(1 for h in heur["entries"] if h["module"] == m["id"])
        status = "complete" if m["status"] == "complete" else "locked" if m["status"] == "locked" else "active"
        stage = "complete" if status == "complete" else state["current_stage"] if m["id"] == current else None
        spent, box = m["hours_spent"], m["timebox_hours"]
        notes = []
        if m["flashcards_count"] != len(mine):
            notes.append(f"STATE.json says {m['flashcards_count']} flashcards; flashcards/m{m['id']:02d}.csv has {len(mine)}.")
        if m["heuristics_added"] != heur_n:
            notes.append(f"STATE.json says {m['heuristics_added']} heuristics; HEURISTICS.md has {heur_n} for this module.")
        modules.append({
            "id": m["id"], "slug": m["slug"], "title": m["title"], "status": status, "stage": stage,
            "stage_index": STAGES.index(stage) if stage else -1,
            "stage_history": m["stage_history"],
            "hours_spent": spent, "timebox_hours": box,
            "burn_pct": min(100.0, 100.0 * spent / box), "over_hours": max(0.0, spent - box),
            "at_cut_line": spent >= 0.8 * box,
            "gate": m["gate"], "outputs": m["outputs"], "nice_to_haves_cut": m["nice_to_haves_cut"],
            "expanded": m["expanded"],
            "cards": len(mine), "certs": content.cert_counts(mine), "heuristics": heur_n,
            "notes": notes,
        })
    return {
        "current_module": current, "current_stage": state["current_stage"], "updated": state["updated"],
        "stages": STAGES, "modules": modules, "edges": edge_list,
        "totals": {
            "modules_complete": sum(1 for m in modules if m["status"] == "complete"),
            "modules": len(modules),
            "hours_logged": sum(e["hours"] for e in state["time_log"]),
            "hours_planned": sum(m["timebox_hours"] for m in state["modules"]),
            "cards": len(cards), "heuristics": len(heur["entries"]),
            "certs": content.cert_counts(cards),
        },
    }


def _prompt(module_id: int, stage: str, tail: str) -> str:
    return f"Module {module_id:02d}, stage {stage}. {tail}"


def prompts(module_id: int, stage: str) -> list[dict]:
    """Fixed templates for work that happens in Claude Code. Each names the
    module and the stage and points at spec/MODULE_LOOP.md. None carries a
    summary of the learner's work, app state, or a hint about a verdict."""
    loop = "spec/MODULE_LOOP.md"
    if stage == "gate":
        return [
            {"id": "gate_edge_case", "label": "Check 1: edge case",
             "text": _prompt(module_id, stage, f"Run gate check 1 (first-principles edge case) as described in {loop}, stage 5.")},
            {"id": "gate_pushback", "label": "Check 2: pushback",
             "text": _prompt(module_id, stage, f"Run gate check 2 (1st-line pushback) as described in {loop}, stage 5.")},
            {"id": "gate_compression", "label": "Check 3: review briefs",
             "text": _prompt(module_id, stage, f"Run gate check 3 (four-tier compression) as described in {loop}, stage 5.")},
            {"id": "gate_artifact_check", "label": "Check 4: grader",
             "text": _prompt(module_id, stage, f"Run gate check 4 (artifact check) as described in {loop}, stage 5, using the grader handoff template there unchanged.")},
        ]
    if stage == "lab":
        return [
            {"id": "lab_continue", "label": "Continue the lab",
             "text": _prompt(module_id, stage, f"Continue this stage as described in {loop}, stage 3.")},
            {"id": "lab_procedure_to_code", "label": "Procedure to code",
             "text": _prompt(module_id, stage, f"I have written a procedure in prose. Follow {loop}, stage 3, rules for 3.3.")},
        ]
    if stage == "complete":
        return []
    number = STAGES.index(stage)
    return [{"id": f"{stage}_continue", "label": "Continue this stage",
             "text": _prompt(module_id, stage, f"Continue this stage as described in {loop}, stage {number}.")}]


def banner(stage: str, lab: dict) -> dict:
    """What to do next and where. Wording is fixed per stage; the only inputs
    are the stage and whether a few named files exist."""
    base = f"labs/{lab['slug']}"
    if stage == "preflight":
        return {"where": "cli", "text": "Pre-flight runs in Claude Code: the module is expanded and its sources are verified and converted."}
    if stage == "incubation":
        if not lab["pairs"]:
            return {"where": "cli", "text": "The contrastive pair is not built yet. Claude Code builds it at the start of incubation."}
        if lab["has_cold_attempt"]:
            return {"where": "cli", "text": "Your cold attempt is on disk. Tell Claude Code you are ready to move on."}
        return {"where": "app", "text": "Open both artifacts in the workbench, then write your diagnosis and test procedure cold.",
                "open": f"{base}/incubation/cold_attempt.md", "open_label": "Open cold attempt"}
    if stage == "ingestion":
        return {"where": "cli", "text": "Ingestion is taught by question in Claude Code. This module's papers are in the Papers tab."}
    if stage == "lab":
        if not lab["has_trace"]:
            return {"where": "cli", "text": "Lab steps 3.1 and 3.2 run as subagents in Claude Code. Step 3.3 is yours once the red-team trace exists."}
        return {"where": "app", "text": "Step 3.3 is yours. Write each procedure in prose before any code, then run the harness.",
                "open_tab": "write", "open_label": "Open my files"}
    if stage == "heuristics":
        return {"where": "app", "text": "Add your heuristics in the workbench. Flashcards and the portfolio piece are written with Claude Code.",
                "open_tab": "heuristic", "open_label": "Add a heuristic"}
    if stage == "gate":
        return {"where": "cli", "text": "Checks 1, 2 and 4 run in Claude Code. Write your four briefs here first.",
                "open": f"{base}/gate/a-raw-trace.md", "open_label": "Open briefs"}
    return {"where": "app", "text": "This module is complete."}
