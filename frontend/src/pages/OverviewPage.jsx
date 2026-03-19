import { Link } from "react-router-dom";
import { useDeferredValue } from "react";
import { AlertTrendPanel } from "../components/AlertTrendPanel";
import { SectionCard } from "../components/SectionCard";
import { SourceHealthGrid } from "../components/SourceHealthGrid";
import { StatCard } from "../components/StatCard";
import { TopEntitiesPanel } from "../components/TopEntitiesPanel";
import { formatIncidentTime, SEVERITY_STYLES, SOURCE_STYLES, sourceSummary } from "../lib/ui";

export function OverviewPage({ siem }) {
  const deferredLogs = useDeferredValue(siem.recent_logs);

  return (
    <>
      <section className="grid gap-5 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="overflow-hidden rounded-[30px] border border-white/8 bg-gradient-to-br from-slate-950/75 via-panel/80 to-shell/80 p-6 shadow-panel">
          <p className="text-[11px] uppercase tracking-[0.34em] text-gold">Analyst Briefing</p>
          <h2 className="mt-4 max-w-2xl font-display text-4xl leading-tight text-white">Security posture, live connectors, and incident momentum in one glance.</h2>
          <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-300">
            Presage is built to tell a complete operational story: what signals are active, which risks are emerging, and how quickly the platform is converting suspicious behavior into structured investigation.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <div className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.22em] text-mist">
              {siem.stats.total_incidents} incidents in session
            </div>
            <div className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.22em] text-mist">
              {siem.stats.sources_active} active sources
            </div>
            <div className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.22em] text-mist">
              Avg MTTD {siem.mttd?.average ? `${siem.mttd.average}s` : "--"}
            </div>
          </div>
        </div>
        <div className="grid gap-4">
          <div className="rounded-[28px] border border-mint/20 bg-gradient-to-br from-mint/12 to-white/5 p-5 shadow-panel">
            <p className="text-[11px] uppercase tracking-[0.3em] text-mint">Defense State</p>
            <p className="mt-3 text-3xl font-semibold text-white">{siem.stats.high_severity}</p>
            <p className="mt-2 text-sm leading-6 text-slate-300">High-priority incidents currently demanding analyst attention.</p>
          </div>
          <div className="rounded-[28px] border border-gold/20 bg-gradient-to-br from-gold/12 to-white/5 p-5 shadow-panel">
            <p className="text-[11px] uppercase tracking-[0.3em] text-gold">Operator Prompt</p>
            <p className="mt-3 text-sm leading-7 text-slate-200">Use the command dock above to move between mission views, then trigger one scenario from Attack Center to prove live detection and response.</p>
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <StatCard label="Logs Ingested" value={siem.stats.total_logs} accent="text-sky" hint="Telemetry ingested across all active sources." />
        <StatCard label="Alerts Fired" value={siem.stats.total_alerts} accent="text-amber" hint="Detection rules that have produced alerts." />
        <StatCard label="Incidents" value={siem.stats.total_incidents} accent="text-rose" hint="Incidents opened by the alert manager." />
        <StatCard label="High Severity" value={siem.stats.high_severity} accent="text-rose" hint="Priority items requiring analyst attention." />
        <StatCard label="Sources Active" value={siem.stats.sources_active} accent="text-mint" hint="Simulated connectors currently sending logs." />
      </section>

      <SectionCard title="Source Health" subtitle="Connector heartbeat and ingestion status similar to a SIEM source overview.">
        <SourceHealthGrid sources={siem.source_health || []} />
      </SectionCard>

      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <SectionCard
          title="Latest Incidents"
          subtitle="Newest incidents first with severity, evidence, and response context."
          actions={<Link to="/workspace/incidents" className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.22em] text-white transition hover:border-sky/30 hover:bg-sky/10">Open full queue</Link>}
        >
          <div className="space-y-4">
            {siem.loading ? <p className="text-sm text-steel">Loading incidents...</p> : null}
            {!siem.loading && siem.incidents.length === 0 ? <p className="text-sm text-steel">No incidents yet. Use the Attack Lab to generate activity.</p> : null}
            {siem.incidents.slice(0, 4).map((incident) => (
              <article key={`${incident.IncidentNumber}-${incident.CreatedTime}`} className="rounded-[24px] border border-white/8 bg-slate-950/45 p-5">
                <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                  <div>
                    <p className="text-xs uppercase tracking-[0.28em] text-steel">
                      Incident #{incident.IncidentNumber} at {formatIncidentTime(incident.CreatedTime)}
                    </p>
                    <h3 className="mt-2 font-display text-2xl text-white">{incident.Title}</h3>
                  </div>
                  <span className={`rounded-full px-3 py-1 text-xs font-semibold ${SEVERITY_STYLES[incident.Severity] || SEVERITY_STYLES.Low}`}>
                    {incident.Severity}
                  </span>
                </div>
                <p className="mt-4 text-sm leading-7 text-slate-300">{incident.Evidence}</p>
              </article>
            ))}
          </div>
        </SectionCard>

        <SectionCard title="Alert Trend" subtitle="Severity mix and recent alert density for the monitoring story.">
          <div className="space-y-4">
            <AlertTrendPanel trend={siem.alert_trend} />
            <TopEntitiesPanel entities={siem.top_entities || []} />
          </div>
        </SectionCard>
      </div>

      <SectionCard
        title="Live Log Stream"
        subtitle="Recent telemetry merged across all active sources."
        actions={<Link to="/workspace/telemetry" className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.22em] text-white transition hover:border-sky/30 hover:bg-sky/10">Open telemetry page</Link>}
      >
        <div className="grid gap-3">
          {deferredLogs.length === 0 ? (
            <p className="text-sm text-steel">Waiting for logs. Background traffic starts automatically when the backend comes online.</p>
          ) : (
            deferredLogs.slice(0, 10).map((log, index) => (
              <div key={`${log.TimeGenerated}-${index}`} className="flex flex-col gap-3 rounded-2xl border border-white/8 bg-slate-950/45 p-4 md:flex-row md:items-center md:justify-between">
                <div className="flex min-w-0 items-center gap-3">
                  <span className={`rounded-full px-3 py-1 text-xs font-semibold ${SOURCE_STYLES[log._table] || "bg-white/10 text-white"}`}>
                    {log._table}
                  </span>
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium text-white">{sourceSummary(log)}</p>
                    <p className="mt-1 text-xs text-steel">{log.TimeGenerated}</p>
                  </div>
                </div>
                <p className="text-xs uppercase tracking-[0.22em] text-slate-500">{formatIncidentTime(log.TimeGenerated)}</p>
              </div>
            ))
          )}
        </div>
      </SectionCard>
    </>
  );
}
