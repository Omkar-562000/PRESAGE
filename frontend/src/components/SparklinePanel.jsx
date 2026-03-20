export function SparklinePanel({ title, subtitle, points, tone = "#73c7ff", valueSuffix = "" }) {
  const normalized = points.length > 0 ? points : [{ label: "0", value: 0 }];
  const max = Math.max(...normalized.map((point) => point.value), 1);
  const width = 420;
  const height = 120;
  const path = normalized
    .map((point, index) => {
      const x = normalized.length === 1 ? width / 2 : (index / (normalized.length - 1)) * width;
      const y = height - (point.value / max) * (height - 18) - 9;
      return `${index === 0 ? "M" : "L"} ${x} ${y}`;
    })
    .join(" ");

  const latest = normalized[normalized.length - 1]?.value || 0;

  return (
    <div className="rounded-[28px] border border-white/8 bg-slate-950/45 p-5">
      <div className="flex items-end justify-between gap-3">
        <div>
          <p className="text-[10px] uppercase tracking-[0.28em] text-steel">{title}</p>
          {subtitle ? <p className="mt-2 text-sm leading-6 text-slate-400">{subtitle}</p> : null}
        </div>
        <div className="text-right">
          <p className="text-xs uppercase tracking-[0.22em] text-steel">Latest</p>
          <p className="mt-2 text-2xl font-semibold text-white">
            {latest}
            {valueSuffix}
          </p>
        </div>
      </div>

      <div className="mt-5 overflow-hidden rounded-[24px] border border-white/8 bg-gradient-to-br from-white/[0.04] to-transparent p-4">
        <svg viewBox={`0 0 ${width} ${height}`} className="h-40 w-full">
          {[0.25, 0.5, 0.75].map((stop) => (
            <line
              key={stop}
              x1="0"
              x2={width}
              y1={height * stop}
              y2={height * stop}
              stroke="rgba(255,255,255,0.08)"
              strokeDasharray="5 7"
            />
          ))}
          <path d={`${path} L ${width} ${height} L 0 ${height} Z`} fill={`${tone}22`} />
          <path d={path} fill="none" stroke={tone} strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
          {normalized.map((point, index) => {
            const x = normalized.length === 1 ? width / 2 : (index / (normalized.length - 1)) * width;
            const y = height - (point.value / max) * (height - 18) - 9;
            return <circle key={`${point.label}-${index}`} cx={x} cy={y} r="4.5" fill={tone} stroke="#071018" strokeWidth="2" />;
          })}
        </svg>

        <div className="mt-4 grid gap-2 sm:grid-cols-3">
          {normalized.slice(-3).map((point) => (
            <div key={point.label} className="rounded-2xl border border-white/8 bg-white/5 px-3 py-2">
              <p className="text-[10px] uppercase tracking-[0.22em] text-steel">{point.label}</p>
              <p className="mt-2 text-sm font-semibold text-white">
                {point.value}
                {valueSuffix}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
