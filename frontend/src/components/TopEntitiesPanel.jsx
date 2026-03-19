export function TopEntitiesPanel({ entities }) {
  return (
    <div className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
      <p className="text-xs uppercase tracking-[0.22em] text-steel">Top Affected Entities</p>
      <div className="mt-4 space-y-3">
        {entities.length === 0 ? (
          <p className="text-sm text-slate-400">No entities to rank yet.</p>
        ) : (
          entities.map((item) => (
            <div key={item.entity} className="flex items-center justify-between rounded-xl border border-white/8 bg-white/5 px-4 py-3">
              <span className="truncate pr-3 text-sm text-white">{item.entity}</span>
              <span className="text-sm font-semibold text-mint">{item.incidents}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
