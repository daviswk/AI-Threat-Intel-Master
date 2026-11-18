import { useCallback, useEffect, useMemo, useState } from "react";
import { ApiError, fileUrl, get, send } from "../../api/client";
import type { FilePayload, Lab } from "../../api/types";
import { ErrorNote, Loading } from "../../components/ui";
import { getDraft, patchDraft, setDraft, useDirtyPaths, useDraft } from "../../lib/drafts";
import { blankFinding, composeFinding, parseFinding, SECTIONS, STATUSES, type Finding } from "../../lib/finding";
import { useOnChange, useToast } from "../../lib/repo";

/** Editors for the files the learner authors. They save what is typed.
 *  Nothing here drafts, completes or suggests. */
export function WritePane({ lab, moduleId, openPath, onOpen }: {
  lab: Lab; moduleId: number; openPath: string | null; onOpen: (path: string) => void;
}) {
  const dirty = useDirtyPaths();
  const [extra, setExtra] = useState<string[]>([]);       // procedures named here but not yet on disk
  const [control, setControl] = useState("");
  const [kind, setKind] = useState<"tod" | "toe">("toe");

  const files = useMemo(() => {
    const known = new Set(lab.authored.map((f) => f.path));
    const added = extra.filter((p) => !known.has(p)).map((path) => ({ group: "Procedures", path, exists: false }));
    return [...lab.authored, ...added];
  }, [lab.authored, extra]);
  const groups = ["Incubation", "Procedures", "Finding", "Gate briefs"];
  const current = openPath && files.some((f) => f.path === openPath) ? openPath : files[0]?.path ?? null;

  if (!lab.exists) return <p className="empty pad">labs/{lab.slug}/ does not exist yet. Claude Code creates it when the lab is built.</p>;

  const controlOk = /^[A-Za-z0-9]+(-[A-Za-z0-9]+)*$/.test(control);
  const addProcedure = () => {
    const path = `labs/${lab.slug}/procedures/${control}-${kind}.md`;
    setExtra((list) => (list.includes(path) ? list : [...list, path]));
    setControl("");
    onOpen(path);
  };

  return (
    <div className="write">
      <nav className="file-rail" aria-label="Files you author">
        {groups.map((g) => (
          <div key={g}>
            <div className="eyebrow">{g}</div>
            {files.filter((f) => f.group === g).map((f) => (
              <button key={f.path} className="file" role="tab" aria-selected={f.path === current} title={f.path} onClick={() => onOpen(f.path)}>
                <span>{f.path.split("/").pop()}</span>
                {dirty.has(f.path) ? <span className="mark">edited</span> : !f.exists ? <span className="mark" data-new="">new</span> : null}
              </button>
            ))}
            {g === "Procedures" && lab.writable && (
              <form className="new-proc" onSubmit={(e) => { e.preventDefault(); if (controlOk) addProcedure(); }}>
                <input className="input" value={control} onChange={(e) => setControl(e.target.value)}
                  placeholder="control id" aria-label="Control id for a new procedure" />
                <button className="btn" type="submit" disabled={!controlOk}>Add</button>
                <span className="seg" role="group" aria-label="Procedure type">
                  <button type="button" aria-pressed={kind === "tod"} onClick={() => setKind("tod")}>ToD</button>
                  <button type="button" aria-pressed={kind === "toe"} onClick={() => setKind("toe")}>ToE</button>
                </span>
              </form>
            )}
          </div>
        ))}
      </nav>
      {current ? <Editor key={current} path={current} moduleId={moduleId} writable={lab.writable} />
        : <p className="empty pad">No files yet.</p>}
    </div>
  );
}

function Editor({ path, moduleId, writable }: { path: string; moduleId: number; writable: boolean }) {
  const draft = useDraft(path);
  const toast = useToast();
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const isFinding = /\/findings\/F-\d{2}-\d+\.md$/.test(path);

  const load = useCallback(async (force: boolean) => {
    try {
      const file = await get<FilePayload>(fileUrl(path));
      const cur = getDraft(path);
      if (cur?.dirty && !force) {
        // Keep the learner's text; just note that the disk moved underneath it.
        if (file.sha256 !== cur.base) patchDraft(path, { changedOnDisk: true });
        return;
      }
      setDraft(path, { text: file.content, base: file.sha256, exists: file.exists, dirty: false,
        rev: (cur?.rev ?? 0) + 1, changedOnDisk: false, conflict: null });
      setError(null);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "The backend did not answer.");
    }
  }, [path]);

  useEffect(() => { void load(false); }, [load]);
  useOnChange(["lab"], () => { void load(false); });

  const setText = (text: string) => patchDraft(path, { text, dirty: true });

  const save = async () => {
    const cur = getDraft(path);
    if (!cur) return;
    setSaving(true);
    try {
      const res = await send<{ sha256: string }>("PUT", "/api/authored", { path, content: cur.text, base_sha256: cur.base });
      patchDraft(path, { base: res.sha256, exists: true, dirty: false, changedOnDisk: false, conflict: null });
      setError(null);
      toast(`Saved ${path}`);
    } catch (e) {
      if (e instanceof ApiError && e.status === 409) {
        patchDraft(path, { conflict: { content: (e.body.disk_content as string | null) ?? null, sha: (e.body.disk_sha256 as string | null) ?? null } });
      } else {
        setError(e instanceof ApiError ? `Not saved: ${e.message}` : "Not saved: the backend did not answer.");
      }
    } finally {
      setSaving(false);
    }
  };

  if (!draft) return <div className="editor">{error ? <div className="pad"><ErrorNote>{error}</ErrorNote></div> : <Loading what={path} />}</div>;

  const finding = isFinding ? (draft.text.trim() === "" ? blankFinding(path, moduleId) : parseFinding(draft.text)) : null;
  const state = draft.dirty ? "unsaved changes" : draft.exists ? "matches file on disk" : "not on disk yet";

  return (
    <div className="editor">
      <div className="editor-head">
        <span className="editor-path" title={path}><bdi>{path}</bdi></span>
        <span className="save-state" data-dirty={draft.dirty} aria-live="polite">{state}</span>
        <button className="btn btn-primary" onClick={save} disabled={!writable || saving || !draft.dirty || draft.conflict !== null}>Save</button>
      </div>
      <div className="editor-body">
        {!writable && <div className="notice">This module is locked, so its files are read-only here.</div>}
        {error && <ErrorNote>{error}</ErrorNote>}
        {draft.conflict && (
          <ErrorNote>
            <strong>This file changed on disk since you loaded it. Nothing was written.</strong> Your text is still in the editor below.
            {draft.conflict.content === null ? <p>The file no longer exists on disk.</p> : <pre aria-label="Version on disk">{draft.conflict.content}</pre>}
            <div className="banner-actions">
              <button className="btn" onClick={() => void load(true)}>Discard mine, load the disk version</button>
              <button className="btn" onClick={() => patchDraft(path, { base: draft.conflict!.sha, conflict: null, changedOnDisk: false })}>
                Keep mine (Save will then replace the disk version)
              </button>
            </div>
          </ErrorNote>
        )}
        {draft.changedOnDisk && !draft.conflict && (
          <div className="notice" data-tone="warn">This file changed on disk while you were editing. Saving will be refused until you choose which version to keep.</div>
        )}
        {isFinding && finding
          ? <FindingForm key={draft.rev} initial={finding} readOnly={!writable} onChange={(f) => setText(composeFinding(f))} />
          : <>
            {isFinding && <div className="notice">This finding is not in the standard front-matter-plus-five-headings form, so it opens as plain text.</div>}
            <textarea className="textarea fill" value={draft.text} readOnly={!writable} spellCheck aria-label={path}
              placeholder="Your words only. Nothing here drafts, completes or suggests."
              onChange={(e) => setText(e.target.value)} />
          </>}
      </div>
    </div>
  );
}

function FindingForm({ initial, readOnly, onChange }: { initial: Finding; readOnly: boolean; onChange: (f: Finding) => void }) {
  const [f, setF] = useState(initial);
  const update = (patch: Partial<Finding>) => { const next = { ...f, ...patch }; setF(next); onChange(next); };
  return (
    <>
      <div className="field-row">
        <label className="field"><span className="eyebrow">control_id</span>
          <input className="input mono" value={f.control_id} readOnly={readOnly} onChange={(e) => update({ control_id: e.target.value })} /></label>
        <label className="field"><span className="eyebrow">status</span>
          <select className="input" value={f.status} disabled={readOnly} onChange={(e) => update({ status: e.target.value })}>
            {STATUSES.map((s) => <option key={s}>{s}</option>)}
          </select></label>
        <label className="field"><span className="eyebrow">title</span>
          <input className="input" value={f.title} readOnly={readOnly} placeholder="One line" onChange={(e) => update({ title: e.target.value })} /></label>
      </div>
      <label className="field"><span className="eyebrow">evidence (result record paths, comma-separated)</span>
        <input className="input mono" value={f.evidence} readOnly={readOnly} onChange={(e) => update({ evidence: e.target.value })} /></label>
      {SECTIONS.map((s) => (
        <label className="field cs" key={s}>
          <h5>{s}</h5>
          <textarea className="textarea" value={f.sections[s]} readOnly={readOnly} spellCheck
            onChange={(e) => update({ sections: { ...f.sections, [s]: e.target.value } })} />
        </label>
      ))}
    </>
  );
}
