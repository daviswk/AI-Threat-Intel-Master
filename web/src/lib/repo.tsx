import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import { AnimatePresence, motion } from "motion/react";
import { ApiError, get } from "../api/client";

/* ------------------------------------------------------------------ change bus
   The backend's file watcher sends topics over server-sent events. Each
   resource names the topics it depends on and refetches when one arrives.
   If the event stream is down, a slow poll refreshes everything instead. */

export type Topic = "state" | "heuristics" | "flashcards" | "portfolio" | "lab" | "results" | "harness" | "curriculum" | "literature";
const ALL: Topic[] = ["state", "heuristics", "flashcards", "portfolio", "lab", "results", "harness", "curriculum", "literature"];
export type LiveMode = "live" | "polling" | "offline";
type Listener = (topics: Topic[]) => void;

interface Bus { subscribe: (fn: Listener) => () => void; emit: (topics: Topic[]) => void; refreshAll: () => void }
const BusContext = createContext<Bus | null>(null);
const LiveContext = createContext<LiveMode>("live");

export function RepoProvider({ children }: { children: ReactNode }) {
  const listeners = useRef(new Set<Listener>());
  const [mode, setMode] = useState<LiveMode>("live");

  const bus = useMemo<Bus>(() => {
    const emit = (topics: Topic[]) => listeners.current.forEach((fn) => fn(topics));
    return {
      subscribe: (fn) => { listeners.current.add(fn); return () => { listeners.current.delete(fn); }; },
      emit,
      refreshAll: () => emit(ALL),
    };
  }, []);

  useEffect(() => {
    const source = new EventSource("/api/events");
    let poll: number | undefined;
    let wasDown = false;
    const stopPoll = () => { if (poll !== undefined) { window.clearInterval(poll); poll = undefined; } };
    source.addEventListener("open", () => {
      stopPoll();
      setMode("live");
      if (wasDown) bus.refreshAll();
      wasDown = false;
    });
    source.addEventListener("change", (e) => {
      try { bus.emit(JSON.parse((e as MessageEvent<string>).data) as Topic[]); } catch { bus.refreshAll(); }
    });
    source.addEventListener("error", () => {
      wasDown = true;
      if (poll === undefined) {
        // Polling fallback: ask for everything every 5 s until the stream is back.
        poll = window.setInterval(async () => {
          try { await get("/api/session"); setMode("polling"); bus.refreshAll(); } catch { setMode("offline"); }
        }, 5000);
      }
    });
    return () => { stopPoll(); source.close(); };
  }, [bus]);

  return <BusContext.Provider value={bus}><LiveContext.Provider value={mode}>{children}</LiveContext.Provider></BusContext.Provider>;
}

export function useBus(): Bus {
  const bus = useContext(BusContext);
  if (!bus) throw new Error("RepoProvider is missing");
  return bus;
}
export const useLiveMode = () => useContext(LiveContext);

/** Call `fn` whenever one of `topics` changes in the repo. */
export function useOnChange(topics: Topic[], fn: () => void) {
  const bus = useBus();
  const saved = useRef(fn);
  saved.current = fn;
  const key = topics.join(",");
  useEffect(() => bus.subscribe((changed) => {
    if (changed.some((t) => key.split(",").includes(t))) saved.current();
  }), [bus, key]);
}

export interface Resource<T> { data: T | null; error: string | null; loading: boolean; reload: () => void }

/** Fetch JSON, and fetch it again when the repo changes under it. */
export function useResource<T>(url: string | null, topics: Topic[]): Resource<T> {
  const [state, setState] = useState<{ url: string | null; data: T | null; error: string | null; loading: boolean }>(
    { url, data: null, error: null, loading: url !== null });
  const seq = useRef(0);

  const load = useCallback(() => {
    if (url === null) { setState({ url, data: null, error: null, loading: false }); return; }
    const mine = ++seq.current;
    get<T>(url).then(
      (data) => { if (mine === seq.current) setState({ url, data, error: null, loading: false }); },
      (e: unknown) => {
        if (mine !== seq.current) return;
        const msg = e instanceof ApiError ? e.message : "The backend did not answer.";
        setState((s) => ({ url, data: s.url === url ? s.data : null, error: msg, loading: false }));
      });
  }, [url]);

  useEffect(() => {
    setState((s) => (s.url === url ? s : { url, data: null, error: null, loading: url !== null }));
    load();
  }, [url, load]);
  useOnChange(topics, load);

  return { data: state.url === url ? state.data : null, error: state.error, loading: state.loading, reload: load };
}

/* ---------------------------------------------------------------------- toasts */
const ToastContext = createContext<(msg: string) => void>(() => {});
export const useToast = () => useContext(ToastContext);

export function ToastProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<{ id: number; msg: string }[]>([]);
  const next = useRef(0);
  const push = useCallback((msg: string) => {
    const id = ++next.current;
    setItems((list) => [...list.slice(-2), { id, msg }]);
    window.setTimeout(() => setItems((list) => list.filter((t) => t.id !== id)), 3600);
  }, []);
  return (
    <ToastContext.Provider value={push}>
      {children}
      <div className="toasts" role="status" aria-live="polite">
        <AnimatePresence>
          {items.map((t) => (
            <motion.div key={t.id} className="toast" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 4 }}>{t.msg}</motion.div>
          ))}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
}
