/* MOCK DATA for the Phase A design prototype only.
   Shaped like spec/SCHEMAS.md (STATE.json §1, result record §2, finding §3,
   heuristics §5, flashcards §6). Module ids, slugs, titles and time-boxes are
   the real ones from STATE.json. Everything else is invented so the three
   states (complete, active, locked) and a failing test can be shown.
   Identifiers that do not exist in the repo are prefixed MOCK-.
   Nothing here is read by the real app. */
(function () {
  const BASE = [
    [1, "m01-risk-controls-independence", "Risk, controls & independence", 16],
    [2, "m02-cti-threat-modeling", "CTI tradecraft & threat modeling", 16],
    [3, "m03-hyperscale-security", "Hyperscale security & Google's model", 20],
    [4, "m04-assurance-as-code", "Assurance-as-code foundations", 16],
    [5, "m05-privacy-engineering", "Privacy engineering & testing", 20],
    [6, "m06-ai-ml-internals", "AI/ML internals & the 5 paradigm shifts", 24],
    [7, "m07-ai-threats-red-teaming", "AI threat taxonomy & red teaming", 24],
    [8, "m08-ai-evals-measurement", "AI evals & measurement science", 16],
    [9, "m09-agentic-mcp-security", "Agentic & MCP security", 16],
    [10, "m10-ai-supply-chain", "AI/ML supply chain integrity", 16],
    [11, "m11-frameworks-regulation-severity", "Frameworks, regulation & severity", 12],
    [12, "m12-program-management-capstone", "Program management, 5 C's & influence", 24],
  ];
  const STAGES = ["preflight", "incubation", "ingestion", "lab", "heuristics", "gate", "complete"];
  const pass = { edge_case: "pass", pushback: "pass", compression: "pass", artifact_check: "pass", attempts: 1 };
  const pending = { edge_case: "pending", pushback: "pending", compression: "pending", artifact_check: "pending", attempts: 0 };
  const hist = (dates) => dates.map((d, i) => ({ stage: STAGES[i], entered_on: d }));

  const overrides = {
    1: { status: "complete", expanded: true, expanded_on: "2026-11-17", hours_spent: 15.5, gate: pass,
         stage_history: hist(["2026-11-17", "2026-11-17", "2026-11-20", "2026-11-24", "2026-12-01", "2026-12-02", "2026-12-03"]),
         outputs: ["labs/m01-risk-controls-independence/register/risk_control_register.csv"],
         flashcards_count: 6, heuristics_added: 2 },
    2: { status: "complete", expanded: true, expanded_on: "2026-12-04", hours_spent: 17, gate: { ...pass, attempts: 2 },
         stage_history: hist(["2026-12-04", "2026-12-06", "2026-12-08", "2026-12-12", "2026-12-18", "2026-12-19", "2026-12-21"]),
         outputs: ["labs/m02-cti-threat-modeling/MOCK-threat-model.md"],
         nice_to_haves_cut: ["MOCK nice-to-have cut on overrun"],
         flashcards_count: 5, heuristics_added: 1 },
    3: { status: "in_progress", expanded: true, expanded_on: "2026-12-22", hours_spent: 9, gate: pending,
         stage_history: hist(["2026-12-22", "2026-12-27", "2026-12-29", "2027-01-03"]),
         telemetry_source: "synthetic_labeled" },
  };

  const modules = BASE.map(([id, slug, title, timebox_hours]) => ({
    id, slug, title, status: "locked", expanded: false, expanded_on: null,
    timebox_hours, hours_spent: 0, stage_history: [], gate: pending, outputs: [],
    nice_to_haves_cut: [], telemetry_source: null, flashcards_count: 0, heuristics_added: 0,
    ...(overrides[id] || {}),
  }));

  const state = {
    schema_version: 1, created: "2026-11-17", updated: "2027-01-05", weekly_hours_budget: 8,
    current_module: 3, current_stage: "lab", modules,
    time_log: [
      { date: "2026-12-03", module: 1, stage: "gate", hours: 15.5 },
      { date: "2026-12-21", module: 2, stage: "gate", hours: 17 },
      { date: "2027-01-05", module: 3, stage: "lab", hours: 9 },
    ],
  };

  /* Flashcards: flashcards/mNN.csv rows (Front, Back, Tags). Card text is taken
     from process facts in spec/, never from a lab's lesson. */
  const flashcards = [
    { file: "flashcards/m01.csv", front: "In this harness, what does pytest going green mean?", back: "The procedure is sound: population reconciled, sample reproducible, query deterministic. It does not mean the control passed.", tags: "m01 CISA::D1 AAIA::D3" },
    { file: "flashcards/m01.csv", front: "Where does a control's result live in a harness result record?", back: "In the record's conclusion field: effective, ineffective, or not_determinable.", tags: "m01 CISA::D1 AAIA::D3" },
    { file: "flashcards/m01.csv", front: "Name the five body headings of a 5 C's finding, in order.", back: "Criteria, Condition, Cause, Consequence, Corrective action.", tags: "m01 CISA::D1 AAIA::D1 AIGP::I" },
    { file: "flashcards/m01.csv", front: "What may a corrective action state?", back: "What must be true. Never how the 1st line should build it.", tags: "m01 CISA::D2 AAIA::D1 AIGP::I" },
    { file: "flashcards/m01.csv", front: "What are a ToE's sensitivity and specificity in this harness?", back: "Sensitivity: detecting the planted exceptions. Specificity: staying silent on the clean dataset.", tags: "m01 CISA::D1 AAIA::D3" },
    { file: "flashcards/m01.csv", front: "Which line writes the ToD and ToE procedures?", back: "The 2nd line: the learner. The main session may turn a written procedure into code but does not write it.", tags: "m01 CISA::D2 AIGP::I" },
    { file: "flashcards/m02.csv", front: "MOCK card front 1", back: "MOCK card back 1", tags: "m02 CISA::D5 AIGP::I" },
    { file: "flashcards/m02.csv", front: "MOCK card front 2", back: "MOCK card back 2", tags: "m02 CISA::D5" },
    { file: "flashcards/m02.csv", front: "MOCK card front 3", back: "MOCK card back 3", tags: "m02 CISA::D5 AAIA::D2" },
    { file: "flashcards/m02.csv", front: "MOCK card front 4", back: "MOCK card back 4", tags: "m02 AIGP::II" },
    { file: "flashcards/m02.csv", front: "MOCK card front 5", back: "MOCK card back 5", tags: "m02 CISA::D4 AIGP::II" },
  ];

  const heuristics = [
    { id: "H-01-1", module: 1, rule: "If MOCK architectural pattern one → then verify MOCK failure mode one.", evidence: "F-01-1" },
    { id: "H-01-2", module: 1, rule: "If MOCK architectural pattern two → then verify MOCK control two.", evidence: "assurance-harness/results/m01/MOCK-CTL-A.json" },
    { id: "H-02-1", module: 2, rule: "If MOCK architectural pattern three → then verify MOCK failure mode three.", evidence: "F-02-1" },
  ];

  const portfolio = [
    { path: "portfolio/m01-risk-controls-independence.md", title: "Module 1 write-up" },
    { path: "portfolio/m02-cti-threat-modeling.md", title: "Module 2 write-up" },
  ];

  /* Active room: Module 3. Briefing text is the real Module 3 contract from
     spec/CURRICULUM.md; stage text is the real Stage 3 section of
     spec/MODULE_LOOP.md, abridged. */
  const briefing = [
    "# Module 3: Hyperscale security & Google's model",
    "`m03-hyperscale-security` · 20 h",
    "- **Core concepts:** IAM, segmentation, encryption/KMS, logging, CI/CD, secrets; BeyondCorp / BeyondProd; \"controls are code, evidence is data\".",
    "- **Input (from M2):** the threat model and test priorities.",
    "- **Output → M4:** a sandbox with controls defined as code and **real audit-log telemetry**, or explicitly labeled synthetic logs if live GCP is deferred.",
    "- **Artifact criteria:** `telemetry_source` is set; controls exist as code for each concept family; at least 10,000 log rows are exported with a schema note; each control traces to an M2 test priority; teardown has been run once and verified.",
  ].join("\n\n");

  const stageText = {
    incubation: [
      "## Stage 1: `incubation`",
      "**Who:** main session, with the learner. No teaching yet.",
      "1. Present the module's unsolved 2nd-line dilemma.\n2. Present the contrastive pair: two near-identical artifacts, one effective. Do not say which, and do not name the flaw category.\n3. The learner writes a diagnosis and a hypothesis or test procedure. Save it verbatim to `labs/mNN-*/incubation/cold_attempt.md`.\n4. Do not grade it yet and do not reveal the canonical framework.",
      "**Exit:** `cold_attempt.md` exists.",
    ].join("\n\n"),
    lab: [
      "## Stage 3: `lab`",
      "Three roles, in order. Role switching is the point (law 3).",
      "1. **3.1 1st line** · `first-line-engineer` subagent · system, controls and synthetic data.\n2. **3.2 Red team / CTI** · `red-team` subagent · `redteam/TRACE.md`, `TTP_MAP.md`.\n3. **3.3 2nd line** · **the learner**, in the main session · ToD + ToE procedures, harness tests, results records, one 5 C's finding.",
      "### Rules for 3.3",
      "- The learner writes each procedure in prose **before** any code (`procedures/<control>-tod.md`, `-toe.md`).\n- Every ToE becomes an executable test in `assurance-harness/mNN/` and runs against 10,000+ rows on both the `planted` and `clean` datasets.\n- Independence: the finding says what must be true. It does not design the fix.\n- Close the lab by returning to `cold_attempt.md`: write what you would now change (`incubation/retrospective.md`).",
      "**Exit:** harness runs, results records exist for both datasets, one 5 C's finding is written, and the module's output artifact exists.",
    ].join("\n\n"),
    gate: [
      "## Stage 5: `gate`",
      "Module N+1 stays `locked` until all four pass.",
      "1. **First-principles edge case** · `socratic-tutor` skill, inline in the main session.\n2. **1st-line pushback** · main session roleplays a skeptical Staff Engineer.\n3. **Four-tier compression** · learner writes; saved to `labs/mNN-*/gate/`.\n4. **Artifact check** · `assurance-grader` subagent, isolated · verdict `PASS`.",
      "A `FAIL` is shown to the learner in full.",
    ].join("\n\n"),
  };

  /* Action banners: one per stage, fixed wording. `where` is "app" or "cli". */
  const banners = {
    incubation: { where: "app", text: "Open both packages in the workbench, then write your diagnosis and test procedure cold.", action: { kind: "open", label: "Open cold attempt", file: "incubation/cold_attempt.md" } },
    lab: { where: "app", text: "Step 3.3 is yours. Write the ToE procedure in prose before any code, then run the harness.", action: { kind: "open", label: "Open procedure", file: "procedures/MOCK-CTL-02-toe.md" }, cli: { label: "Copy CLI prompt: turn procedure into code", prompt: "Module 03, stage lab. I have written a procedure in prose. Follow spec/MODULE_LOOP.md stage 3, rules for 3.3." } },
    gate: { where: "cli", text: "Checks 1, 2 and 4 run in Claude Code. Write the four briefs here, then run each check in the terminal.", cli: { label: "Copy CLI prompt: mastery gate", prompt: "Module 03, stage gate. Run the gate as described in spec/MODULE_LOOP.md stage 5." } },
  };

  const papers = [
    "google-beyondprod.md", "beyondcorp-a-new-approach.md", "google-cloud-audit-logs-overview.md",
    "google-iam-overview.md", "nist-sp-800-207a.md", "nist-sp-800-92.md", "opa-policy-language.md",
  ].map((f) => "literature/m03/" + f);

  /* Contrastive pair: mock artifacts, unrelated to any lab. */
  const pair = {
    label: "MOCK pair · not from any lab",
    files: [
      { name: "sink_config.yaml",
        a: ["sink:", "  name: audit-export", "  destination: bq://assurance.audit_logs", "  filter: logName:\"cloudaudit\"", "  include_children: true", "  retention_days: 400", "  writer_identity: sa-audit-export", "exclusions: []"],
        b: ["sink:", "  name: audit-export", "  destination: bq://assurance.audit_logs", "  filter: logName:\"cloudaudit\" AND severity>=NOTICE", "  include_children: true", "  retention_days: 400", "  writer_identity: sa-audit-export", "exclusions: [health-checks]"] },
      { name: "export_summary.json",
        a: ["{", "  \"period_start\": \"2026-10-01\",", "  \"period_end\": \"2026-12-31\",", "  \"rows_exported\": 18240,", "  \"projects\": 6,", "  \"status\": \"complete\"", "}"],
        b: ["{", "  \"period_start\": \"2026-10-01\",", "  \"period_end\": \"2026-12-31\",", "  \"rows_exported\": 17112,", "  \"projects\": 6,", "  \"status\": \"complete\"", "}"] },
    ],
  };

  /* Files the learner authors, with the paths the module loop names. */
  const myFiles = [
    { group: "Incubation", path: "incubation/cold_attempt.md", kind: "text", body: "MOCK text of a cold attempt written during incubation.", saved: true },
    { group: "Incubation", path: "incubation/retrospective.md", kind: "text", body: "", saved: true },
    { group: "Procedures", path: "procedures/MOCK-CTL-01-tod.md", kind: "text", body: "MOCK test of design, written in prose.", saved: true },
    { group: "Procedures", path: "procedures/MOCK-CTL-02-toe.md", kind: "text", body: "", saved: true },
    { group: "Finding", path: "findings/F-03-1.md", kind: "finding", saved: true,
      front: { id: "F-03-1", module: 3, control_id: "MOCK-CTL-02", title: "", severity: null, evidence: ["assurance-harness/results/m03/MOCK-CTL-02.json"], status: "open" },
      sections: { Criteria: "", Condition: "", Cause: "", Consequence: "", "Corrective action": "" } },
    { group: "Gate briefs", path: "gate/a-raw-trace.md", kind: "text", body: "", saved: true },
    { group: "Gate briefs", path: "gate/b-engineer-walkthrough.md", kind: "text", body: "", saved: true },
    { group: "Gate briefs", path: "gate/c-legal-brief.md", kind: "text", body: "", saved: true },
    { group: "Gate briefs", path: "gate/d-executive-pitch.md", kind: "text", body: "", saved: true },
  ];

  /* Harness run: streamed lines and per-test outcomes. One test fails so the
     failing state is visible. */
  const harness = {
    command: "uv run --frozen python -m pytest assurance-harness/m03",
    tests: [
      { id: "test_mock_ctl_01.py::test_population_reconciles[planted]", outcome: "pass" },
      { id: "test_mock_ctl_01.py::test_population_reconciles[clean]", outcome: "pass" },
      { id: "test_mock_ctl_02.py::test_full_population[planted]", outcome: "fail" },
      { id: "test_mock_ctl_02.py::test_full_population[clean]", outcome: "pass" },
    ],
    lines: [
      ["$ uv run --frozen python -m pytest assurance-harness/m03", null],
      ["..", [0, 1]],
      ["F", [2]],
      [".", [3]],
      ["", null],
      ["=================================== FAILURES ===================================", null],
      ["_______________________ test_full_population[planted] ________________________", null],
      ["assurance-harness/m03/test_mock_ctl_02.py:41: in test_full_population", null],
      ["    assert record[\"population_reconciled\"] is True", null],
      ["E   AssertionError: MOCK failure: population not reconciled before testing", null],
      ["=========================== short test summary info ============================", null],
      ["FAILED assurance-harness/m03/test_mock_ctl_02.py::test_full_population[planted]", null],
      ["1 failed, 3 passed in 2.41s", null],
    ],
    /* Result records (SCHEMAS §2). Shown apart from the test flags: a ToE that
       finds exceptions is a successful test. */
    records: [
      { control_id: "MOCK-CTL-01", dataset: "planted", population_size: 12000, exceptions: 14, conclusion: "ineffective" },
      { control_id: "MOCK-CTL-01", dataset: "clean", population_size: 12000, exceptions: 0, conclusion: "effective" },
    ],
  };

  const sync = {
    upFiles: [" M HEURISTICS.md", " M STATE.json", "?? labs/m03-hyperscale-security/procedures/MOCK-CTL-02-toe.md", "?? assurance-harness/results/m03/MOCK-CTL-01.json"],
    /* The mock harness has a failing test, so sync-up stops at step 1. The
       script's own message is shown unchanged. */
    upLines: ["", "== 1/4 Assurance harness ==", "FAILED assurance-harness/m03/test_mock_ctl_02.py::test_full_population[planted]", "1 failed, 3 passed in 2.41s", "FAIL: harness tests failed; nothing committed"],
    downLines: ["", "== 1/4 Pull ==", "Already up to date.", "", "== 2/4 Python environment (locked) ==", "", "== 3/4 STATE.json integrity ==", "STATE.json valid | module 3 / lab | 220 h planned at 8 h/week = 27.5 weeks", "", "== 4/4 Re-hydrate missing local data ==", "", "== Position ==", "Module 3: Hyperscale security & Google's model | stage: lab | 9 of 20 h used"],
  };

  window.MOCK = { STAGES, state, flashcards, heuristics, portfolio, briefing, stageText, banners, papers, pair, myFiles, harness, sync };
})();
