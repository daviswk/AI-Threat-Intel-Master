// Shapes returned by web/server. The server derives all of these from the repo.

export type Stage = "preflight" | "incubation" | "ingestion" | "lab" | "heuristics" | "gate" | "complete";
export type ModuleStatus = "complete" | "active" | "locked";
export type GateResult = "pending" | "pass" | "fail";

export interface CertCount { cert: string; cards: number }

export interface ModuleView {
  id: number; slug: string; title: string; status: ModuleStatus;
  stage: Stage | null; stage_index: number;
  stage_history: { stage: Stage; entered_on: string }[];
  hours_spent: number; timebox_hours: number; burn_pct: number; over_hours: number; at_cut_line: boolean;
  gate: { edge_case: GateResult; pushback: GateResult; compression: GateResult; artifact_check: GateResult; attempts: number };
  outputs: string[]; nice_to_haves_cut: string[]; expanded: boolean;
  cards: number; certs: CertCount[]; heuristics: number; notes: string[];
}

export interface Overview {
  current_module: number; current_stage: Stage; updated: string; stages: Stage[];
  modules: ModuleView[]; edges: [number, number][];
  totals: { modules_complete: number; modules: number; hours_logged: number; hours_planned: number; cards: number; heuristics: number; certs: CertCount[] };
}

export interface BriefBlock { title: string | null; level: number; markdown: string; withheld: boolean; until?: Stage }
export interface Banner { where: "app" | "cli"; text: string; open?: string; open_tab?: "write" | "heuristic"; open_label?: string }
export interface Prompt { id: string; label: string; text: string }
export interface Pair { name: string; a: string; b: string; files: string[]; only_a: string[]; only_b: string[] }
export interface Authored { group: string; path: string; exists: boolean }
export interface Lab { slug: string; exists: boolean; writable: boolean; files: string[]; pairs: Pair[]; authored: Authored[]; has_trace: boolean; has_cold_attempt: boolean }
export interface ResultRecord { path: string; error?: string; control_id?: string | null; dataset?: string | null; population_size?: number | null; exceptions?: number | null; conclusion?: string | null }
export interface Paper { path: string; name: string; title: string | null; publisher: string | null }

export interface Room {
  module: { id: number; slug: string; title: string; status: string };
  stage: Stage; is_current: boolean;
  briefing: BriefBlock[]; stage_markdown: string; banner: Banner; prompts: Prompt[];
  literature: Paper[]; lab: Lab; results: ResultRecord[]; harness_target: string;
  heuristics_sha256: string | null;
}

export interface FilePayload {
  path: string; exists: boolean; content: string; sha256: string | null; writable: boolean;
  front_matter: Record<string, unknown> | null; body: string;
}

export interface Heuristic { id: string; module: number; n: number; rule: string; evidence: string }
export interface Card { file: string; module: number | null; front: string; back: string; tags: string[] }
export interface Arsenal {
  heuristics: { exists: boolean; sha256: string | null; entries: Heuristic[] };
  flashcards: Card[]; certs: CertCount[]; portfolio: { path: string; title: string | null }[];
}

export interface TestOutcome { file: string; name: string; outcome: "pass" | "fail" | "error" | "skip" }
export type RunName = "harness" | "sync_down" | "sync_up";
export type RunEvent =
  | { t: "cmd"; d: string }
  | { t: "out"; d: string }
  | { t: "exit"; code: number; tests?: TestOutcome[]; note?: string | null };

export interface RunState {
  running: boolean; cmd: string; output: string; code: number | null;
  tests: TestOutcome[] | null; note: string | null; error: string | null;
}
