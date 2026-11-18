# Mission Control

A local dashboard over this repository: a map of the 12 modules, a room for the
active stage, editors for the files you author, and a button that runs the
harness. It is tooling, not a module. It does not replace Claude Code: the
Socratic gate, the Staff Engineer pushback and the subagents stay in the
terminal, and the app hands you the prompt to paste.

## Run it

From the repo root:

```
uv run python scripts/start_ui.py
```

(`make studio` does the same where `make` exists.) The launcher builds the
frontend into `web/dist` when it is missing or stale, starts the backend on
`127.0.0.1:8765`, and opens the browser. `--no-browser`, `--port N` and
`--no-build` are available.

**Requirements:** uv, and Node 22.12 or newer on both Windows and macOS
(`web/.nvmrc` pins 24). The first build runs `npm ci`, which needs the network
once. After that the app loads nothing from the network: fonts, icons and
scripts are bundled. On Windows the two sync buttons run the repo's scripts
through Git Bash.

## What it reads and writes

The repo is the only source of truth. There is no database and no browser
storage; the current view is kept in the URL hash, and unsaved editor text
lives in memory until you save it.

| | |
|---|---|
| Reads | `STATE.json`, `HEURISTICS.md`, `spec/CURRICULUM.md`, `spec/MODULE_LOOP.md`, `literature/mNN/*.md`, `flashcards/*.csv`, `portfolio/*.md`, `assurance-harness/results/mNN/*.json`, and inside `labs/mNN-*/`: `README.md`, `SYSTEM.md`, `NOTES.md`, `evidence/`, `incubation/`, `procedures/`, `findings/`, `gate/`, `redteam/`, `register/` |
| Writes | Only files you author: `incubation/cold_attempt.md`, `incubation/retrospective.md`, `procedures/<control>-tod.md` and `-toe.md`, `findings/F-NN-<n>.md`, the four briefs in `gate/`, and entries appended to `HEURISTICS.md` |
| Never touches | `labs/mNN-*/.sealed/`, anything named `sealed_*`, all of `assurance-harness/generators/` and `assurance-harness/data/`, `labs/*/data/`, hidden paths (`.git/`, `.env`), secrets, and `STATE.json` (read only) |

The policy is one file: `server/paths.py`. Writes are atomic and are refused
when the file on disk is not the version the editor loaded.

Progress is derived on every request (`server/derive.py`) from stage history,
flashcard tags, `HEURISTICS.md` and logged hours. Nothing is stored as a score.

While a module is in progress, parts of its curriculum section are held back
until the stage that needs them (`WITHHOLD_RULES` in `server/curriculum.py`).
Held-back text is not sent to the browser. Set `WITHHOLD = False` there to show
everything.

## Safety

Bound to `127.0.0.1`. Requests with a foreign `Host` or `Origin`, and
cross-site requests, are refused. Every write and every subprocess needs a
token generated at launch and kept in memory. Subprocess command lines are
fixed in `server/runner.py`; a request can only name one of them. Rendered
Markdown is sanitized with raw HTML disabled, and images are never fetched.

## Tests

```
uv run python -m pytest web/tests -v
```

They prove that sealed paths, traversal, stale writes and tokenless requests
are refused, against a throwaway repo (`tests/fixture_repo.py`).

## Working on the UI

```
uv run python scripts/start_ui.py --dev --no-browser     # backend on :8765
cd web && npm run dev                                    # Vite on :5173, proxies /api
```

`web/design/` holds the Phase A prototype (mock data, three directions). The
app implements direction A, "Schematic".
