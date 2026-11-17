---
description: Start-of-session handoff. Pull latest commits, verify STATE.json, re-hydrate missing local data.
allowed-tools: Bash(bash scripts/sync_down.sh:*)
---

Run `bash scripts/sync_down.sh` from the repo root and show its output.

- If every step succeeds, report the position line (module, stage, hours used)
  and stop. Do not start the stage until the learner says so.
- If any step fails or warns, show the message exactly and stop. Do not repair
  `STATE.json`, resolve Git conflicts, or rebuild data by hand without asking.
