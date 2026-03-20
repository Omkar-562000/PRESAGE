export function AlertTrendPanel({ trend }) {
  const severity = trend?.by_severity || {};
  const windows = trend?.recent_windows || [];
  const maxWindowCount = Math.max(...windows.map((window) => window.count), 1);
  const totalAlerts = (severity.High || 0) + (severity.Medium || 0) + (severity.Low || 0);

  return (
    <div className="grid gap-4 lg:grid-cols-[0.82fr_1.18fr]">
      <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-1">
        {["High", "Medium", "Low"].map((level) => (
          <div key={level} className="rounded-2xl border border-white/8 bg-gradient-to-br from-slate-950/70 to-white/[0.03] p-4">
            <p className="text-xs uppercase tracking-[0.22em] text-steel">{level} Alerts</p>
            <p className="mt-3 text-3xl font-semibold text-white">{severity[level] || 0}</p>
            <div className="mt-4 h-2 overflow-hidden rounded-full bg-white/5">
              <div
                className={`h-full rounded-full ${
                  level === "High"
                    ? "bg-gradient-to-r from-rose/80 to-rose"
                    : level === "Medium"
                      ? "bg-gradient-to-r from-amber/80 to-amber"
                      : "bg-gradient-to-r from-mint/80 to-mint"
                }`}
                style={{
                  width: `${((severity[level] || 0) / Math.max(totalAlerts, 1)) * 100}%`,
                }}
              />
            </div>
          </div>
        ))}
      </div>
      <div className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-xs uppercase tracking-[0.22em] text-steel">Recent Incident Windows</p>
            <p className="mt-2 text-sm text-slate-400">Burst density across the latest incident creation windows.</p>
          </div>
          <div className="rounded-full border border-white/8 bg-white/5 px-3 py-2 text-xs uppercase tracking-[0.22em] text-white">
            Last {windows.length || 0} windows
          </div>
        </div>
        <div className="mt-5 space-y-3">
          {windows.length === 0 ? (
            <p className="text-sm text-slate-400">No incidents yet.</p>
          ) : (
            windows.map((window) => (
              <div key={window.window} className="rounded-xl border border-white/8 bg-white/5 px-4 py-3">
                <div className="flex items-center justify-between gap-3">
                  <span className="text-sm text-white">{window.window.replace("T", " ")}</span>
                  <span className="text-sm font-semibold text-sky">{window.count}</span>
                </div>
                <div className="mt-3 h-2 overflow-hidden rounded-full bg-white/5">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-sky/80 via-cobalt/70 to-mint/70"
                    style={{ width: `${(window.count / maxWindowCount) * 100}%` }}
                  />
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
