import { useEffect, useState } from "react";
import { motion } from "motion/react";
import { Lock } from "lucide-react";
import { fileUrl } from "../../api/client";
import type { FilePayload, Room } from "../../api/types";
import { CopyPrompt, ErrorNote, Loading, Markdown, Tabs } from "../../components/ui";
import { useResource } from "../../lib/repo";

type LeftTab = "stage" | "briefing" | "papers";
const SOURCE_FIELDS = ["title", "publisher", "source_url", "retrieved", "licence", "pages"];

export function LeftPane({ room, onOpenFile, onOpenTab }: {
  room: Room; onOpenFile: (path: string) => void; onOpenTab: (tab: "write" | "heuristic") => void;
}) {
  const [tab, setTab] = useState<LeftTab>("stage");
  const [paper, setPaper] = useState<string | null>(null);
  const { banner } = room;

  useEffect(() => {
    if (paper && !room.literature.some((p) => p.path === paper)) setPaper(null);
  }, [room.literature, paper]);
  const openPaper = paper ?? room.literature[0]?.path ?? null;

  return (
    <div className="panel pane-left">
      {/* Stage-change feedback: when the stage (or what it asks for) changes, the
          new banner slides in. Nothing waits on an exit animation. */}
      <>
        <motion.div key={`${room.stage}:${banner.text}`} className="banner" role="status"
          initial={{ opacity: 0, y: -6 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.24 }}>
          <span className="banner-where">Next · {banner.where === "app" ? "in the app" : "in Claude Code"}</span>
          <p className="banner-text">{banner.text}</p>
          <div className="banner-actions">
            {banner.open && <button className="btn btn-primary" onClick={() => onOpenFile(banner.open!)}>{banner.open_label}</button>}
            {banner.open_tab && <button className="btn btn-primary" onClick={() => onOpenTab(banner.open_tab!)}>{banner.open_label}</button>}
            {room.prompts.map((p) => <CopyPrompt key={p.id} label={p.label} text={p.text} />)}
          </div>
        </motion.div>
      </>

      <Tabs name="left" label="Briefing and curriculum" value={tab} onChange={setTab}
        tabs={[{ id: "stage", label: "Stage" }, { id: "briefing", label: "Briefing" }, { id: "papers", label: `Papers (${room.literature.length})` }]} />

      {tab === "papers" && room.literature.length > 0 && (
        <div className="paper-strip" role="tablist" aria-label="Papers for this module">
          {room.literature.map((p) => (
            <button key={p.path} role="tab" aria-selected={p.path === openPaper} title={p.title ?? p.name}
              onClick={() => setPaper(p.path)}>{p.name}</button>
          ))}
        </div>
      )}

      <article className="reader" id="left-panel" role="tabpanel" aria-labelledby={`left-tab-${tab}`} tabIndex={0}>
        {tab === "stage" && (room.stage_markdown
          ? <Markdown source={room.stage_markdown} />
          : <p className="empty">spec/MODULE_LOOP.md has no section for stage "{room.stage}".</p>)}

        {tab === "briefing" && (room.briefing.length === 0
          ? <p className="empty">spec/CURRICULUM.md has no section for this module.</p>
          : room.briefing.map((b, i) => (
            <div key={i}>
              {b.title && (b.withheld
                ? <p className="withheld"><Lock aria-hidden="true" />{b.title}: held back until {b.until}</p>
                : <h3 className="brief-h" data-level={b.level}>{b.title}</h3>)}
              {!b.withheld && b.markdown && <Markdown source={b.markdown} />}
            </div>
          )))}

        {tab === "papers" && (openPaper
          ? <Paper path={openPaper} />
          : <p className="empty">No converted papers in literature/m{String(room.module.id).padStart(2, "0")}/ yet.</p>)}
      </article>
    </div>
  );
}

function Paper({ path }: { path: string }) {
  const file = useResource<FilePayload>(fileUrl(path), ["literature"]);
  if (file.error) return <ErrorNote>{path}: {file.error}</ErrorNote>;
  if (!file.data) return <Loading what={path} />;
  const meta = file.data.front_matter;
  return (
    <>
      {meta && (
        <table className="source-table">
          <tbody>
            {SOURCE_FIELDS.filter((k) => meta[k] != null).map((k) => <tr key={k}><th scope="row">{k}</th><td>{String(meta[k])}</td></tr>)}
          </tbody>
        </table>
      )}
      <Markdown source={file.data.body} />
    </>
  );
}
