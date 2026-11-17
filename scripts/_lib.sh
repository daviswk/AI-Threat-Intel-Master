#!/usr/bin/env bash
# Shared helpers for bootstrap_laptop.sh, sync_down.sh, sync_up.sh.
# Source this file; do not run it.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

step() { printf '\n== %s ==\n' "$1"; }
warn() { printf 'WARN: %s\n' "$1" >&2; }
die()  { printf 'FAIL: %s\n' "$1" >&2; exit 1; }

# ensure_env: create .venv and install exactly the locked packages.
# Prefers uv (uv.lock). Falls back to python -m venv + requirements.lock.
# Afterwards, run Python with:  py <args>
ensure_env() {
  if command -v uv >/dev/null 2>&1; then
    uv sync --frozen --quiet || die "uv sync failed (needs network the first time, to fetch wheels)"
    PY_MODE=uv
  else
    warn "uv not found; falling back to python -m venv + requirements.lock"
    local sys_py=""
    for c in python3.11 python3.12 python3 python; do
      if command -v "$c" >/dev/null 2>&1; then sys_py="$c"; break; fi
    done
    [ -n "$sys_py" ] || die "no Python found. Install uv (https://docs.astral.sh/uv/) or Python 3.11."
    if [ ! -d .venv ]; then "$sys_py" -m venv .venv || die "could not create .venv"; fi
    if [ -x .venv/bin/python ]; then VENV_PY=.venv/bin/python; else VENV_PY=.venv/Scripts/python.exe; fi
    "$VENV_PY" -m pip install --quiet -r requirements.lock || die "pip install from requirements.lock failed"
    PY_MODE=venv
  fi
}

py() {
  if [ "${PY_MODE:-}" = uv ]; then uv run --frozen python "$@"; else "$VENV_PY" "$@"; fi
}

# run_harness: pytest over assurance-harness. Exit code 5 means "no tests
# collected", which is expected before the first lab; treat it as success.
run_harness() {
  local rc=0
  py -m pytest assurance-harness || rc=$?
  if [ "$rc" -eq 5 ]; then echo "no harness tests yet (expected before the first lab)"; return 0; fi
  return "$rc"
}

where_am_i() {
  py -c "import json;s=json.load(open('STATE.json',encoding='utf-8'));m=s['modules'][s['current_module']-1];print(f\"Module {m['id']}: {m['title']} | stage: {s['current_stage']} | {m['hours_spent']:g} of {m['timebox_hours']:g} h used\")"
}
