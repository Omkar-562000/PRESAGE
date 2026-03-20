import { useMemo, useState } from "react";
import { MetricBarChart } from "../components/MetricBarChart";
import { SectionCard } from "../components/SectionCard";
import { SourceHealthGrid } from "../components/SourceHealthGrid";
import { SparklinePanel } from "../components/SparklinePanel";
import { ThreatDonut } from "../components/ThreatDonut";
import { formatIncidentTime, SOURCE_STYLES, sourceSummary } from "../lib/ui";

const TABLES = ["SigninLogs", "SecurityEvent", "WindowsEvent", "AzureActivity", "NetworkEvents"];

export function TelemetryPage({ siem }) {
  const [selectedSource, setSelectedSource] = useState("All");

  const filteredTimeline = useMemo(() => {
    if (selectedSource === "All") {
      return siem.recent_logs || [];
    }
    return (siem.recent_logs || []).filter((log) => log._table === selectedSource);
  }, [selectedSource, siem.recent_logs]);

  const sourceVolume = useMemo(
    () =>
      TABLES.map((table) => ({
        label: table,
        value: siem.logs_by_table?.[table]?.length || 0,
        caption: `${table} recent records`,
      })),
    [siem.logs_by_table],
  );

  const sourceHeartbeat = useMemo(
    () =>
      (siem.source_health || []).map((source, index) => ({
        label: `S${index + 1}`,
        value: source.recent_events,
      })),
    [siem.source_health],
  );

  const telemetrySegments = useMemo(
    () =>
      TABLES.map((table, index) => ({
        label: table,
        value: siem.logs_by_table?.[table]?.length || 0,
        color: ["#73c7ff", "#f3a941", "#22d3ee", "#e879f9", "#4ad4a0"][index],
      })),
    [siem.logs_by_table],
  );

  return (
    <div className="space-y-6">
      <SectionCard title="Source Health" subtitle="Quick source monitoring, heartbeat, and recent log volume.">
        <SourceHealthGrid sources={siem.source_health || []} />
      </SectionCard>

      <SectionCard title="Telemetry Analytics" subtitle="Visual SIEM telemetry diagnostics for connector share, event volume, and source heartbeat.">
        <div className="grid gap-5 xl:grid-cols-[0.95fr_1.05fr]">
          <ThreatDonut
            title="Connector Share"
            subtitle="Distribution of the currently retained event feed across all log sources."
            segments={telemetrySegments}
            totalLabel="Recent logs"
          />
          <div className="grid gap-5">
            <MetricBarChart
              title="Source Event Volume"
              subtitle="Relative activity level by telemetry source in the current polling window."
              items={sourceVolume}
              valueFormatter={(value) => `${value} evts`}
            />
            <SparklinePanel
              title="Heartbeat Trace"
              subtitle="Source-by-source event pulse across the current telemetry snapshot."
              points={sourceHeartbeat}
              tone="#73c7ff"
            />
          </div>
        </div>
      </SectionCard>

      <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <SectionCard title="Telemetry Sources" subtitle="Connector-specific log feeds with recent events per source.">
          <div className="space-y-4">
            {TABLES.map((table) => {
              const entries = siem.logs_by_table?.[table] || [];
              return (
                <div key={table} className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
                  <div className="flex items-center justify-between">
                    <span className={`rounded-full px-3 py-1 text-xs font-semibold ${SOURCE_STYLES[table] || "bg-white/10 text-white"}`}>
                      {table}
                    </span>
                    <span className="text-xs text-steel">{entries.length} recent events</span>
                  </div>
                  <div className="mt-4 space-y-3">
                    {entries.length === 0 ? <p className="text-sm text-steel">No recent events.</p> : null}
                    {entries.slice(0, 5).map((entry, index) => (
                      <div key={`${table}-${index}`} className="rounded-xl border border-white/8 bg-white/5 p-3">
                        <p className="text-sm text-white">{sourceSummary({ ...entry, _table: table })}</p>
                        <p className="mt-1 text-xs text-steel">{entry.TimeGenerated}</p>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </SectionCard>

        <SectionCard
          title="Merged Telemetry Timeline"
          subtitle="A cross-source operational timeline for the SOC view."
          actions={
            <select
              value={selectedSource}
              onChange={(event) => setSelectedSource(event.target.value)}
              className="rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-sm text-white outline-none focus:border-sky/40"
            >
              <option value="All">All sources</option>
              {TABLES.map((table) => (
                <option key={table} value={table}>{table}</option>
              ))}
            </select>
          }
        >
          <div className="space-y-3">
            {filteredTimeline.length === 0 ? (
              <p className="text-sm text-steel">No recent logs available for the selected source.</p>
            ) : (
              filteredTimeline.map((log, index) => (
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
      </div>
    </div>
  );
}
