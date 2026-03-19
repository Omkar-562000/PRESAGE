import { useMemo, useState } from "react";
import { SectionCard } from "../components/SectionCard";
import { SourceHealthGrid } from "../components/SourceHealthGrid";
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

  return (
    <div className="space-y-6">
      <SectionCard title="Source Health" subtitle="Quick source monitoring, heartbeat, and recent log volume.">
        <SourceHealthGrid sources={siem.source_health || []} />
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
