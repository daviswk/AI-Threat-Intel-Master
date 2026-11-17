#!/usr/bin/env bash
# Re-hydrate this repo on a freshly cloned machine. Idempotent: safe to re-run.
#
#   bash scripts/bootstrap_laptop.sh                 # full run
#   bash scripts/bootstrap_laptop.sh --skip-routing  # offline / no Claude login yet
#
# What it does:
#   1. Checks prerequisites (git, uv or Python, the claude CLI).
#   2. Creates .venv and installs exactly the locked packages.
#   3. Validates STATE.json and checks the repo for machine-specific paths.
#   4. Rebuilds local data (DuckDB tables, synthetic telemetry) from seeded
#      generators. Nothing rebuilt here is tracked in Git.
#   5. Runs the assurance harness.
#   6. Re-runs the Phase 0 environment audit and the model-routing check on this
#      machine and writes a "Laptop Environment" section into spec/PHASE0.md
#      (replaced on re-run, never duplicated).
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/_lib.sh"

SKIP_ROUTING=0
LABEL="Laptop Environment"
while [ $# -gt 0 ]; do
  case "$1" in
    --skip-routing) SKIP_ROUTING=1 ;;
    --label) shift; LABEL="$1" ;;
    *) die "unknown argument: $1" ;;
  esac
  shift
done

step "1/6 Prerequisites"
command -v git >/dev/null 2>&1 || die "git not found"
echo "git:    $(git --version)"
if command -v uv >/dev/null 2>&1; then echo "uv:     $(uv --version)"; else warn "uv not found (pip fallback will be used)"; fi
if command -v claude >/dev/null 2>&1; then
  echo "claude: $(claude --version 2>/dev/null || echo 'installed')"
else
  warn "claude CLI not found. Install Claude Code and log in before starting a session."
  SKIP_ROUTING=1
fi
if [ -n "${CLAUDE_CODE_SUBAGENT_MODEL:-}" ]; then
  die "CLAUDE_CODE_SUBAGENT_MODEL is set. Unset it: it silently overrides subagent models."
fi
[ -f .claude/skills/socratic-tutor/SKILL.md ] || die "vendored socratic-tutor skill is missing from .claude/skills/"
[ ! -e .claude/agents/socratic-tutor.md ] || die "a socratic-tutor agent exists; the tutor must run inline"

step "2/6 Python environment (locked)"
ensure_env
py -c "import sys; print('python:', sys.version.split()[0])"

step "3/6 State and portability"
py scripts/validate_state.py
py scripts/check_portable.py

step "4/6 Re-hydrate local data (seeded generators)"
py scripts/rehydrate.py

step "5/6 Assurance harness"
run_harness

step "6/6 Phase 0 audit on this machine"
AUDIT_ARGS=(--label "$LABEL" --write)
if [ "$SKIP_ROUTING" -eq 1 ]; then AUDIT_ARGS+=(--skip-routing); fi
py scripts/phase0_audit.py "${AUDIT_ARGS[@]}"

step "Ready"
where_am_i
echo "Next: run 'claude' in this folder. It reads STATE.json and resumes."
if ! git diff --quiet -- spec/PHASE0.md 2>/dev/null; then
  echo "spec/PHASE0.md gained this machine's audit; '/sync-up' (or 'bash scripts/sync_up.sh') will commit it."
fi
