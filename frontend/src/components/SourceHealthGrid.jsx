import { formatIncidentTime, SOURCE_STYLES } from "../lib/ui";

export function SourceHealthGrid({ sources }) {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      {sources.map((source) => (
        <div key={source.source} className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
          <div className="flex items-center justify-between gap-3">
            <span className={`rounded-full px-3 py-1 text-xs font-semibold ${SOURCE_STYLES[source.source] || "bg-white/10 text-white"}`}>
              {source.source}
            </span>
            <span className={`text-xs ${source.status === "Healthy" ? "text-mint" : "text-amber"}`}>{source.status}</span>
          </div>
          <p className="mt-4 text-2xl font-semibold text-white">{source.recent_events}</p>
          <p className="mt-1 text-sm text-slate-400">Recent events</p>
          <p className="mt-4 text-xs uppercase tracking-[0.22em] text-steel">Last Seen</p>
          <p className="mt-1 text-sm text-white">{formatIncidentTime(source.last_seen)}</p>
        </div>
      ))}
    </div>
  );
}
