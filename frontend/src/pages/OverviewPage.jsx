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
          actions={<Link to="/workspace/incidents" className="text-sm text-sky hover:text-white">Open full queue</Link>}
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
                    <h3 className="mt-2 text-xl font-semibold text-white">{incident.Title}</h3>
                  </div>
                  <span className={`rounded-full px-3 py-1 text-xs font-semibold ${SEVERITY_STYLES[incident.Severity] || SEVERITY_STYLES.Low}`}>
                    {incident.Severity}
                  </span>
                </div>
                <p className="mt-4 text-sm leading-6 text-slate-300">{incident.Evidence}</p>
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
        actions={<Link to="/workspace/telemetry" className="text-sm text-sky hover:text-white">Open telemetry page</Link>}
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
