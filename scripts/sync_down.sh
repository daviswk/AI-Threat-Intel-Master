#!/usr/bin/env bash
# sync-down: start-of-session handoff.
#   1. Pull the latest commits (fast-forward only).
#   2. Install locked packages (in case uv.lock changed).
#   3. Verify STATE.json.
#   4. Re-hydrate any missing local data artifacts.
# Works offline: a failed pull is reported and the rest still runs.
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/_lib.sh"

step "1/4 Pull"
if ! git remote get-url origin >/dev/null 2>&1; then
  warn "no 'origin' remote configured; skipping pull"
elif git pull --ff-only --autostash; then
  # --autostash sets local uncommitted edits aside, fast-forwards, and puts them back.
  :
else
  warn "pull failed (offline, or local and remote history diverged). Continuing with the local copy."
  warn "If you committed on two machines without syncing, resolve it by hand; nothing was overwritten."
fi

step "2/4 Python environment (locked)"
ensure_env

step "3/4 STATE.json integrity"
py scripts/validate_state.py

step "4/4 Re-hydrate missing local data"
py scripts/rehydrate.py

step "Position"
where_am_i
