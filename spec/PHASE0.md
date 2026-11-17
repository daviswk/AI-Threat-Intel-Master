# Phase 0: Environment Audit & Tool Binding

Desktop audit date: **2026-11-17**. Host: Windows 11 Home, Git Bash + PowerShell,
Claude Code 2.1.321 (desktop app, Code tab). Sections 1–8 describe the desktop
the project was created on. Any other machine gets its own section at the end
of this file, written by `scripts/phase0_audit.py`.

## 1. Environment audit (desktop)

### Hardware and runtime

| Item | Found |
|---|---|
| GPU | NVIDIA GeForce RTX 2070 SUPER, 8 GB VRAM |
| Free disk (repo volume) | 1.5 TB |
| Python | 3.11 (uv-managed), project venv at `.venv` |
| Node | v24.18.0, npm, pnpm 11.10.0 |
| Docker | 29.6.1 |
| git | 2.55.0 |
| uv | 0.11.28 |
| `make`, `gh` | not installed |

### Skills

| Location | Contents |
|---|---|
| Project (`.claude/skills/`) | **`socratic-tutor`** (vendored 2026-11-17, see §3) |
| User-level skills folder | `learnharness`, plus desktop-app skills (docs, docx, pdf, pptx, xlsx, learn, deep-research, skill-creator, and others). None are required by this curriculum |
| Plugins (CLI) | `superpowers@claude-plugins-official` 7.0.2. Not required |
| Plugins (desktop app) | `data`, `productivity`, `pdf-viewer`, `mattpocock-skills`, `cowork-plugin-management`, and single-skill plugins. Not required |

There is no user-level `CLAUDE.md`, commands folder, or agents folder, so
nothing else needed vendoring.

### MCP servers

| Server | State |
|---|---|
| Claude Docs, Consensus, Figma, Monarch, Microsoft Learn (claude.ai connectors) | Connected |
| `pdf-viewer` (plugin) | Connected |
| `research-desk` reference lookup (plugin) | Connected |
| Slack, Notion, Linear, Atlassian, Monday, ClickUp, Hex, Amplitude (plugins) | Need authentication; not needed by this curriculum |
| `definite` (plugin) | Failed to connect (endpoint not found) |

None of the curriculum depends on an MCP server today. Module 9 will build its own.

### Python packages

Locked in `uv.lock` (and mirrored in `requirements.lock` for pip): `pytest`,
`duckdb`, `jsonschema`, `pymupdf4llm` (with `pymupdf`), `beautifulsoup4`,
`markdownify`, and their dependencies. 32 packages in total. Nothing large.

## 2. Literature pipeline (PDF and HTML → Markdown)

**Choice: `pymupdf4llm`** for PDFs, `beautifulsoup4` + `markdownify` for HTML
pages. `literature/build.py` fetches and converts every entry in
`literature/sources.json`; `literature/convert.py` converts a single file.

- **`bentopdf` was checked and rejected.** Its tools reference does list a
  "PDF to Markdown" tool, so the capability exists, but BentoPDF is a
  browser-only web app (self-hosting covers Docker and static builds; there is
  no CLI and no npm package named `bentopdf`). It cannot run inside an
  automated pipeline. Sources: [tools reference](https://bentopdf.com/docs/tools/),
  [self-hosting](https://bentopdf.com/docs/self-hosting/).
- Preference order was `docling`, `marker`, `pymupdf4llm`. The learner chose
  `pymupdf4llm` on 2026-11-17: no model download, adequate for text-based
  standards. `docling` and `marker` both need multi-GB model downloads.
- **Revisit trigger:** if a module's sources convert badly (complex tables,
  scanned pages), ask before installing `docling`.
- `pymupdf4llm` reports that RapidOCR is not installed; that only matters for
  scanned PDFs.
- Downloads use plain `curl` under its own identity. Sites that refuse
  automated clients (pcaobus.org, iso.org, IEEE Xplore) are marked `manual` in
  `sources.json`: save the page as PDF from a browser into
  `literature/_inbox/<slug>.pdf` and re-run `build.py`. The pipeline never
  poses as a browser.
- nvlpubs.nist.gov answers HEAD with 404 for some PDFs but serves GET, so link
  checkers raise false alarms.

## 3. Tutor

**`socratic-tutor` is vendored into this repository** at
`.claude/skills/socratic-tutor/SKILL.md` and is invoked as `socratic-tutor`.

- Before 2026-11-17 it existed only as a desktop-app plugin skill, outside both
  the project and the user-level skills folder, so a terminal session on
  another machine would not have had it. The vendored copy is byte-identical
  to that plugin's single `SKILL.md`. It was copied, not rewritten.
- On the desktop app the plugin copy also appears, namespaced as
  `socratic-tutor:socratic-tutor`. Either works; the vendored one is the
  portable one.
- The skill ships with no licence file. Treat the vendored copy as private-use
  material, which is one more reason this repository stays private.
- It runs inline in the main session. No `.claude/agents/socratic-tutor.md`
  exists, and both `scripts/verify_routing.py` and
  `scripts/bootstrap_laptop.sh` fail if one is ever created.

## 4. Model routing

**Main session:** `claude-fable-5-2` (the model the Pass 1 session was launched on).

| Subagent | `model:` (frontmatter) | Served by (observed) | Verified |
|---|---|---|---|
| `first-line-engineer` | `claude-opus-5-5` | `claude-opus-5-5` | 2026-11-17 PASS |
| `red-team` | `claude-mythos-5-2` | `claude-mythos-5-2` | 2026-11-17 PASS |
| `assurance-grader` | `claude-fable-5-2` | `claude-fable-5-2` | 2026-11-17 PASS |

- `CLAUDE_CODE_SUBAGENT_MODEL`: **unset** (confirmed). Leave it unset.
- `ANTHROPIC_API_KEY`: not set; the CLI is on a claude.ai login.

### How it was verified

`/tasks` is not reachable from inside a session, and agents created
mid-session are not loaded until the next session. So verification runs a
separate headless session: `scripts/verify_routing.py` launches `claude -p` on
a **third** model (`claude-sonnet-5-5`), has it invoke each subagent on a
trivial `ls` task, and reads the `model` field on each subagent's own messages
in the event stream. Using a main model that differs from every subagent model
means inheritance or fallback cannot be mistaken for correct routing.

```
uv run python scripts/verify_routing.py
```

### Change log

| Date | Change | Result |
|---|---|---|
| 2026-11-17 | Initial routing: `red-team` on `claude-opus-5-5` | Verified (all three PASS) |
| 2026-11-17 | Learner reported Mythos approval. `red-team` switched to `claude-mythos-5-2`. The ID string was read from Anthropic's model page ([Claude Mythos 5.2 overview](https://platform.claude.com/docs/en/models/mythos-5-2/overview), "Model IDs" table, Claude API row), not guessed | Re-verified: served by `claude-mythos-5-2` |

**Open item for the learner:** compare `claude-mythos-5-2` with the ID in your
approval notice from Anthropic. If they differ, change the frontmatter and
re-run the check.

**If Mythos access lapses**, the check will show `red-team` served by another
model. Do not leave it that way: confirm the fallback (`claude-opus-5-5`) with
the learner, update the frontmatter, re-verify, and log it here.

Routing is a property of the account and the machine. It is re-verified on
every new machine by `scripts/bootstrap_laptop.sh`.

## 5. Lab tooling

| Tool | Desktop status | First needed | Decision |
|---|---|---|---|
| `pytest` | Installed (locked) | Module 1 | Done |
| `duckdb` | Installed (locked, Python package) | Module 1 | Done |
| `opa` | Missing | Module 3 | Deferred; small single binary |
| `gcloud` | Missing | Module 3 pre-flight | Deferred; **ask first** (large SDK) |
| Terraform / OpenTofu | Missing | Module 3 | Deferred |
| Ollama + model weights | Missing | Module 6 | Deferred; **ask first** (multi-GB) |
| LoRA stack (`peft`, `transformers`, `torch`) | Not in the lock | Module 6 | Deferred; **ask first**; added as an optional dependency group |
| `garak` | Missing | Module 7 | Deferred; **ask first** |
| `PyRIT` | Missing | Module 7 | Deferred; **ask first** (heavy dependency stack) |
| `promptfoo` | Missing | Module 7 | Deferred |
| Docker | Installed | Module 3+ | Available |

Nothing beyond the locked base packages is needed before Module 3.

## 6. Time budget

**8 hours per week** (learner, 2026-11-17). Time-boxes are in `STATE.json` and
total 220 h, 27.5 weeks. On overrun, Nice-to-haves are cut first; the time-box
does not stretch.

## 7. Known limitations

1. **The grader's Bash restriction is an instruction, not a technical
   control.** `assurance-grader` has no `Write` or `Edit` tool, but Bash can
   still write files. Its prompt forbids that; nothing enforces it. A
   `PreToolUse` hook could. Left as is for now, and noted because it is exactly
   the design-versus-operation gap Module 1 teaches.
2. **Running the harness writes files** (`assurance-harness/results/`). That is
   the harness writing its own output, not the grader editing what it grades.
   pytest runs with `-p no:cacheprovider` to avoid a cache directory.
3. **New or renamed agents load at session start.** After editing
   `.claude/agents/`, start a new session before invoking them.
4. **GCP is deliberately not provisioned.** It happens at the Module 3
   pre-flight gate.

## 8. Literature status

| Module | Converted | Needs a manual browser save | Notes |
|---|---|---|---|
| 1 | all 10, see `literature/SOURCES.md` | none outstanding (the two PCAOB standards were saved from a browser on 2026-11-17) | Pre-flight closed 2026-11-17 |
| 2 | pre-cached for travel | see `literature/SOURCES.md` | Sources verified early; lab design and cert mapping remain just-in-time |
| 3 | pre-cached for travel | CIS GCP Foundations Benchmark (registration form; optional) | Same |

Pre-caching Modules 2 and 3 is a deliberate exception to just-in-time
expansion, made on 2026-11-17 for offline travel. Only source verification and
conversion were done early. Their I/O contracts are unchanged, and each module's
pre-flight still re-checks that its cached sources are current.

## 9. Travel mode (Modules 6–7 on laptop hardware)

`travel_mode` is decided per machine by `scripts/phase0_audit.py` and recorded
in that machine's section below: **on** when there is no NVIDIA GPU with at
least 8 GB of VRAM, **off** otherwise. The desktop is `off`.

When `travel_mode` is **on**, the Module 6 pre-flight sizes the local model as
follows. These are constraints for the just-in-time expansion to satisfy; the
specific model, runtime, and their IDs are verified then, not named here.

| Constraint | Travel-mode target |
|---|---|
| Base model | **1B to 3B parameters, quantized** (4-bit class), runnable on CPU or Apple Silicon |
| Memory | Fits in laptop RAM with headroom: at most half of physical RAM for model plus context |
| Runtime | One that runs without a discrete GPU on the laptop's OS (CPU, or Apple Silicon acceleration) |
| LoRA fine-tune | Low rank, short sequences, a slice of at most a few hundred Module 5 records, a fixed seed |
| **Time budget** | **The memorization lab (fine-tune) and the extraction lab (attack run) each finish locally in under 5 minutes** |
| Planted canaries | The fine-tune slice includes seeded canary records repeated enough times that memorization is measurable at this model size, so extraction attacks have something real to find |
| Determinism | Fixed seeds and a recorded slice of record IDs, so `scripts/rehydrate.py` can rebuild the adapter and the vector store on any machine |
| Module 7 tooling | Attack tools run against the local model only; prefer the lightest tool that covers the technique, and ask before any heavy install |

Consequences to accept in travel mode:

- A 1B–3B model memorizes less and refuses less than a larger one. Results are
  valid for the lab's purpose (showing that memorization and extraction are
  real and measurable) but failure rates are not comparable with the desktop's.
  Record `travel_mode` next to any Module 8 statistic that depends on them.
- **Model weights are not in Git and cannot be pre-cached by cloning.** The
  one-time download (roughly 1 to 2 GB at this size) needs a good connection.
  Do it when one is available, before reaching Module 6.
- If the under-5-minute target cannot be met on the laptop, shrink the slice
  and the adapter rank first, then the model. Do not move the lab to a hosted
  model: the labs must stay local.

At 8 hours per week, Module 6 starts around week 11, so it is unlikely to be
reached during a one-month trip. Modules 1 and 2 need no network once cloned.
Module 3 needs a connection for the live GCP sandbox; its contract allows
labeled synthetic logs instead (`telemetry_source: synthetic_labeled`).

## 10. Portability

The project is a Git repository designed to clone onto any machine.

| Concern | How it is handled |
|---|---|
| Skills and agents | Vendored in `.claude/` and tracked |
| Paths | Repo-relative only; `scripts/check_portable.py` fails on any machine-specific path in `CLAUDE.md`, `spec/`, `.claude/`, or `scripts/`, and runs inside `sync-up` |
| Python | `pyproject.toml` + `uv.lock` (universal: Windows, macOS, Linux), mirrored to `requirements.lock`; `.python-version` pins 3.11 |
| Commands | `uv run python ...`, never an OS-specific venv path |
| Local data | Not tracked. Rebuilt deterministically by `scripts/rehydrate.py` from seeded generators, and checked against committed checksums |
| Literature | Converted Markdown is tracked; raw downloads are not |
| Secrets | `.gitignore` excludes keys, credentials, `.env`, and Terraform state before Module 3 ever creates them |
| Session handoff | `/sync-down` at the start, `/sync-up` at the end (`scripts/sync_down.sh`, `scripts/sync_up.sh`; `make` targets where `make` exists) |
| New machine | `bash scripts/bootstrap_laptop.sh`, which also writes that machine's audit below |

**Not portable, by nature:** the Claude Code login, the claude.ai connectors,
and any desktop-app plugins. None are required.

<!-- env:desktop-environment-bootstrap-self-test:start -->
## Desktop Environment (bootstrap self-test)

Audited 2026-11-17 by `scripts/phase0_audit.py`. Re-running replaces this section.

| Item | Found |
|---|---|
| OS | Windows 10 (AMD64) |
| Python (venv) | 3.11.15 |
| RAM | 64 GB |
| GPU | NVIDIA GeForce RTX 2070 SUPER, 8 GB VRAM |
| Free disk (repo volume) | 1498 GB |
| Claude Code | 2.1.321 (Claude Code) |
| `CLAUDE_CODE_SUBAGENT_MODEL` | unset |
| Vendored `socratic-tutor` skill | present |
| `socratic-tutor` agent file | absent (correct) |

| Tool | Status |
|---|---|
| `git` | git version 2.55.0.windows.2 |
| `uv` | uv 0.11.28 (ebf0f43d7 2026-07-07 x86_64-pc-windows-msvc) |
| `node` | v24.18.0 |
| `docker` | Docker version 29.6.1, build 8900f1d |
| `make` | missing |
| `gh` | missing |
| `opa` | missing |
| `gcloud` | missing |
| `tofu` | missing |
| `terraform` | missing |
| `ollama` | missing |
| `garak` | missing |
| `promptfoo` | missing |

**Model routing on this machine: VERIFIED**

```
subagent              frontmatter model       served by                   result
assurance-grader      claude-fable-5-2        claude-fable-5-2            PASS
first-line-engineer   claude-opus-5-5         claude-opus-5-5             PASS
red-team              claude-mythos-5-2       claude-mythos-5-2           PASS
```

**travel_mode: off** (NVIDIA GPU with 8 GB or more present; desktop sizing applies).
<!-- env:desktop-environment-bootstrap-self-test:end -->
