import { Link } from "react-router-dom";
import { useDeferredValue, useMemo } from "react";
import { AlertTrendPanel } from "../components/AlertTrendPanel";
import { MetricBarChart } from "../components/MetricBarChart";
import { SectionCard } from "../components/SectionCard";
import { SparklinePanel } from "../components/SparklinePanel";
import { SourceHealthGrid } from "../components/SourceHealthGrid";
import { StatCard } from "../components/StatCard";
import { ThreatDonut } from "../components/ThreatDonut";
import { TopEntitiesPanel } from "../components/TopEntitiesPanel";
import { formatIncidentTime, SEVERITY_STYLES, SOURCE_STYLES, sourceSummary } from "../lib/ui";

export function OverviewPage({ siem }) {
  const deferredLogs = useDeferredValue(siem.recent_logs);
  const severitySegments = useMemo(
    () => [
      { label: "High", value: siem.alert_trend?.by_severity?.High || 0, color: "#ff6e7d" },
      { label: "Medium", value: siem.alert_trend?.by_severity?.Medium || 0, color: "#f3a941" },
      { label: "Low", value: siem.alert_trend?.by_severity?.Low || 0, color: "#4ad4a0" },
    ],
    [siem.alert_trend],
  );
  const sourceVolume = useMemo(
    () =>
      (siem.source_health || []).map((source) => ({
        label: source.source,
        value: source.recent_events,
        caption: source.status === "Healthy" ? `Last seen ${formatIncidentTime(source.last_seen)}` : "Awaiting fresh events",
        tone: source.status === "Healthy" ? "from-sky/80 via-cobalt/70 to-mint/70" : "from-amber/70 via-gold/60 to-rose/60",
      })),
    [siem.source_health],
  );
  const incidentStatus = useMemo(() => {
    const counts = (siem.incidents || []).reduce((acc, incident) => {
      const key = incident.Status || "Unknown";
      acc[key] = (acc[key] || 0) + 1;
      return acc;
    }, {});
    return Object.entries(counts).map(([label, value]) => ({
      label,
      value,
      tone: label === "Under Investigation" ? "from-gold/80 via-amber/70 to-rose/60" : "from-sky/80 via-cobalt/70 to-mint/70",
    }));
  }, [siem.incidents]);
  const mttdPoints = useMemo(
    () =>
      (siem.mttd?.records || []).slice(-8).map((record, index) => ({
        label: `R${index + 1}`,
        value: Number(record.mttd_seconds) || 0,
      })),
    [siem.mttd],
  );
  const logMomentum = useMemo(
    () =>
      (siem.recent_logs || []).slice(0, 10).map((log, index) => ({
        label: log._table || `Signal ${index + 1}`,
        value: Math.max(10 - index, 1),
      })),
    [siem.recent_logs],
  );

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

      <SectionCard title="Security Command Center" subtitle="Professional SIEM analytics focused on severity pressure, connector throughput, response status, and detection performance.">
        <div className="grid gap-5 xl:grid-cols-[1.02fr_0.98fr]">
          <ThreatDonut
            title="Threat Distribution"
            subtitle="Current incident severity mix across the monitoring session."
            segments={severitySegments}
            totalLabel="Incident total"
          />
          <div className="grid gap-5">
            <MetricBarChart
              title="Connector Ingestion Volume"
              subtitle="Recent event volume by telemetry source."
              items={sourceVolume}
              valueFormatter={(value) => `${value} evts`}
              emptyLabel="No source traffic yet."
            />
            <div className="grid gap-5 lg:grid-cols-2">
              <MetricBarChart
                title="Incident Pipeline"
                subtitle="How many cases are sitting in each operational state."
                items={incidentStatus}
                valueFormatter={(value) => `${value}`}
                emptyLabel="No incident states available yet."
              />
              <SparklinePanel
                title="MTTD Performance"
                subtitle="Recent detection latency trend from attack trigger to alert."
                points={mttdPoints}
                tone="#4ad4a0"
                valueSuffix="s"
              />
            </div>
          </div>
        </div>
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

      <SectionCard title="Telemetry Momentum" subtitle="Quick pulse on the freshest cross-source signal flow reaching the analyst console.">
        <div className="grid gap-5 xl:grid-cols-[0.9fr_1.1fr]">
          <MetricBarChart
            title="Recent Signal Priority"
            subtitle="A visual ordering of the latest telemetry reaching the console feed."
            items={logMomentum}
            valueFormatter={(value) => `P${value}`}
            emptyLabel="No recent log activity detected."
          />
          <div className="rounded-[28px] border border-white/8 bg-slate-950/45 p-5">
            <p className="text-[10px] uppercase tracking-[0.28em] text-steel">Analyst Notes</p>
            <div className="mt-5 grid gap-4 md:grid-cols-3">
              <div className="rounded-2xl border border-rose/20 bg-rose/10 p-4">
                <p className="text-xs uppercase tracking-[0.22em] text-rose">Exposure</p>
                <p className="mt-3 text-3xl font-semibold text-white">{siem.stats.high_severity}</p>
                <p className="mt-2 text-sm text-slate-300">High severity cases requiring immediate validation.</p>
              </div>
              <div className="rounded-2xl border border-sky/20 bg-sky/10 p-4">
                <p className="text-xs uppercase tracking-[0.22em] text-sky">Detection Depth</p>
                <p className="mt-3 text-3xl font-semibold text-white">{siem.stats.total_alerts}</p>
                <p className="mt-2 text-sm text-slate-300">Alerts created by the active detection catalog.</p>
              </div>
              <div className="rounded-2xl border border-mint/20 bg-mint/10 p-4">
                <p className="text-xs uppercase tracking-[0.22em] text-mint">Connector Reach</p>
                <p className="mt-3 text-3xl font-semibold text-white">{siem.stats.sources_active}</p>
                <p className="mt-2 text-sm text-slate-300">Sources currently contributing to the workspace.</p>
              </div>
            </div>
          </div>
        </div>
      </SectionCard>

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
