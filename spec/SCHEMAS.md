# Schemas

Single source of truth for every state and record format in this repo.
`scripts/validate_state.py` extracts the JSON Schema below (the fenced block
that follows the `schema:state` marker) and validates `STATE.json` against it.
Change the schema here, never in the script.

## 1. `STATE.json`

Updated at **every** stage transition (see `spec/MODULE_LOOP.md`). Dates are
ISO `YYYY-MM-DD`. `current_stage` is a named enum, never a list number.

| Stage value | Meaning |
|---|---|
| `preflight` | Stage 0. JIT expansion, source verification and conversion, module-specific gates |
| `incubation` | Stage 1. Dilemma + contrastive cold start |
| `ingestion` | Stage 2. Extract new concepts from `/literature` |
| `lab` | Stage 3. Purple-team lab + assurance-as-code |
| `heuristics` | Stage 4. Heuristics, flashcards, portfolio write-up |
| `gate` | Stage 5. Socratic mastery gate |
| `complete` | Gate passed; next module unlocks |

<!-- schema:state -->
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "STATE.json",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version", "created", "updated", "weekly_hours_budget",
    "current_module", "current_stage", "bootstrap", "model_routing",
    "modules", "time_log", "parked", "contract_changes"
  ],
  "properties": {
    "schema_version": { "const": 1 },
    "created": { "$ref": "#/$defs/date" },
    "updated": { "$ref": "#/$defs/date" },
    "weekly_hours_budget": { "type": "number", "exclusiveMinimum": 0 },
    "current_module": { "type": "integer", "minimum": 1, "maximum": 12 },
    "current_stage": { "$ref": "#/$defs/stage" },
    "bootstrap": {
      "type": "object",
      "additionalProperties": false,
      "required": ["pass1_complete", "pass1_completed_on"],
      "properties": {
        "pass1_complete": { "type": "boolean" },
        "pass1_completed_on": { "$ref": "#/$defs/date_or_null" }
      }
    },
    "model_routing": {
      "type": "object",
      "additionalProperties": false,
      "required": ["main_session_model", "subagent_env_override_unset", "subagents"],
      "properties": {
        "main_session_model": { "type": "string", "minLength": 1 },
        "subagent_env_override_unset": { "type": "boolean" },
        "subagents": {
          "type": "object",
          "additionalProperties": false,
          "required": ["first-line-engineer", "red-team", "assurance-grader"],
          "properties": {
            "first-line-engineer": { "$ref": "#/$defs/subagent_route" },
            "red-team": { "$ref": "#/$defs/subagent_route" },
            "assurance-grader": { "$ref": "#/$defs/subagent_route" }
          }
        }
      }
    },
    "modules": {
      "type": "array",
      "minItems": 12,
      "maxItems": 12,
      "items": { "$ref": "#/$defs/module" }
    },
    "time_log": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["date", "module", "stage", "hours"],
        "properties": {
          "date": { "$ref": "#/$defs/date" },
          "module": { "type": "integer", "minimum": 1, "maximum": 12 },
          "stage": { "$ref": "#/$defs/stage" },
          "hours": { "type": "number", "exclusiveMinimum": 0 },
          "note": { "type": "string" }
        }
      }
    },
    "parked": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["item", "reason", "trigger", "parked_on"],
        "properties": {
          "item": { "type": "string", "minLength": 1 },
          "reason": { "enum": ["out_of_scope", "maybe_later", "nice_to_have"] },
          "trigger": { "type": ["string", "null"] },
          "parked_on": { "$ref": "#/$defs/date" }
        }
      }
    },
    "contract_changes": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["module", "date", "change", "approved_by_learner"],
        "properties": {
          "module": { "type": "integer", "minimum": 1, "maximum": 12 },
          "date": { "$ref": "#/$defs/date" },
          "change": { "type": "string", "minLength": 1 },
          "approved_by_learner": { "const": true }
        }
      }
    }
  },
  "$defs": {
    "date": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" },
    "date_or_null": {
      "anyOf": [ { "$ref": "#/$defs/date" }, { "type": "null" } ]
    },
    "stage": {
      "enum": ["preflight", "incubation", "ingestion", "lab", "heuristics", "gate", "complete"]
    },
    "gate_result": { "enum": ["pending", "pass", "fail"] },
    "subagent_route": {
      "type": "object",
      "additionalProperties": false,
      "required": ["model", "verified", "verified_on", "served_by"],
      "properties": {
        "model": { "type": "string", "pattern": "^claude-[a-z0-9-]+$" },
        "verified": { "type": "boolean" },
        "verified_on": { "$ref": "#/$defs/date_or_null" },
        "served_by": { "type": ["string", "null"] }
      }
    },
    "module": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "id", "slug", "title", "status", "expanded", "expanded_on",
        "timebox_hours", "hours_spent", "stage_history", "gate", "outputs",
        "nice_to_haves_cut", "telemetry_source", "flashcards_count", "heuristics_added"
      ],
      "properties": {
        "id": { "type": "integer", "minimum": 1, "maximum": 12 },
        "slug": { "type": "string", "pattern": "^m\\d{2}-[a-z0-9-]+$" },
        "title": { "type": "string", "minLength": 1 },
        "status": { "enum": ["locked", "unlocked", "in_progress", "complete"] },
        "expanded": { "type": "boolean" },
        "expanded_on": { "$ref": "#/$defs/date_or_null" },
        "timebox_hours": { "type": "number", "exclusiveMinimum": 0 },
        "hours_spent": { "type": "number", "minimum": 0 },
        "stage_history": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["stage", "entered_on"],
            "properties": {
              "stage": { "$ref": "#/$defs/stage" },
              "entered_on": { "$ref": "#/$defs/date" }
            }
          }
        },
        "gate": {
          "type": "object",
          "additionalProperties": false,
          "required": ["edge_case", "pushback", "compression", "artifact_check", "attempts"],
          "properties": {
            "edge_case": { "$ref": "#/$defs/gate_result" },
            "pushback": { "$ref": "#/$defs/gate_result" },
            "compression": { "$ref": "#/$defs/gate_result" },
            "artifact_check": { "$ref": "#/$defs/gate_result" },
            "attempts": { "type": "integer", "minimum": 0 }
          }
        },
        "outputs": { "type": "array", "items": { "type": "string" } },
        "nice_to_haves_cut": { "type": "array", "items": { "type": "string" } },
        "telemetry_source": { "enum": [null, "live_gcp", "synthetic_labeled"] },
        "flashcards_count": { "type": "integer", "minimum": 0 },
        "heuristics_added": { "type": "integer", "minimum": 0 }
      }
    }
  }
}
```

### Invariants the schema cannot express (checked by `validate_state.py`)

1. `modules[i].id == i + 1`, in order.
2. Exactly one module is `in_progress` or `unlocked` at a time, and it is `current_module`. Every earlier module is `complete`; every later module is `locked`.
3. A module is `complete` only if all four `gate` fields are `pass`.
4. `hours_spent` for a module equals the sum of its `time_log` entries.
5. `telemetry_source` is non-null only on module 3, and module 3 cannot be `complete` while it is null.
6. A module with `expanded: false` cannot be past `preflight`.

## 2. Harness result record

Every Test of Operating Effectiveness writes one JSON record to
`assurance-harness/results/mNN/<control_id>.json`.

**Convention:** pytest going green means the *procedure* is sound (population
reconciled, sample reproducible, query deterministic). It does **not** mean the
control passed. The control's result lives in the record's `conclusion` field.
A ToE that finds exceptions is a successful test, not a failing one.

```json
{
  "control_id": "LD-AC-03",
  "module": 1,
  "procedure_ref": "labs/m01-risk-controls-independence/procedures/LD-AC-03-toe.md",
  "period_start": "2026-07-01",
  "period_end": "2026-09-30",
  "population_source": "iam_accounts (system of record)",
  "population_size": 12000,
  "population_reconciled": true,
  "method": "full_population | sample",
  "sample_size": null,
  "sample_seed": null,
  "evidence_type": "reperformance | inspection | observation | inquiry",
  "exceptions": 0,
  "exception_ids": [],
  "exception_rate": 0.0,
  "conclusion": "effective | ineffective | not_determinable",
  "dataset": "planted | clean",
  "run_at": "2026-11-17T00:00:00Z"
}
```

Each ToE runs against two datasets: `planted` (with injected drift, missing
inventory, and exceptions) and `clean`. Detecting the planted exceptions is the
test's sensitivity; staying silent on `clean` is its specificity. The grader
scores both against the sealed answer key.

## 3. 5 C's finding

One Markdown file per finding at `labs/mNN-*/findings/F-NN-<n>.md`, with front matter:

```yaml
---
id: F-01-1
module: 1
control_id: LD-AC-03
title: <one line>
severity: null            # rated from Module 4 onward; null before
evidence: [assurance-harness/results/m01/LD-AC-03.json]
status: open              # open | remediated | revalidated | risk_accepted
---
```

Body headings, in order: `## Criteria`, `## Condition`, `## Cause`,
`## Consequence`, `## Corrective action`. Corrective action states what must be
true, never how the 1st line should build it.

## 4. Sealed answer key

`labs/mNN-*/.sealed/ANSWER_KEY.md`, written only by `first-line-engineer`. One
entry per planted flaw: `id`, `type` (incomplete_population | survivorship |
drift | missing_inventory | planted_exception | bypass), `where`, `expected
exception ids or count`, `which control it defeats`. The main session does not
show it to the learner before the gate's artifact check. `red-team` does not
read it. `assurance-grader` may read it but reports only detected / not detected.

## 5. `HEURISTICS.md` entry

```
### H-NN-<n>  (Module NN)
If <architectural pattern X> → then verify <control or failure mode Y>.
Evidence: <harness test or finding id that taught this>
```

## 6. Flashcards

`flashcards/mNN.csv`, Anki-importable, UTF-8, 15 to 30 cards per module:

```
#separator:Comma
#html:false
#columns:Front,Back,Tags
#tags column:3
"<question>","<answer>","m01 CISA::D1 AAIA::D3 AIGP::I"
```

Tags: module (`mNN`) plus at least one of `CISA::D1`..`D5`, `AAIA::D1`..`D3`,
`AIGP::I`..`IV`. Optional: `CISSP::D1`..`D8`, `CISM::D1`..`D4`, `42001LA::D1`..`D7`.
Domain names are in `spec/CURRICULUM.md` under "Cert domain reference".

## 7. Literature front matter

Every file in `/literature` starts with:

```yaml
---
title: <exact official title>
publisher: <publisher>
source_url: <URL the file was retrieved from>
retrieved: YYYY-MM-DD
sha256: <hash of the source file>
converter: pymupdf4llm <version> | markdownify <version>
source_format: pdf | html | text
pages: "<1-based ranges>"      # only when part of a PDF was converted
licence: <as stated by the publisher, or "unstated">
module: NN
verified: true
---
```

Written by `literature/convert.py`; never by hand. `literature/SOURCES.md` is
regenerated from these blocks. `literature/sources.json` is the declared list
of what to fetch: one entry per verified source, with `module`, `slug`,
`format`, `title`, `publisher`, `url`, `licence`, optional `pages`, and
optional `manual` (the reason an automated fetch is not possible).
