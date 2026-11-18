import { useState } from "react";
import type { Overview, Room, RunState } from "../api/types";
import { ErrorNote, Loading, Tabs } from "../components/ui";
import { useResource } from "../lib/repo";
import { HeuristicForm } from "./room/HeuristicForm";
import { LeftPane } from "./room/LeftPane";
import { PairViewer } from "./room/PairViewer";
import { Runner } from "./room/Runner";
import { WritePane } from "./room/WritePane";

type WorkTab = "pair" | "write" | "heuristic";
const NOW: Partial<Record<string, WorkTab>> = { incubation: "pair", lab: "write", heuristics: "heuristic", gate: "write" };

export function ActiveRoom({ overview, run, onRun }: { overview: Overview; run: RunState; onRun: () => void }) {
  const id = overview.current_module;
  const room = useResource<Room>(`/api/module/${id}/room`,
    ["state", "lab", "results", "harness", "curriculum", "literature", "heuristics"]);
  const [tab, setTab] = useState<WorkTab>("pair");
  const [openPath, setOpenPath] = useState<string | null>(null);

  if (room.error && !room.data) return <section className="view pad"><ErrorNote>{room.error}</ErrorNote></section>;
  if (!room.data) return <section className="view"><Loading what="the active room" /></section>;
  const r = room.data;
  const now = NOW[r.stage];

  return (
    <section className="view view-room" aria-label={`Active Room: Module ${id}`}>
      <LeftPane room={r}
        onOpenFile={(path) => { setOpenPath(path); setTab("write"); }}
        onOpenTab={(t) => setTab(t)} />

      <div className="pane-right">
        <div className="panel pane-work" aria-label="Workbench">
          <div className="pane-head">
            <span className="pane-title">Workbench</span>
            <Tabs name="work" label="Workbench" value={tab} onChange={setTab} tabs={[
              { id: "pair", label: "Contrastive pair", now: now === "pair" },
              { id: "write", label: "Write", now: now === "write" },
              { id: "heuristic", label: "Add heuristic", now: now === "heuristic" },
            ]} />
          </div>
          <div className="work-body" id="work-panel" role="tabpanel" aria-labelledby={`work-tab-${tab}`}>
            {tab === "pair" && <PairViewer pairs={r.lab.pairs} />}
            {tab === "write" && <WritePane lab={r.lab} moduleId={id} openPath={openPath} onOpen={setOpenPath} />}
            {tab === "heuristic" && <HeuristicForm moduleId={id} />}
          </div>
        </div>

        <Runner run={run} target={r.harness_target} results={r.results} onRun={onRun} />
      </div>
    </section>
  );
}
