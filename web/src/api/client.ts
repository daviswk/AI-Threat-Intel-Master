import type { RunEvent, RunName } from "./types";

/** A refusal or failure from the backend. `reason` is the server's own wording. */
export class ApiError extends Error {
  status: number;
  body: Record<string, unknown>;
  constructor(status: number, body: Record<string, unknown>) {
    super(typeof body.reason === "string" ? body.reason : `request failed (${status})`);
    this.status = status;
    this.body = body;
  }
}

async function fail(res: Response): Promise<never> {
  let body: Record<string, unknown> = {};
  try { body = await res.json(); } catch { /* not JSON */ }
  throw new ApiError(res.status, body);
}

export async function get<T>(url: string, signal?: AbortSignal): Promise<T> {
  const res = await fetch(url, { signal, headers: { Accept: "application/json" } });
  if (!res.ok) return fail(res);
  return res.json() as Promise<T>;
}

// The per-launch token. Held in memory only; never put in browser storage.
let tokenPromise: Promise<string> | null = null;
function token(): Promise<string> {
  tokenPromise ??= get<{ token: string }>("/api/session").then((r) => r.token)
    .catch((e) => { tokenPromise = null; throw e; });
  return tokenPromise;
}

export async function send<T>(method: "PUT" | "POST", url: string, body: unknown): Promise<T> {
  const res = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json", "X-MC-Token": await token() },
    body: JSON.stringify(body),
  });
  if (!res.ok) return fail(res);
  return res.json() as Promise<T>;
}

export const fileUrl = (path: string) => `/api/file?path=${encodeURIComponent(path)}`;

/** Run one of the backend's fixed commands and deliver its output as it arrives. */
export async function run(name: RunName, onEvent: (e: RunEvent) => void): Promise<void> {
  const res = await fetch(`/api/run/${name}`, { method: "POST", headers: { "X-MC-Token": await token() } });
  if (!res.ok || !res.body) return fail(res);
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    let nl: number;
    while ((nl = buffer.indexOf("\n")) >= 0) {
      const line = buffer.slice(0, nl);
      buffer = buffer.slice(nl + 1);
      if (line.trim()) onEvent(JSON.parse(line) as RunEvent);
    }
  }
}
