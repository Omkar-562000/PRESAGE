export function AlertTrendPanel({ trend }) {
  const severity = trend?.by_severity || {};
  const windows = trend?.recent_windows || [];

  return (
    <div className="grid gap-4 lg:grid-cols-[0.9fr_1.1fr]">
      <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-1">
        {["High", "Medium", "Low"].map((level) => (
          <div key={level} className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
            <p className="text-xs uppercase tracking-[0.22em] text-steel">{level} Alerts</p>
            <p className="mt-3 text-3xl font-semibold text-white">{severity[level] || 0}</p>
          </div>
        ))}
      </div>
      <div className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
        <p className="text-xs uppercase tracking-[0.22em] text-steel">Recent Incident Windows</p>
        <div className="mt-4 space-y-3">
          {windows.length === 0 ? (
            <p className="text-sm text-slate-400">No incidents yet.</p>
          ) : (
            windows.map((window) => (
              <div key={window.window} className="flex items-center justify-between rounded-xl border border-white/8 bg-white/5 px-4 py-3">
                <span className="text-sm text-white">{window.window.replace("T", " ")}</span>
                <span className="text-sm font-semibold text-sky">{window.count}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
