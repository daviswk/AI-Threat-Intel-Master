"""Builds a throwaway repo shaped like the real one. Used by the tests and by
manual end-to-end checks. It never touches the real repo."""
from __future__ import annotations

import json
from pathlib import Path

TOKEN = "test-token-for-this-launch"
PORT = 8765
SLUG = "m01-test-module"
CANARY = "SEALED-CANARY-7f3a"
PAIR_SECRET = "PAIR-DETAIL-CANARY-91c2"
BUILDER_SECRET = "BUILDER-BRIEF-CANARY-55d0"


def state() -> dict:
    gate = {"edge_case": "pending", "pushback": "pending", "compression": "pending",
            "artifact_check": "pending", "attempts": 0}
    modules = []
    for i in range(1, 13):
        modules.append({
            "id": i, "slug": SLUG if i == 1 else f"m{i:02d}-later-module", "title": f"Module {i}",
            "status": "in_progress" if i == 1 else "locked", "expanded": i == 1,
            "expanded_on": "2026-11-17" if i == 1 else None, "timebox_hours": 16, "hours_spent": 0,
            "stage_history": [{"stage": "preflight", "entered_on": "2026-11-17"},
                              {"stage": "incubation", "entered_on": "2026-11-17"}] if i == 1 else [],
            "gate": dict(gate), "outputs": [], "nice_to_haves_cut": [], "telemetry_source": None,
            "flashcards_count": 0, "heuristics_added": 0,
        })
    return {"schema_version": 1, "created": "2026-11-17", "updated": "2026-11-17",
            "weekly_hours_budget": 8, "current_module": 1, "current_stage": "incubation",
            "modules": modules, "time_log": [], "parked": [], "contract_changes": []}


def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def build(tmp_path: Path) -> Path:
    """Create <tmp_path>/repo and return it."""
    root = tmp_path / "repo"
    lab = f"labs/{SLUG}"
    write(root, "STATE.json", json.dumps(state(), indent=2))
    write(root, "HEURISTICS.md", "# Heuristics Codex\n\n---\n\n<!-- entries start below this line -->\n")
    write(root, "spec/CURRICULUM.md", "\n".join([
        "# Curriculum", "", "# Module 1: Test module", "", "**Slug:** `m01-test-module`", "",
        "## I/O contract (frozen)", "", "Input: none.", "",
        "## Stage 1: dilemma and contrastive pair", "",
        "**Dilemma.** A visible dilemma paragraph.", "",
        f"**Contrastive pair.** {PAIR_SECRET}", "",
        "## Stage 3: lab design", "", "Lab folder.", "",
        "### 3.1 First line (`first-line-engineer`)", "", BUILDER_SECRET, "",
        "# Modules 2–12: I/O contracts", "", "## Module 2: Later", "", "- **Input (from M1):** something.", ""]))
    write(root, "spec/MODULE_LOOP.md", "\n".join([
        "# Loop", "", "## Stage 1: `incubation`", "", "Write the cold attempt.", "",
        "## Stage 2: `ingestion`", "", "Extract the new concepts.", ""]))
    write(root, f"{lab}/README.md", "# Lab readme\n")
    write(root, f"{lab}/.sealed/ANSWER_KEY.md", CANARY + "\n")
    write(root, f"{lab}/data/planted_notes.txt", CANARY + "\n")
    write(root, f"{lab}/evidence/q3/package_A/decisions.csv", "id,decision\n1,keep\n2,keep\n")
    write(root, f"{lab}/evidence/q3/package_B/decisions.csv", "id,decision\n1,keep\n2,revoke\n")
    write(root, "assurance-harness/generators/sealed_m01.py", f"# {CANARY}\n")
    write(root, "assurance-harness/generators/m01_gen.py", f"# {CANARY}\n")
    write(root, "assurance-harness/results/m01/C-1.json",
          json.dumps({"control_id": "C-1", "dataset": "clean", "exceptions": 0, "conclusion": "effective"}))
    write(root, "flashcards/m01.csv", '#separator:Comma\n"Front","Back","m01 CISA::D1"\n')
    write(root, "literature/m01/sample-paper.md",
          "---\ntitle: Sample paper\npublisher: Nobody\nretrieved: 2026-11-17\n---\n\n# Sample\n\n<script>window.pwned = true</script>\n\nBody text.\n")
    write(root, ".git/config", f"[core]\n# {CANARY}\n")
    write(root, ".env", f"SECRET={CANARY}\n")
    write(tmp_path, "outside-secret.txt", CANARY + "\n")
    return root
