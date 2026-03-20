import { useMemo } from "react";
import { getReportJsonUrl, getReportPdfUrl } from "../lib/api";
import { SectionCard } from "../components/SectionCard";
import { SEVERITY_STYLES, SOURCE_STYLES, formatIncidentTime, sourceSummary } from "../lib/ui";

export function ReportsPage({ siem }) {
  const reportPdfUrl = getReportPdfUrl();
  const reportJsonUrl = getReportJsonUrl();

  const tableSummary = useMemo(
    () =>
      Object.entries(siem.logs_by_table || {}).map(([table, entries]) => ({
        table,
        count: entries.length,
        latest: entries[0]?.TimeGenerated || null,
      })),
    [siem.logs_by_table],
  );

  return (
    <div className="space-y-6">
      <SectionCard
        title="Report Center"
        subtitle="A clean moderator-ready report summary with export actions and the latest operational evidence."
        actions={
          <div className="flex flex-wrap gap-3">
            <a
              href={reportPdfUrl}
              className="rounded-full border border-gold/25 bg-gradient-to-r from-gold/20 to-amber/15 px-5 py-3 text-xs font-semibold uppercase tracking-[0.22em] text-white transition hover:border-gold/40 hover:bg-gold/20"
            >
              Download PDF
            </a>
            <a
              href={reportJsonUrl}
              target="_blank"
              rel="noreferrer"
              className="rounded-full border border-white/10 bg-white/5 px-5 py-3 text-xs font-semibold uppercase tracking-[0.22em] text-white transition hover:border-sky/30 hover:bg-sky/10"
            >
              Open JSON
            </a>
          </div>
        }
      >
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <div className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
            <p className="text-xs uppercase tracking-[0.22em] text-steel">Generated</p>
            <p className="mt-3 text-lg font-semibold text-white">{siem.generated_at ? new Date(siem.generated_at).toLocaleString("en-IN") : "--"}</p>
          </div>
          <div className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
            <p className="text-xs uppercase tracking-[0.22em] text-steel">Incidents</p>
            <p className="mt-3 text-3xl font-semibold text-white">{siem.stats.total_incidents}</p>
          </div>
          <div className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
            <p className="text-xs uppercase tracking-[0.22em] text-steel">Logs Captured</p>
            <p className="mt-3 text-3xl font-semibold text-white">{siem.stats.total_logs}</p>
          </div>
          <div className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
            <p className="text-xs uppercase tracking-[0.22em] text-steel">Average MTTD</p>
            <p className="mt-3 text-3xl font-semibold text-white">{siem.mttd?.average ? `${siem.mttd.average}s` : "--"}</p>
          </div>
        </div>
      </SectionCard>

      <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
        <SectionCard title="Incident Summary" subtitle="Structured case list for presentation and moderation review.">
          <div className="space-y-4">
            {siem.incidents.length === 0 ? <p className="text-sm text-steel">No incidents recorded yet.</p> : null}
            {siem.incidents.map((incident) => (
              <article key={`${incident.IncidentNumber}-${incident.CreatedTime}`} className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
                <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                  <div>
                    <p className="text-xs uppercase tracking-[0.22em] text-steel">Incident #{incident.IncidentNumber} • {formatIncidentTime(incident.CreatedTime)}</p>
                    <h3 className="mt-2 text-xl font-semibold text-white">{incident.Title}</h3>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <span className={`rounded-full px-3 py-1 text-xs font-semibold ${SEVERITY_STYLES[incident.Severity] || SEVERITY_STYLES.Low}`}>{incident.Severity}</span>
                    <span className="rounded-full border border-sky/20 bg-sky/10 px-3 py-1 text-xs text-sky">{incident.Status}</span>
                  </div>
                </div>
                <div className="mt-4 grid gap-3 md:grid-cols-3">
                  <div className="rounded-xl border border-white/8 bg-white/5 p-3">
                    <p className="text-[10px] uppercase tracking-[0.22em] text-steel">Entity</p>
                    <p className="mt-2 text-sm text-white">{incident.AffectedEntity || "N/A"}</p>
                  </div>
                  <div className="rounded-xl border border-white/8 bg-white/5 p-3">
                    <p className="text-[10px] uppercase tracking-[0.22em] text-steel">Source</p>
                    <p className="mt-2 text-sm text-white">{incident.SourceTable}</p>
                  </div>
                  <div className="rounded-xl border border-white/8 bg-white/5 p-3">
                    <p className="text-[10px] uppercase tracking-[0.22em] text-steel">MTTD</p>
                    <p className="mt-2 text-sm text-white">{incident.MTTD_seconds ? `${incident.MTTD_seconds}s` : "Pending"}</p>
                  </div>
                </div>
                <p className="mt-4 text-sm leading-7 text-slate-300">{incident.Evidence}</p>
              </article>
            ))}
          </div>
        </SectionCard>

        <div className="space-y-6">
          <SectionCard title="Log Table Summary" subtitle="Recent ingestion coverage by source for the generated report.">
            <div className="space-y-3">
              {tableSummary.map((item) => (
                <div key={item.table} className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <span className={`rounded-full px-3 py-1 text-xs font-semibold ${SOURCE_STYLES[item.table] || "bg-white/10 text-white"}`}>{item.table}</span>
                    <span className="text-sm font-semibold text-white">{item.count}</span>
                  </div>
                  <p className="mt-3 text-xs uppercase tracking-[0.22em] text-steel">Latest Record</p>
                  <p className="mt-2 text-sm text-slate-300">{item.latest ? new Date(item.latest).toLocaleString("en-IN") : "No recent record"}</p>
                </div>
              ))}
            </div>
          </SectionCard>

          <SectionCard title="Recent Evidence Feed" subtitle="A clean evidence strip you can show instead of raw JSON objects.">
            <div className="space-y-3">
              {(siem.recent_logs || []).slice(0, 8).map((log, index) => (
                <div key={`${log.TimeGenerated}-${index}`} className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <span className={`rounded-full px-3 py-1 text-xs font-semibold ${SOURCE_STYLES[log._table] || "bg-white/10 text-white"}`}>{log._table}</span>
                    <span className="text-xs uppercase tracking-[0.22em] text-steel">{formatIncidentTime(log.TimeGenerated)}</span>
                  </div>
                  <p className="mt-3 text-sm text-white">{sourceSummary(log)}</p>
                  <p className="mt-2 text-xs text-slate-400">{log.TimeGenerated}</p>
                </div>
              ))}
            </div>
          </SectionCard>
        </div>
      </div>
    </div>
  );
}
