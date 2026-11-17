# The Module Execution Loop

One pre-flight stage plus five stages. `STATE.json` is updated at every
transition: set `current_stage`, append to the module's `stage_history`, set
`updated`, and log hours in `time_log`. Then run
`uv run python scripts/validate_state.py`.

## Session start (every session)

1. Run `/sync-down` (`bash scripts/sync_down.sh`): pull, install locked
   packages, verify `STATE.json`, re-hydrate missing local data. It works
   offline; a failed pull is reported and the rest still runs.
2. Read `STATE.json`. Resume at `current_module` / `current_stage`. Do not
   restart a stage that is already in `stage_history` unless the learner asks.
3. Report in two lines: where we are, and hours spent vs. the module's time-box.
4. If `hours_spent` is at or above 80% of `timebox_hours`, name which
   Nice-to-haves get cut. The time-box does not stretch.

## Session end (every session)

1. Log the session's hours in `time_log` and update the module's `hours_spent`.
2. Run `/sync-up` (`bash scripts/sync_up.sh`): harness, `STATE.json` check,
   portability check, commit, push. A failed check means nothing is committed;
   fix the cause, never the check. Offline, the commit stays local and
   `/sync-up` is re-run when connected.

## Time-box split (guide, per module)

| Stage | Share of time-box |
|---|---|
| `preflight` | 10% |
| `incubation` | 10% |
| `ingestion` | 20% |
| `lab` | 40% |
| `heuristics` | 10% |
| `gate` | 10% |

On overrun: cut Nice-to-haves first and record them in the module's
`nice_to_haves_cut`. If the core still does not fit, stop and ask the learner
which lab control to drop. Never drop a gate stage.

---

## Stage 0: `preflight` (not one of the five)

**Who:** main session.

1. **JIT expansion.** Expand Module N's section in `spec/CURRICULUM.md`: lab
   design, sources, cert mapping. The I/O contract (required input, required
   output, gate pass criteria) is frozen. Changing it needs the learner's
   approval and an entry in `STATE.json` `contract_changes`.
2. **Verify every source** before listing it: load the page, confirm title,
   publisher, date, and that it has not been superseded. Anything not confirmed
   is written as `UNVERIFIED` with the reason. Same for repos, tools, technique
   IDs, and model IDs.
3. **Convert sources** into `/literature/mNN/`: add each verified source to
   `literature/sources.json` and run
   `uv run python literature/build.py --module N` (front matter per
   `spec/SCHEMAS.md` §7). Sources already pre-cached are re-checked for
   currency, not re-fetched. Sites that refuse automated clients are saved from
   a browser into `literature/_inbox/`. Paywalled sources are listed but not
   converted; note the gap.
4. **Check the input.** Confirm the prior module's output artifact exists at the
   path recorded in its `outputs`. If it does not, stop.
5. **Module-specific gates.** Module 3: GCP sandbox gate (see curriculum).
   Ask before any large install.
6. Set `expanded: true`, `expanded_on`, status `in_progress`.

**Exit:** sources verified and converted, input present, tools available.

## Stage 1: `incubation`

**Who:** main session, with the learner. No teaching yet.

0. If the contrastive pair does not exist yet, build it first: invoke
   `first-line-engineer` with the module's lab path and its 3.1 build brief
   from `spec/CURRICULUM.md`. The pair is cut from the same system and data the
   lab uses, so lab step 3.1 is effectively done here and is not repeated in
   stage 3. This build needs no learner input.
1. Present the module's unsolved 2nd-line dilemma.
2. Present the contrastive pair: two near-identical artifacts, one effective.
   Do not say which, and do not name the flaw category.
3. The learner writes a diagnosis and a hypothesis or test procedure. Save it
   verbatim to `labs/mNN-*/incubation/cold_attempt.md`.
4. Do not grade it yet and do not reveal the canonical framework. It gets
   revisited at the end of the lab.

**Exit:** `cold_attempt.md` exists.

## Stage 2: `ingestion`

**Who:** main session, with the learner.

1. From `/literature/mNN/`, extract only concepts **new** to this module.
   Concepts from earlier modules are referenced by ID (`M1-C4`), never re-taught.
2. Teach by question first (law 1). Each concept is tied back to the learner's
   cold attempt: what did it get right, what did it miss.
3. Write `labs/mNN-*/NOTES.md`: one short entry per new concept, each with its
   source file and section.

**Exit:** every concept in the module's contract has a `NOTES.md` entry.

## Stage 3: `lab`

Three roles, in order. Role switching is the point (law 3).

| Step | Role | Who runs it | Output |
|---|---|---|---|
| 3.1 | 1st line | `first-line-engineer` subagent | System + controls + synthetic data in `labs/mNN-*/`, generators in `assurance-harness/generators/`, sealed answer key |
| 3.2 | Red team / CTI | `red-team` subagent | `labs/mNN-*/redteam/TRACE.md`, `TTP_MAP.md` |
| 3.3 | 2nd line | **the learner**, in the main session | ToD + ToE procedures, harness tests, results records, one 5 C's finding |

Rules for 3.1 (portability): lab data is never tracked in Git. Every generator
in `assurance-harness/generators/` follows the contract at the top of
`scripts/rehydrate.py`: a fixed internal seed, a `--rehydrate` mode that is
idempotent, and a self-check against checksums it commits to
`assurance-harness/generators/checksums/`. That is what lets a fresh clone
rebuild exactly the dataset the sealed answer key describes. Small evidence
packages the learner inspects by hand go in `labs/mNN-*/evidence/` and are
tracked; bulk data goes in `assurance-harness/data/` or `labs/mNN-*/data/` and
is not.

Rules for 3.3:

- The learner writes each procedure in prose **before** any code
  (`labs/mNN-*/procedures/<control>-tod.md`, `-toe.md`). The main session may
  then help turn it into code, but does not write the procedure.
- Every ToE becomes an executable test in `assurance-harness/mNN/` (pytest, SQL
  via DuckDB, or Rego/OPA from Module 3) and runs against 10,000+ rows on both
  the `planted` and `clean` datasets. Results follow `spec/SCHEMAS.md` §2.
- The main session never reads `.sealed/ANSWER_KEY.md` aloud or hints from it.
- Independence: the finding says what must be true. It does not design the fix.
- Close the lab by returning to `cold_attempt.md`: the learner writes what they
  would now change (`incubation/retrospective.md`).

**Exit:** harness runs, results records exist for both datasets, one 5 C's
finding is written, and the module's output artifact exists.

## Stage 4: `heuristics`

**Who:** main session, with the learner.

1. Add "If X → then verify Y" entries to `HEURISTICS.md` (format: SCHEMAS §5).
2. Emit 15 to 30 flashcards to `flashcards/mNN.csv` (format: SCHEMAS §6).
3. Write the sanitized portfolio piece to `portfolio/mNN-<slug>.md`: synthetic
   data only, nothing from any employer, no sealed answer-key content.
4. Update `flashcards_count` and `heuristics_added` in `STATE.json`.

**Exit:** all three artifacts exist.

## Stage 5: `gate`

Module N+1 stays `locked` until all four pass. Record each result in the
module's `gate` object and increment `attempts` per full attempt.

| # | Check | Who | Pass when |
|---|---|---|---|
| 1 | First-principles edge case ("what breaks if X changes?") | `socratic-tutor` skill, **inline in the main session** | The learner derives the consequence from mechanism, not recall |
| 2 | 1st-line pushback | Main session roleplays a skeptical Staff Engineer (false positive? too costly?) | The learner defends with re-performance evidence and risk mechanics, and does not design the fix |
| 3 | Four-tier compression | Learner writes; main session reviews | Same finding as (a) raw query or exploit trace, (b) 10-minute engineer walkthrough, (c) privilege-aware legal brief, (d) 2-sentence executive risk pitch, saved to `labs/mNN-*/gate/` |
| 4 | Artifact check | `assurance-grader` subagent, isolated | Verdict `PASS` |

The tutor skill is never run as a subagent: the gate is a live back-and-forth
and subagents run to completion without one. There is no `socratic-tutor` file
in `.claude/agents/` and one must never be created.

### Grader handoff (check 4): paths only

The handoff prompt is exactly this and nothing else:

```
Module: NN
Paths:
- labs/mNN-<slug>/
- assurance-harness/
- spec/CURRICULUM.md
```

No summary of the session, no explanation of shortcuts or struggles, no hint
about the expected verdict. The subagent never sees conversation history, so
this prompt is the only channel for bias. If the grader reports
`ISOLATION BREACH`, the check is void: fix the handoff and re-run.

A `FAIL` is shown to the learner in full. The main session does not argue with
it or re-run the grader with added context.

### On pass

Set the module `status: complete`, `current_stage: complete`, record `outputs`
paths. Then unlock module N+1 (`status: unlocked`, `current_module: N+1`,
`current_stage: preflight`).

## Parking

Anything outside the scope fence, or any Maybe-later item whose trigger has not
fired, is named, appended to `STATE.json` `parked`, and not built.
