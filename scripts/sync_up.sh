#!/usr/bin/env bash
# sync-up: end-of-session handoff.
#   1. Run pytest on the harness.
#   2. Verify STATE.json against spec/SCHEMAS.md.
#   3. Check for machine-specific paths and oversized files.
#   4. Commit all progress and push.
# Any failed check stops before the commit. If the push fails (offline), the
# commit is kept locally; re-run sync-up when you have a connection.
#
#   bash scripts/sync_up.sh ["optional commit message"]
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/_lib.sh"

MAX_BYTES=$((50 * 1024 * 1024))

step "1/4 Assurance harness"
ensure_env
run_harness || die "harness tests failed; nothing committed"

step "2/4 STATE.json"
py scripts/validate_state.py || die "STATE.json invalid; nothing committed"

step "3/4 Portability and size checks"
py scripts/check_portable.py || die "machine-specific paths found; nothing committed"
git add -A
while IFS= read -r -d '' f; do
  [ -f "$f" ] || continue
  size=$(wc -c < "$f")
  if [ "$size" -gt "$MAX_BYTES" ]; then
    git reset -q
    die "$f is $((size / 1024 / 1024)) MB. Weights, vector stores and databases are not tracked; add a .gitignore rule."
  fi
done < <(git diff --cached --name-only -z --diff-filter=AM)

step "4/4 Commit and push"
if ! git config user.name >/dev/null || ! git config user.email >/dev/null; then
  die "Git has no author identity on this machine. Set one for this repo, then re-run:
  git config user.name  \"Your Name\"
  git config user.email \"you@example.com\""
fi
if git diff --cached --quiet; then
  echo "nothing new to commit"
else
  MSG="${1:-$(py -c "import json,datetime;s=json.load(open('STATE.json',encoding='utf-8'));print(f\"progress: m{s['current_module']:02d} {s['current_stage']} ({datetime.date.today().isoformat()})\")")}"
  git commit -q -m "$MSG"
  echo "committed: $MSG"
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  warn "no 'origin' remote. Add one, then re-run:  git remote add origin <private-repo-url>"
  exit 0
fi
if git push -u origin HEAD; then
  echo "pushed"
else
  warn "push failed (offline?). Your commit is safe locally; re-run sync-up when connected."
  exit 1
fi
git status --short --branch
