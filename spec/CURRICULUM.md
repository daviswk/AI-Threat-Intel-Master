# Curriculum: the 12-Module DAG

Each module's **output** is the next module's **input**. Module 1 is fully
expanded. Modules 2–12 are I/O contracts only and are expanded just-in-time at
their own pre-flight (`spec/MODULE_LOOP.md`, stage 0). A contract cannot change
without the learner's approval.

**Verification status (law 7).** Everything in the Module 1 section and the
cert domain reference was loaded from the publisher's own page on 2026-11-17
unless marked `UNVERIFIED`. Tools, frameworks, and programs named in the
Module 2–12 contracts come from the learner's brief and are **`UNVERIFIED`
until that module's JIT expansion**.

## The running system: Larkspur Desk

One fictional system carries through all twelve modules so that outputs chain.
**Larkspur Desk** is a small customer-support SaaS: customers open tickets,
support agents answer them from a console, admins manage access, and service
accounts run integrations. It is invented for this curriculum, all its data is
synthetic, and it resembles no employer's system.

| Module | What Larkspur Desk gains |
|---|---|
| 1 | Identity and access layer, five access controls, a risk & control register |
| 2 | An adversary profile and threat model |
| 3 | Cloud infrastructure controls and audit-log telemetry |
| 4 | Harness v1 over those controls |
| 5 | A synthetic customer corpus, lineage & retention manifest, deletion log |
| 6 | A RAG support assistant and a LoRA fine-tune on the corpus |
| 7–8 | Guardrails, an attack corpus, and measured failure rates |
| 9 | An agent with tools and an MCP server |
| 10 | Supply-chain controls over the app and the fine-tuned model |
| 11–12 | Every finding mapped, rated, and briefed; the capstone |

## Time-boxes (8 h/week)

| Module | Hours | Weeks | | Module | Hours | Weeks |
|---|---|---|---|---|---|---|
| 1 | 16 | 2.0 | | 7 | 24 | 3.0 |
| 2 | 16 | 2.0 | | 8 | 16 | 2.0 |
| 3 | 20 | 2.5 | | 9 | 16 | 2.0 |
| 4 | 16 | 2.0 | | 10 | 16 | 2.0 |
| 5 | 20 | 2.5 | | 11 | 12 | 1.5 |
| 6 | 24 | 3.0 | | 12 | 24 | 3.0 |

Total 220 h, 27.5 weeks. `STATE.json` is authoritative if these differ.

## Universal gate (every module)

Module N+1 unlocks only when all four pass: (1) first-principles edge case,
(2) 1st-line pushback defended without designing the fix, (3) four-tier
compression, (4) `assurance-grader` verdict `PASS` against the module's
**artifact criteria** below. Details: `spec/MODULE_LOOP.md`, stage 5.

---

# Module 1: Risk, controls & independence

**Slug:** `m01-risk-controls-independence` · **Time-box:** 16 h · **Status:** expanded 2026-11-17

## I/O contract (frozen)

| | |
|---|---|
| **Input** | None (first module). Starts from the Larkspur Desk brief above. |
| **Output → Module 2** | A **risk & control register** for Larkspur Desk's identity and access layer at `labs/m01-risk-controls-independence/register/risk_control_register.csv`, with the columns defined below. |

## Concepts (new in this module)

Later modules cite these by ID and do not re-teach them.

| ID | Concept | Primary source |
|---|---|---|
| M1-C1 | Risk as likelihood × impact; the risk model (threat source, threat event, vulnerability, predisposing condition) | S2 |
| M1-C2 | Inherent vs residual risk; risk appetite and tolerance; risk response | S8 |
| M1-C3 | Control objectives and types (preventive, detective, corrective); **Test of Design vs Test of Operating Effectiveness** | S5 |
| M1-C4 | **Evidence hierarchy:** re-performance > inspection > observation > inquiry; why inquiry alone is never enough | S5, S4 |
| M1-C5 | Evidence relevance and reliability; information produced by the entity; **population completeness** | S4 |
| M1-C6 | Three Lines Model; independence and objectivity; what the 2nd line may test, state, and must not design | S1 |
| M1-C7 | Security design principles: least privilege, fail-safe defaults, complete mediation, separation of privilege (SoD), economy of mechanism, open design, least common mechanism, psychological acceptability; CIA; defense in depth | S6, S9 |
| M1-C8 | Zero trust as a design stance: no implicit trust from network location, per-request decisions | S7 |
| M1-C9 | The risk & control register as the 2nd line's working artifact | S8 |
| M1-C10 | Assessment methods in a second vocabulary (examine / interview / test) and how they map onto C4 | S3 |

**Used here, taught later (so nothing is taught twice):**
- *5 C's finding form.* Module 1 uses the template in `spec/SCHEMAS.md` §3 as a
  form to fill in. The craft of writing and landing findings is Module 12.
- *Sampling.* Module 1 tests full populations only. Sampling and its
  justification are Module 4.
- *Severity rating.* Findings carry `severity: null` until Module 4.

## Sources

All loaded 2026-11-17. "Convert" shows the state of the copy in
`/literature/m01/` (index: `literature/SOURCES.md`; fetch list:
`literature/sources.json`).

| ID | Source | Use in module | Access | Convert |
|---|---|---|---|---|
| S1 | The IIA, *The IIA's Three Lines Model: An update of the Three Lines of Defense* (2020). [Landing](https://www.theiia.org/en/content/position-papers/2020/the-iias-three-lines-model-an-update-of-the-three-lines-of-defense/) · [PDF](https://www.theiia.org/globalassets/documents/resources/the-iias-three-lines-model-an-update-of-the-three-lines-of-defense-july-2020/three-lines-model-updated-english.pdf) | M1-C6 | Free | Done |
| S2 | NIST SP 800-30 Rev. 1, *Guide for Conducting Risk Assessments* (Sep 2012, Final). [Landing](https://csrc.nist.gov/pubs/sp/800/30/r1/final) · [PDF](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf) | M1-C1 | Free | Done |
| S3 | NIST SP 800-53A Rev. 5, *Assessing Security and Privacy Controls in Information Systems and Organizations* (Jan 2022, Final). [Landing](https://csrc.nist.gov/pubs/sp/800/53/a/r5/final) · [PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53Ar5.pdf) | M1-C10 | Free | Done: chapters 1–3, start of the AC family, Appendix C (Assessment Method Descriptions) and the later appendices |
| S4 | PCAOB, *AS 1105: Audit Evidence*. [Standard](https://pcaobus.org/oversight/standards/auditing-standards/details/AS1105). Relevance and reliability .06–.08; information produced by the company .10; procedures .15–.21 (inspection, observation, inquiry, confirmation, recalculation, reperformance, analytical procedures) | M1-C4, M1-C5 | Free, HTML only | **Manual:** site refuses automated clients; save as PDF into `literature/_inbox/` |
| S5 | PCAOB, *AS 2201: An Audit of Internal Control Over Financial Reporting That Is Integrated with An Audit of Financial Statements*. [Standard](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201). Design effectiveness .42; operating effectiveness .44–.45; persuasiveness ordering .50 | M1-C3, M1-C4 | Free, HTML only | **Manual:** same as S4 |
| S6 | Saltzer & Schroeder, "The Protection of Information in Computer Systems," *Proceedings of the IEEE* 63(9), Sep 1975, pp. 1278–1308, DOI 10.1109/PROC.1975.9939. [IEEE Xplore](https://ieeexplore.ieee.org/document/1451869) · free author copy at [MIT](https://web.mit.edu/Saltzer/www/publications/protection/index.html) | M1-C7 | Free (author copy) | Done: Section I, which states all eight design principles |
| S7 | NIST SP 800-207, *Zero Trust Architecture* (Aug 2020, Final). [Landing](https://csrc.nist.gov/pubs/sp/800/207/final) · [PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf) | M1-C8 | Free | Done (whole document; see §2.1 Tenets of Zero Trust) |
| S8 | NIST IR 8286 Rev. 1, *Integrating Cybersecurity and Enterprise Risk Management (ERM)* (Final, 18 Dec 2025). [Landing](https://csrc.nist.gov/pubs/ir/8286/r1/final) · [PDF](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8286r1.pdf). The landing page also lists a risk register template (xlsx) and JSON schema | M1-C2, M1-C9 | Free | Done (register guidance: Table 1 and Appendices D–E) |
| S9 | NIST SP 800-53 Rev. 5, controls **AC-2 Account Management**, **AC-5 Separation of Duties**, **AC-6 Least Privilege**, **CA-7 Continuous Monitoring**. [Catalog (CPRT, Release 5.2.0)](https://csrc.nist.gov/projects/cprt/catalog#/cprt/framework/version/SP_800_53_5_2_0/home?element=AC-02) · [Publication](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) | Lab criteria | Free | No (cite by control ID) |
| S10 | MITRE ATT&CK Enterprise, content v20.1: [T1078 Valid Accounts](https://attack.mitre.org/techniques/T1078/), [T1098 Account Manipulation](https://attack.mitre.org/techniques/T1098/), [T1136 Create Account](https://attack.mitre.org/techniques/T1136/), [T1087 Account Discovery](https://attack.mitre.org/techniques/T1087/) | Red-team step | Free | No (cite by technique ID) |

**Reference only (not converted, not required reading):**

- ISO 31000:2018, *Risk management — Guidelines* ([iso.org](https://www.iso.org/standard/31000)). Paywalled. Under revision; a DIS successor is in development, so re-check before citing in the portfolio.
- COSO, *Internal Control — Integrated Framework* (2013), executive summary, linked from [coso.org/guidance-on-ic](https://www.coso.org/guidance-on-ic). The page states no licence terms, so read it at the source.
- The IIA, *Global Internal Audit Standards* (issued 9 Jan 2024, effective 9 Jan 2025), [free PDF page](https://www.theiia.org/en/standards/2024-standards/global-internal-audit-standards/free-documents/complete-global-internal-audit-standards/). Optional depth on independence and objectivity. Cached in `/literature/m01/`.
- NIST SP 800-160 Vol. 1 Rev. 1, *Engineering Trustworthy Secure Systems* (Nov 2022), [landing](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final). Optional modern counterpart to S6. Appendix D (Trustworthy Secure Design) and Appendix E (Principles for Trustworthy Secure Design) are cached in `/literature/m01/`; the appendix names were read from the PDF's own table of contents.

**Caveats to carry into pre-flight:**

- NIST IR 8286 (2020) was withdrawn on 18 Dec 2025; cite Rev. 1 only. The PDF itself contains the register guidance: Table 1 (notional register template elements), Appendix D (excerpt from a notional cybersecurity risk register) and Appendix E (notional enterprise risk register).
- The S1 landing page is dated Sep 2020 and the PDF path says July 2020; the PDF's own copyright line says 2020 with no month. Cite it as 2020.
- S2's appendices cover threat sources, threat events, vulnerabilities and predisposing conditions, likelihood, impact, and risk determination (headings read from the converted file). Take appendix letters and section numbers from the converted text at ingestion, never from memory. PCAOB paragraph numbers above were read from the live pages.
- **Module 1 pre-flight is not finished until S4 and S5 are saved from a browser and converted.** M1-C3, C4 and C5 depend on them.
- AS 2201 amendments to .09 and a new .99 take effect 15 Dec 2026; they do not touch .42–.50.
- T1078.004 Cloud Accounts exists (verified) and is held for Module 3.

## Stage 1: dilemma and contrastive pair

**Dilemma (unsolved, presented cold).** Larkspur Desk's quarterly user access
review has passed four quarters running: every account on the review list was
certified by its owner, on time, with sign-off. Last month a login came from the
account of a contractor who left in the spring. The control owner's position:
"The control operated effectively. 100% of reviewed accounts were reviewed."
As the 2nd line: is that statement true, is it sufficient, and what would you
need in your hands to know?

**Contrastive pair.** Two Q3 access-review evidence packages, A and B. Both show
100% completion, reviewer sign-offs, timestamps inside the window, and
revocations actioned. In one, the review list reconciles to the identity system
of record. In the other, the list was produced by a query that silently leaves
some accounts out. The learner gets both packages plus read access to the raw
tables, and writes a diagnosis and a test procedure before any teaching.

The pair is built by `first-line-engineer`; which package is flawed, and how, is
recorded only in `.sealed/ANSWER_KEY.md`.

## Stage 3: lab design

**Folder:** `labs/m01-risk-controls-independence/` · **Harness:** `assurance-harness/m01/`
· **Tools:** Python, pytest, DuckDB (SQL). OPA/Rego is deferred to Module 3.

### 3.1 First line (`first-line-engineer`)

Build Larkspur Desk's identity and access layer as a local simulator backed by
DuckDB, with a seeded generator in `assurance-harness/generators/m01_iam.py`
that emits both a `planted` and a `clean` dataset.

| Table | Approx. rows | Notes |
|---|---|---|
| `hr_identities` | 3,000 | Employees and contractors, with hire and termination timestamps |
| `iam_accounts` | 12,000 | Human and service accounts; the system of record |
| `entitlements` | 45,000 | Account-to-permission grants, with grant time and approval reference |
| `access_requests` | 40,000 | Provisioning approvals |
| `access_reviews` | 22,000 | Two quarters of review decisions |
| `auth_events` | 120,000 | Login telemetry over the period |

Controls the 1st line documents in `SYSTEM.md`, each with an owner:

| ID | Control | Criteria |
|---|---|---|
| LD-AC-01 | Every entitlement grant has an owner-approved request dated before the grant | AC-2 |
| LD-AC-02 | Accounts of terminated identities are disabled within 24 hours of HR termination | AC-2 |
| LD-AC-03 | Every active account, human and service, is certified by its owner each quarter; revocations are actioned within 7 days | AC-2, CA-7 |
| LD-AC-04 | No identity holds a toxic pair (`refund.issue` + `refund.approve`; `iam.admin` + `auditlog.admin`) | AC-5 |
| LD-AC-05 | Privileged roles are limited to named owners | AC-6 |

Planted in the `planted` dataset and sealed: an incomplete review population,
drift in deprovisioning timeliness over the period, accounts missing from
inventory, lapsed exceptions, and a survivorship gap in `auth_events`. The
`clean` dataset has none. Realistic constraint for the build: a two-day
deadline and a legacy HR export with inconsistent identifiers.

### 3.2 Red team (`red-team`)

Against the local simulator only. Demonstrate, with a re-runnable trace:
account discovery (T1087), use of an orphaned account (T1078), an entitlement
added outside the approval workflow (T1098), and an account created outside
provisioning (T1136). For each: what it achieved and what telemetry it did or
did not leave. No reading of `.sealed/`.

### 3.3 Second line (the learner)

1. **ToD** for LD-AC-02, LD-AC-03, LD-AC-04: if the control operated exactly as
   written, would it meet its objective? Use the red-team trace as challenge
   evidence.
2. **ToE** procedures for LD-AC-02 and LD-AC-03, written in prose first, then
   turned into pytest + DuckDB SQL in `assurance-harness/m01/`. Each procedure
   begins by reconciling its population to the system of record, states its
   evidence type, and tests the full population.
3. Run each ToE on `planted` and `clean`; write result records
   (`spec/SCHEMAS.md` §2).
4. One **5 C's finding** on the most significant failure.
5. Build the **risk & control register** (the output).

**Core vs Nice-to-have.** Core is the list above. Nice-to-have, cut first on
overrun: ToE for LD-AC-04, ToD/ToE for LD-AC-01 and LD-AC-05.

### Mental models woven in (law 4)

- **Sensitivity and specificity.** A ToE is a diagnostic test. Detecting the
  planted exceptions is its sensitivity; reporting nothing on `clean` is its
  specificity. The learner reports both for each procedure.
- **Bayesian updating.** Before each ToE the learner writes a prior that the
  control is effective, then updates after each piece of evidence, and explains
  why a sign-off (inquiry) moves the estimate far less than a re-performed query.

### Register columns (output contract)

`risk_id, asset, threat_event, vulnerability, likelihood_1to5, impact_1to5,
inherent_score, control_id, control_description, control_type, control_owner,
design_principle, tod_result, toe_result, evidence_type, test_procedure_ref,
residual_likelihood_1to5, residual_impact_1to5, residual_score,
appetite_threshold, within_appetite, attack_technique_ids`

`control_type` ∈ preventive / detective / corrective. `tod_result` and
`toe_result` ∈ effective / ineffective / not_tested. `evidence_type` ∈
reperformance / inspection / observation / inquiry. `attack_technique_ids` holds
ATT&CK IDs from S10 and is the hook Module 2 builds on.

## Gate: artifact criteria (what `assurance-grader` checks)

1. The register exists at the contract path with every column above, at least
   8 risks, each mapped to at least one control, with inherent and residual
   scores and an appetite threshold.
2. Written ToD exists for LD-AC-02, LD-AC-03, and LD-AC-04, each reaching a
   stated conclusion with reasons.
3. Written ToE procedures and harness tests exist for LD-AC-02 and LD-AC-03;
   `pytest assurance-harness/m01 -q -p no:cacheprovider` exits 0.
4. Each ToE reconciles its population to `iam_accounts` (or states and
   justifies another system of record) before testing.
5. Result records exist for both datasets. On `planted`, every sealed flaw
   affecting LD-AC-02 and LD-AC-03 is detected. On `clean`, zero exceptions.
6. At least one ToE procedure reproduces from its written steps alone.
7. One 5 C's finding has all five sections, cites a result record as evidence,
   and does not design the 1st line's fix.
8. Every register row with a `toe_result` names its `evidence_type`, and no
   conclusion of `effective` rests on inquiry alone.

**Edge-case prompts for gate check 1** (the tutor picks or varies one): the
review population is drawn from the HR roster instead of the IAM system; the
period of reliance spans a migration between identity systems; the 2nd line
wrote the query the 1st line now uses to build its own review list.

## Cert mapping (Module 1)

Domain names are verified (see reference below). The mapping of concepts to
domains is this curriculum's judgment, not the certifying bodies'.

| Concept | CISA | AAIA | AIGP | CISSP | CISM | 42001 LA (PECB) |
|---|---|---|---|---|---|---|
| M1-C1, C2, C9 risk and the register | D2 | D1 | I | D1 | D2 | D1 |
| M1-C3 ToD vs ToE | D1 | D3 | — | D6 | D3 | D5 |
| M1-C4, C5, C10 evidence and populations | D1 | D3 | — | D6 | — | D3, D5 |
| M1-C6 Three Lines, independence | D1, D2 | D1 | I | D1 | D1 | D3 |
| M1-C7, C8 design principles, zero trust | D5 | — | — | D3, D5 | D3 | — |

---

# Modules 2–12: I/O contracts

Contract only. No lab design or cert mapping until JIT expansion. Sources for
Modules 2 and 3 were verified and cached early for offline travel; that is the
only exception, and each pre-flight still re-checks them for currency.
"Artifact criteria" are what the grader will check; the universal gate applies
to all.

## Module 2: CTI tradecraft & threat modeling
`m02-cti-threat-modeling` · 16 h

- **Core concepts:** Diamond Model, Kill Chain, ATT&CK, infrastructure pivoting, passive DNS/TLS, STIX/TAXII, live feeds (CISA KEV), ACH matrices; STRIDE, attack trees, trust boundaries.
- **Input (from M1):** the risk & control register.
- **Pre-cached sources (travel prep, verified 2026-11-17):** `/literature/m02/`, indexed in `literature/SOURCES.md`. Lab design and cert mapping remain just-in-time.
- **Output → M3:** an adversary profile and a threat model for Larkspur Desk, plus a ranked list of test priorities, each tracing to a register `risk_id`.
- **Artifact criteria:** the profile covers all four Diamond vertices and cites at least one live-feed item with its retrieval date; an ACH matrix weighs at least three hypotheses with disconfirming evidence; the threat model covers every trust boundary; every test priority traces to a register risk and a technique ID; the intelligence is expressed as a machine-readable bundle that validates.

## Module 3: Hyperscale security & Google's model
`m03-hyperscale-security` · 20 h

- **Core concepts:** IAM, segmentation, encryption/KMS, logging, CI/CD, secrets; BeyondCorp / BeyondProd; "controls are code, evidence is data".
- **Input (from M2):** the threat model and test priorities.
- **Pre-cached sources (travel prep, verified 2026-11-17):** `/literature/m03/`, indexed in `literature/SOURCES.md`. Lab design and cert mapping remain just-in-time.
- **Output → M4:** a sandbox with controls defined as code and **real audit-log telemetry**, or explicitly labeled synthetic logs if live GCP is deferred.
- **Pre-flight gate (replaces any Phase 0 cloud setup):** before the lab, provision a dedicated GCP project with a billing budget and alerts, no production data, and teardown scripts. Terraform/OpenTofu with local mocks is fine for *learning* infrastructure-as-code, but the output contract needs real audit logs, so the gate passes only with the live sandbox **or** with synthetic logs labeled as such in `STATE.json` (`telemetry_source`).
- **Artifact criteria:** `telemetry_source` is set; controls exist as code for each concept family; at least 10,000 log rows are exported with a schema note; each control traces to an M2 test priority; teardown has been run once and verified.

## Module 4: Assurance-as-code foundations
`m04-assurance-as-code` · 16 h

- **Core concepts:** sampling and its justification, period of reliance, exceptions, reproducible procedures, continuous testing, deficiency severity rating.
- **Input (from M3):** the sandbox controls and telemetry.
- **Output → M5:** **Harness v1** testing Module 3's controls (runs on synthetic data either way).
- **Artifact criteria:** at least one test per M3 control family; each states its population, sampling or full-population rationale, period of reliance, and exception handling; two consecutive runs give identical results; one command runs the whole harness; every open finding carries a severity from a written rubric.

## Module 5: Privacy engineering & testing
`m05-privacy-engineering` · 20 h

- **Core concepts:** data minimization, purpose limitation, retention, access/deletion rights; data lineage; deletion verification; de-identification, k-anonymity, differential privacy; PIAs; GDPR, CCPA/CPRA, FTC enforcement including Google's 2011 consent order. **The case library unparks here.**
- **Input (from M4):** Harness v1.
- **Output → M6:** privacy tests in the harness **+ a synthetic PII/customer corpus + a data-lineage & retention manifest + a deletion log**.
- **Artifact criteria:** the corpus has at least 10,000 synthetic records from a seeded generator and no real personal data; the manifest lists every store, field, purpose, and retention period; the deletion log records IDs and timestamps; a harness test proves deleted records are absent from every store in the manifest; k-anonymity is measured on a de-identified export; a PIA exists for Larkspur Desk.

## Module 6: AI/ML internals & the 5 paradigm shifts
`m06-ai-ml-internals` · 24 h

- **Core concepts:** ML lifecycle attack surfaces; tokens, context, system prompts, fine-tuning, RLHF, serving; RAG; shared instruction/data channel, data-as-behavior, probabilistic outputs, memorization, agency.
- **Input (from M5):** the corpus, the lineage manifest, the deletion log.
- **Output → M7:** built as 1st line, a local RAG app whose **vector store ingests the Module 5 corpus**, plus a **small LoRA fine-tune of a local model on a slice of that corpus** (so memorization attacks are real, not only retrieval leakage). The lineage manifest is carried forward and extended.
- **Artifact criteria:** the app answers from the corpus and returns retrieved record IDs; the fine-tune artifact, its config, and the exact slice of record IDs are recorded; the manifest now lists the vector store and the model weights as data stores; each of the five shifts is demonstrated on the app; large installs were approved first.

## Module 7: AI threat taxonomy & red teaming
`m07-ai-threats-red-teaming` · 24 h

- **Core concepts:** Google SAIF (primary vocabulary), MITRE ATLAS, OWASP LLM Top 10, NIST AI 100-2; direct/indirect injection, jailbreaks, poisoning, retrieval leakage, training-data extraction, membership inference, inversion, evasion, insecure output handling; Gandalf, PortSwigger LLM labs, garak, PyRIT, promptfoo, Burp.
- **Input (from M6):** the RAG app, the fine-tuned model, the manifest, and the M5 deletion log.
- **Output → M8:** an attack corpus **+ 1st-line candidate guardrails** (input/output filters, system-prompt hardening, retrieval access controls) **+ initial red-team bypass results**. Includes a **deletion-verification test:** are records deleted in Module 5 still retrievable from the vector store or extractable from the fine-tuned model?
- **Artifact criteria:** every attack is labeled with a SAIF risk and an ATLAS technique; each guardrail is implemented and documented by the 1st line; bypass results are recorded per attack per guardrail; the deletion-verification test has run against both the vector store and the model; every attack ran locally or inside the scope fence.

## Module 8: AI evals & measurement science
`m08-ai-evals-measurement` · 16 h

- **Core concepts:** eval design, defining failure criteria up front, sample size and statistical power, confidence intervals on failure rates, LLM-as-judge pitfalls.
- **Input (from M7):** the attack corpus, guardrails, and bypass results.
- **Output → M9:** a **statistical ToE of the Module 7 guardrails**, including privacy-leak rates.
- **Artifact criteria:** failure criteria are written and dated before any measurement run; sample sizes are justified by a power calculation; each failure rate has a confidence interval; any LLM judge is validated against a human-labeled subset with agreement reported; a privacy-leak rate with its interval is reported; each guardrail has a conclusion.

## Module 9: Agentic & MCP security
`m09-agentic-mcp-security` · 16 h

- **Core concepts:** tool permissions, confused deputy, excessive agency, MCP server threat models, human-in-the-loop controls.
- **Input (from M8):** the measured app and its eval harness.
- **Output → M10:** an **agent extension of the app + agent-specific tests**.
- **Artifact criteria:** the agent uses at least two tools, one through an MCP server; the tool permission model is documented; confused-deputy and excessive-agency tests run in the harness; a human-in-the-loop control on at least one high-impact action is tested; an MCP server threat model exists.

## Module 10: AI/ML supply chain integrity
`m10-ai-supply-chain` · 16 h

- **Core concepts:** SLSA, SBOM/AI-BOM, model signing, pickle/deserialization scanning, dataset provenance (ties to the Module 5 lineage manifest).
- **Input (from M9):** the agent app, the fine-tuned model, the lineage manifest.
- **Output → M11:** **supply-chain controls + tests for the app**, including the fine-tuned model's provenance.
- **Artifact criteria:** an SBOM and an AI-BOM are generated; the model artifact is signed and a test fails on tampering; model files pass a deserialization scan; a test verifies the provenance chain from the M5 manifest to the fine-tune; a build-integrity self-assessment cites evidence.

## Module 11: Frameworks, regulation & severity
`m11-frameworks-regulation-severity` · 12 h

- **Core concepts:** NIST CSF 2.0, SP 800-53, ISO 27001, ISO/IEC 42001, NIST AI RMF, EU AI Act, SOC 2, FedRAMP; mapping findings to criteria.
- **Input (from M10):** every open finding from Modules 1–10 with its evidence.
- **Output → M12:** **every open finding mapped to criteria and rated**.
- **Artifact criteria:** a findings register in which each finding maps to at least one clause in at least two frameworks, with verified clause citations; one severity rubric applied consistently; conflicts between frameworks noted; no unmapped finding.

## Module 12: Program management, 5 C's & influence
`m12-program-management-capstone` · 24 h

- **Core concepts:** scoping vague mandates; metrics (coverage, pass rate, remediation aging, KRIs); remediation tracking and re-validation; 5 C's; multi-audience briefs; attorney-client privilege.
- **Input (from M11):** the mapped and rated findings register, the harness, the threat models.
- **Output:** the **Capstone**: a full AI agent threat model, 3 reproducible ToD/ToE procedures running in the harness, one 5 C's finding, and four audience briefs (raw trace, engineer, legal, executive), published as a sanitized portfolio piece.
- **Artifact criteria:** all capstone elements exist and the three procedures run; program metrics are computed from harness results; at least one finding is tracked through remediation and re-validation; the portfolio piece contains synthetic data only.

---

# Nice-to-have (only if a module finishes under its time-box)

- **Control crosswalk** (`spec/CROSSWALK.md`): a lightweight table mapping each control primitive to the frameworks that require it, filled in as modules introduce frameworks. Not a graph database.
- **Chaos regression:** silently re-plant a failure mode from an earlier module in a later lab (for example, the Module 1 population-completeness flaw inside the Module 9 agent lab).
- **AI VRP submission:** only after the capstone, and only within the program's published scope and rules.

# Maybe-later (parked, with triggers; mirrored in `STATE.json`)

- **Curated conference lectures:** only when a module's written sources prove thin.
- **Real incident & enforcement case library:** starts at Module 5.
- **Calibration ledger** (confidence before each test, Brier scoring): after the capstone.

---

# Cert domain reference

Loaded from each certifying body's own pages on 2026-11-17. Re-check at each
module's JIT expansion; two outlines are in motion.

**ISACA CISA** (job practice effective 1 Aug 2024) · [outline](https://www.isaca.org/credentialing/cisa/cisa-exam-content-outline)
D1 Information System Auditing Process 18% · D2 Governance & Management of IT 18% · D3 Information Systems Acquisition, Development & Implementation 12% · D4 Information Systems Operations and Business Resilience 26% · D5 Protection of Information Assets 26%

**ISACA AAIA, Advanced in AI Audit** · [outline](https://www.isaca.org/credentialing/aaia/aaia-exam-content-outline)
D1 AI Governance and Risk 33% · D2 AI Operations 46% · D3 AI Auditing Tools and Techniques 21%. Requires CISA or another qualifying audit designation. Effective date not stated by ISACA.

**IAPP AIGP** (Body of Knowledge 2.1, effective 2 Feb 2026) · [program page](https://iapp.org/certify/aigp/)
I Understanding the foundations of AI governance · II Understanding how laws, standards and frameworks apply to AI · III Understanding how to govern AI development · IV Understanding how to govern AI deployment and use. IAPP publishes question-count ranges per domain, not percentages.

**ISC2 CISSP** (outline effective 15 Apr 2024) · [outline](https://www.isc2.org/certifications/cissp/cissp-certification-exam-outline)
D1 Security and Risk Management 16% · D2 Asset Security 10% · D3 Security Architecture and Engineering 13% · D4 Communication and Network Security 13% · D5 Identity and Access Management (IAM) 13% · D6 Security Assessment and Testing 12% · D7 Security Operations 13% · D8 Software Development Security 10%.
**A new outline takes effect 15 Apr 2027**; its domains and weights are `UNVERIFIED` here.

**ISACA CISM** (outline effective 3 Nov 2026) · [outline](https://www.isaca.org/credentialing/cism/cism-exam-content-outline)
D1 Information Security Governance 18% · D2 Information Security Risk Management 20% · D3 Information Security Program 33% · D4 Incident Management 29%

**ISO/IEC 42001 Lead Auditor.** The standard is *ISO/IEC 42001:2023, Information technology — Artificial intelligence — Management system*, edition 1 ([iso.org](https://www.iso.org/standard/42001)). ISO defines no auditor exam. The domains below are **PECB's** training-scheme domains, not ISO's ([PECB](https://pecb.com/en/education-and-certification-for-individuals/iso-iec-42001/iso-iec-42001-lead-auditor)):
D1 Fundamental principles and concepts of an AI management system · D2 AI management system requirements · D3 Fundamental audit concepts and principles · D4 Preparing an ISO/IEC 42001 audit · D5 Conducting an ISO/IEC 42001 audit · D6 Closing an ISO/IEC 42001 audit · D7 Managing an ISO/IEC 42001 audit program
