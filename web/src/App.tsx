import { useCallback, useEffect, useRef, useState } from "react";
import { motion, MotionConfig } from "motion/react";
import { ApiError, run as runCommand } from "./api/client";
import type { Overview, RunState } from "./api/types";
import { SyncDialog, type SyncKind } from "./components/SyncDialog";
import { ErrorNote, Loading } from "./components/ui";
import { anyDirty } from "./lib/drafts";
import { RepoProvider, ToastProvider, useBus, useLiveMode, useResource, useToast } from "./lib/repo";
import { ActiveRoom } from "./views/ActiveRoom";
import { Arsenal } from "./views/Arsenal";
import { CampaignMap } from "./views/CampaignMap";

type View = "map" | "room" | "arsenal";
const VIEWS: { id: View; label: string }[] = [
  { id: "map", label: "Campaign Map" }, { id: "room", label: "Active Room" }, { id: "arsenal", label: "Arsenal & Vault" },
];
const IDLE: RunState = { running: false, cmd: "", output: "", code: null, tests: null, note: null, error: null };
const LIVE_LABEL = { live: "watching repo", polling: "polling repo", offline: "backend offline" };

const viewFromHash = (): View => {
  const h = window.location.hash.slice(1);
  return h === "room" || h === "arsenal" ? h : "map";
};

export default function App() {
  return (
    // Motion is functional only. reducedMotion="user" turns transforms off for
    // anyone who has asked their system for less motion.
    <MotionConfig reducedMotion="user" transition={{ duration: 0.15, ease: [0.2, 0, 0, 1] }}>
      <RepoProvider><ToastProvider><Shell /></ToastProvider></RepoProvider>
    </MotionConfig>
  );
}

function Shell() {
  const bus = useBus();
  const toast = useToast();
  const live = useLiveMode();
  const [view, setView] = useState<View>(viewFromHash);
  const [sync, setSync] = useState<SyncKind | null>(null);
  const [harness, setHarness] = useState<RunState>(IDLE);
  const [stageChanged, setStageChanged] = useState(0);
  const overview = useResource<Overview>("/api/overview", ["state", "flashcards", "heuristics", "curriculum"]);
  const validity = useResource<{ valid: boolean; output: string }>("/api/state/validity", ["state"]);

  // The view lives in the URL hash: no browser storage is used.
  useEffect(() => {
    const onHash = () => setView(viewFromHash());
    window.addEventListener("hashchange", onHash);
    return () => window.removeEventListener("hashchange", onHash);
  }, []);
  const go = (v: View) => { window.location.hash = v; setView(v); };

  useEffect(() => {
    const warn = (e: BeforeUnloadEvent) => { if (anyDirty()) e.preventDefault(); };
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, []);

  // Stage-change feedback. The app never moves a stage: it only notices that
  // STATE.json did, because Claude Code wrote it.
  const last = useRef<{ module: number; stage: string } | null>(null);
  useEffect(() => {
    const o = overview.data;
    if (!o) return;
    const prev = last.current;
    last.current = { module: o.current_module, stage: o.current_stage };
    if (prev && (prev.module !== o.current_module || prev.stage !== o.current_stage)) {
      setStageChanged((n) => n + 1);
      toast(prev.module !== o.current_module
        ? `STATE.json changed: now Module ${o.current_module}, stage ${o.current_stage}`
        : `STATE.json changed: stage ${prev.stage} → ${o.current_stage}`);
    }
  }, [overview.data, toast]);

  const runHarness = useCallback(async () => {
    setHarness({ ...IDLE, running: true });
    try {
      await runCommand("harness", (e) => setHarness((s) =>
        e.t === "cmd" ? { ...s, cmd: e.d }
          : e.t === "out" ? { ...s, output: s.output + e.d }
            : { ...s, running: false, code: e.code, tests: e.tests ?? [], note: e.note ?? null }));
    } catch (e) {
      setHarness((s) => ({ ...s, running: false, error: e instanceof ApiError ? e.message : "The backend did not answer." }));
    } finally {
      setHarness((s) => (s.running ? { ...s, running: false, error: s.error ?? "The run ended without an exit code." } : s));
      bus.emit(["results"]);
    }
  }, [bus]);

  const invalid = validity.data && !validity.data.valid ? validity.data.output : null;

  return (
    <div className="app">
      <a className="skip-link" href="#main">Skip to content</a>
      <div>
        {invalid && (
          <div className="strip" role="alert">
            <strong>scripts/validate_state.py reports a problem with STATE.json.</strong>
            <pre>{invalid}</pre>
          </div>
        )}
      </div>

      <header className="topbar">
        <div className="brand"><span className="brand-name">Assurance Engine</span><span className="brand-sub">Mission Control</span></div>
        <nav className="views" aria-label="Views">
          {VIEWS.map((v) => (
            <button key={v.id} className="view-tab" aria-current={view === v.id ? "page" : undefined} onClick={() => go(v.id)}>
              {v.label}
              {view === v.id && <motion.span layoutId="view-underline" className="view-underline" transition={{ duration: 0.24 }} />}
            </button>
          ))}
        </nav>
        <div style={{ marginLeft: "auto", display: "flex", alignItems: "center", gap: 8 }}>
          <span className="live" data-mode={live} role="status"><i aria-hidden="true" />{LIVE_LABEL[live]}</span>
          <button className="btn" onClick={() => setSync("down")}>Sync Down</button>
          <button className="btn" onClick={() => setSync("up")}>Sync Up</button>
        </div>
      </header>

      <main id="main" style={{ minHeight: 0 }}>
        {overview.error && !overview.data && <div className="pad"><ErrorNote>STATE.json could not be loaded: {overview.error}</ErrorNote></div>}
        {!overview.data && !overview.error && <Loading what="STATE.json" />}
        {overview.data && (
          // Pane transition: the incoming view settles in. There is no exit
          // animation to wait on, so a view change is never held up.
          <motion.div key={view} className="view" initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.24 }}>
            {view === "map" && <CampaignMap overview={overview.data} lastRun={harness} stageChanged={stageChanged} onEnterRoom={() => go("room")} />}
            {view === "room" && <ActiveRoom overview={overview.data} run={harness} onRun={() => void runHarness()} />}
            {view === "arsenal" && <Arsenal />}
          </motion.div>
        )}
      </main>

      {sync && <SyncDialog key={sync} kind={sync} onClose={() => setSync(null)} />}
    </div>
  );
}
