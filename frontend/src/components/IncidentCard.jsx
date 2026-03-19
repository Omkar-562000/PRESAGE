import { formatIncidentTime, SEVERITY_STYLES } from "../lib/ui";

export function IncidentCard({ incident }) {
  return (
    <article className="overflow-hidden rounded-[28px] border border-white/8 bg-gradient-to-br from-slate-950/70 via-panel/85 to-slate-950/55 p-5 shadow-panel">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div className="min-w-0">
          <p className="text-xs uppercase tracking-[0.28em] text-steel">
            Incident #{incident.IncidentNumber} opened at {formatIncidentTime(incident.CreatedTime)}
          </p>
          <h2 className="mt-3 font-display text-[2rem] leading-tight text-white">{incident.Title}</h2>
          <p className="mt-4 max-w-3xl text-sm leading-7 text-slate-300">{incident.Evidence}</p>
        </div>
        <div className="flex flex-wrap gap-2 lg:max-w-sm lg:justify-end">
          <span className={`rounded-full px-3 py-1 text-xs font-semibold ${SEVERITY_STYLES[incident.Severity] || SEVERITY_STYLES.Low}`}>
            {incident.Severity}
          </span>
          <span className="rounded-full border border-sky/20 bg-sky/10 px-3 py-1 text-xs text-sky">{incident.Status}</span>
          <span className="rounded-full border border-mint/20 bg-mint/10 px-3 py-1 text-xs text-mint">
            MTTD: {incident.MTTD_seconds ? `${incident.MTTD_seconds}s` : "Pending"}
          </span>
        </div>
      </div>

      <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <div className="rounded-2xl border border-white/8 bg-white/5 p-4 backdrop-blur">
          <p className="text-xs uppercase tracking-[0.22em] text-steel">Entity</p>
          <p className="mt-2 text-sm text-white">{incident.AffectedEntity || "N/A"}</p>
        </div>
        <div className="rounded-2xl border border-white/8 bg-white/5 p-4 backdrop-blur">
          <p className="text-xs uppercase tracking-[0.22em] text-steel">MITRE</p>
          <p className="mt-2 text-sm text-white">{incident.MITRETactic}</p>
        </div>
        <div className="rounded-2xl border border-white/8 bg-white/5 p-4 backdrop-blur">
          <p className="text-xs uppercase tracking-[0.22em] text-steel">Source Table</p>
          <p className="mt-2 text-sm text-white">{incident.SourceTable}</p>
        </div>
        <div className="rounded-2xl border border-white/8 bg-white/5 p-4 backdrop-blur">
          <p className="text-xs uppercase tracking-[0.22em] text-steel">Automation</p>
          <p className="mt-2 text-sm text-white">{incident.PlaybookTriggered ? "Triggered" : "Not triggered"}</p>
        </div>
      </div>

      <div className="mt-5 rounded-2xl border border-white/8 bg-slate-950/55 p-4">
        <p className="text-xs uppercase tracking-[0.22em] text-steel">Recommended Action</p>
        <p className="mt-2 text-sm leading-6 text-slate-300">{incident.RecommendedAction}</p>
      </div>
    </article>
  );
}
