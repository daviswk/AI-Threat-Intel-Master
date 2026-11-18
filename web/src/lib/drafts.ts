import { useSyncExternalStore } from "react";

/** Unsaved editor text, held in memory for this page load only. It is not
 *  state about the repo: the file on disk stays the source of truth, and
 *  `base` is the hash of the version the text was loaded from. */
export interface Draft {
  text: string;
  base: string | null;       // sha256 of the file as loaded; null if it did not exist
  exists: boolean;
  dirty: boolean;
  rev: number;               // bumps when the text is replaced from disk
  changedOnDisk: boolean;
  conflict: { content: string | null; sha: string | null } | null;
}

const drafts = new Map<string, Draft>();
const listeners = new Set<() => void>();
let version = 0;

function notify() { version += 1; listeners.forEach((fn) => fn()); }
const subscribe = (fn: () => void) => { listeners.add(fn); return () => { listeners.delete(fn); }; };

export function getDraft(path: string): Draft | undefined { return drafts.get(path); }

export function setDraft(path: string, next: Draft) { drafts.set(path, next); notify(); }

export function patchDraft(path: string, patch: Partial<Draft>) {
  const cur = drafts.get(path);
  if (cur) { drafts.set(path, { ...cur, ...patch }); notify(); }
}

export function useDraft(path: string): Draft | undefined {
  useSyncExternalStore(subscribe, () => version);
  return drafts.get(path);
}

export function useDirtyPaths(): Set<string> {
  useSyncExternalStore(subscribe, () => version);
  return new Set([...drafts].filter(([, d]) => d.dirty).map(([p]) => p));
}

export function anyDirty(): boolean {
  return [...drafts.values()].some((d) => d.dirty);
}
