export function TopEntitiesPanel({ entities }) {
  const maxIncidents = Math.max(...entities.map((item) => item.incidents), 1);

  return (
    <div className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
      <p className="text-xs uppercase tracking-[0.22em] text-steel">Top Affected Entities</p>
      <p className="mt-2 text-sm text-slate-400">Most frequently impacted users or hosts in the current monitoring session.</p>
      <div className="mt-4 space-y-3">
        {entities.length === 0 ? (
          <p className="text-sm text-slate-400">No entities to rank yet.</p>
        ) : (
          entities.map((item) => (
            <div key={item.entity} className="rounded-xl border border-white/8 bg-white/5 px-4 py-3">
              <div className="flex items-center justify-between gap-3">
                <span className="truncate pr-3 text-sm text-white">{item.entity}</span>
                <span className="text-sm font-semibold text-mint">{item.incidents}</span>
              </div>
              <div className="mt-3 h-2 overflow-hidden rounded-full bg-white/5">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-mint/80 via-sky/70 to-cobalt/70"
                  style={{ width: `${(item.incidents / maxIncidents) * 100}%` }}
                />
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
