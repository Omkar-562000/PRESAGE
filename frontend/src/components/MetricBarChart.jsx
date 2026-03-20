function defaultValueFormatter(value) {
  return `${value}`;
}

export function MetricBarChart({
  title,
  subtitle,
  items,
  valueFormatter = defaultValueFormatter,
  emptyLabel = "No data available.",
}) {
  const maxValue = Math.max(...items.map((item) => item.value), 1);

  return (
    <div className="rounded-[28px] border border-white/8 bg-slate-950/45 p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-[10px] uppercase tracking-[0.28em] text-steel">{title}</p>
          {subtitle ? <p className="mt-2 text-sm leading-6 text-slate-400">{subtitle}</p> : null}
        </div>
      </div>

      <div className="mt-5 space-y-4">
        {items.length === 0 ? (
          <p className="text-sm text-slate-400">{emptyLabel}</p>
        ) : (
          items.map((item) => {
            const width = Math.max((item.value / maxValue) * 100, item.value > 0 ? 8 : 0);
            return (
              <div key={item.label} className="space-y-2">
                <div className="flex items-center justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium text-white">{item.label}</p>
                    {item.caption ? <p className="text-xs text-steel">{item.caption}</p> : null}
                  </div>
                  <p className="shrink-0 text-sm font-semibold text-white">{valueFormatter(item.value)}</p>
                </div>
                <div className="h-3 overflow-hidden rounded-full bg-white/5">
                  <div
                    className={`h-full rounded-full bg-gradient-to-r ${item.tone || "from-sky/80 via-cobalt/70 to-mint/70"}`}
                    style={{ width: `${width}%` }}
                  />
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
