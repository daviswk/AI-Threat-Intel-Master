import { memo, useRef, type KeyboardEvent, type ReactNode } from "react";
import { motion } from "motion/react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeSanitize from "rehype-sanitize";
import { Copy } from "lucide-react";
import { useToast } from "../lib/repo";

/** Status mark. Shape and colour both carry the state; pair it with a word. */
export function Glyph({ s }: { s: string }) {
  return <i className="glyph" data-s={s} aria-hidden="true" />;
}

export interface TabDef<T extends string> { id: T; label: string; now?: boolean }

/** Tab list with arrow-key navigation. The underline slides between tabs. */
export function Tabs<T extends string>({ name, tabs, value, onChange, label }: {
  name: string; tabs: TabDef<T>[]; value: T; onChange: (id: T) => void; label: string;
}) {
  const refs = useRef<Record<string, HTMLButtonElement | null>>({});
  const onKey = (e: KeyboardEvent) => {
    const i = tabs.findIndex((t) => t.id === value);
    const to = e.key === "ArrowRight" ? (i + 1) % tabs.length
      : e.key === "ArrowLeft" ? (i - 1 + tabs.length) % tabs.length
      : e.key === "Home" ? 0 : e.key === "End" ? tabs.length - 1 : -1;
    if (to < 0) return;
    e.preventDefault();
    onChange(tabs[to].id);
    refs.current[tabs[to].id]?.focus();
  };
  return (
    <div className="tabs" role="tablist" aria-label={label} onKeyDown={onKey}>
      {tabs.map((t) => (
        <button key={t.id} ref={(el) => { refs.current[t.id] = el; }} role="tab" className="tab"
          id={`${name}-tab-${t.id}`} aria-controls={`${name}-panel`} aria-selected={t.id === value}
          tabIndex={t.id === value ? 0 : -1} onClick={() => onChange(t.id)}>
          {t.label}{t.now && <span className="now">now</span>}
          {t.id === value && <motion.span layoutId={`${name}-underline`} className="tab-underline" transition={{ duration: 0.24 }} />}
        </button>
      ))}
    </div>
  );
}

/** Copies a fixed prompt for Claude Code. The text comes from the backend's templates. */
export function CopyPrompt({ label, text }: { label: string; text: string }) {
  const toast = useToast();
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      toast(`Copied. Paste into Claude Code: ${text}`);
    } catch {
      toast(`Copy this into Claude Code: ${text}`);
    }
  };
  return <button className="btn" onClick={copy} title={text}><Copy aria-hidden="true" />Copy CLI prompt: {label}</button>;
}

/** Markdown from the repo. Papers in /literature are converted from outside
 *  sources, so: raw HTML is dropped, the tree is sanitized, images are never
 *  fetched, and links open in a new tab without a referrer. */
export const Markdown = memo(function Markdown({ source }: { source: string }) {
  return (
    <div className="md">
      <ReactMarkdown skipHtml remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeSanitize]}
        components={{
          a: ({ href, children }) => <a href={href} target="_blank" rel="noreferrer noopener">{children}</a>,
          img: ({ alt }) => <span className="md-img">[image not loaded: {alt || "no description"}]</span>,
        }}>
        {source}
      </ReactMarkdown>
    </div>
  );
});

export function Loading({ what }: { what: string }) {
  return <p className="empty pad">Loading {what}.</p>;
}

export function ErrorNote({ children }: { children: ReactNode }) {
  return <div className="notice" data-tone="warn" role="alert">{children}</div>;
}
