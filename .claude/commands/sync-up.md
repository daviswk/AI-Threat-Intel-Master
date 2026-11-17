---
description: End-of-session handoff. Run the harness, validate STATE.json, commit all progress, push.
allowed-tools: Bash(bash scripts/sync_up.sh:*)
argument-hint: [optional commit message]
---

Before running anything, make sure `STATE.json` reflects this session: the
current stage, any stage transition in `stage_history`, and hours in
`time_log`. If hours for this session are not logged, ask the learner how long
they worked and log it.

Then run `bash scripts/sync_up.sh $ARGUMENTS` from the repo root and show its
output.

- If a check fails, nothing is committed. Show the failure exactly and stop. Do
  not weaken a test, edit `STATE.json` to force validity, or bypass the check.
- If the commit succeeds but the push fails (offline), say so plainly: the work
  is committed locally and `sync-up` must be re-run when connected.
