const FALLBACK_SEGMENTS = [
  { label: "High", value: 0, color: "#ff6e7d" },
  { label: "Medium", value: 0, color: "#f3a941" },
  { label: "Low", value: 0, color: "#4ad4a0" },
];

export function ThreatDonut({ title, subtitle, segments = FALLBACK_SEGMENTS, totalLabel = "Total incidents" }) {
  const normalizedSegments = segments.length > 0 ? segments : FALLBACK_SEGMENTS;
  const total = normalizedSegments.reduce((sum, segment) => sum + segment.value, 0);
  const radius = 66;
  const circumference = 2 * Math.PI * radius;
  let offset = 0;

  return (
    <div className="rounded-[28px] border border-white/8 bg-gradient-to-br from-slate-950/70 via-panel/80 to-slate-950/55 p-5">
      <p className="text-[10px] uppercase tracking-[0.28em] text-steel">{title}</p>
      {subtitle ? <p className="mt-2 text-sm leading-6 text-slate-400">{subtitle}</p> : null}

      <div className="mt-5 grid items-center gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <div className="relative mx-auto flex h-52 w-52 items-center justify-center">
          <svg viewBox="0 0 180 180" className="h-full w-full -rotate-90">
            <circle cx="90" cy="90" r={radius} stroke="rgba(255,255,255,0.08)" strokeWidth="18" fill="none" />
            {normalizedSegments.map((segment) => {
              const segmentLength = total > 0 ? (segment.value / total) * circumference : 0;
              const circle = (
                <circle
                  key={segment.label}
                  cx="90"
                  cy="90"
                  r={radius}
                  fill="none"
                  stroke={segment.color}
                  strokeWidth="18"
                  strokeDasharray={`${segmentLength} ${circumference - segmentLength}`}
                  strokeDashoffset={-offset}
                  strokeLinecap="round"
                />
              );
              offset += segmentLength;
              return circle;
            })}
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <p className="text-[10px] uppercase tracking-[0.28em] text-steel">{totalLabel}</p>
            <p className="mt-2 text-4xl font-semibold text-white">{total}</p>
            <p className="mt-2 text-xs text-slate-400">Live severity mix</p>
          </div>
        </div>

        <div className="space-y-3">
          {normalizedSegments.map((segment) => (
            <div key={segment.label} className="rounded-2xl border border-white/8 bg-white/5 px-4 py-3">
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <span className="h-3 w-3 rounded-full" style={{ backgroundColor: segment.color }} />
                  <span className="text-sm font-medium text-white">{segment.label}</span>
                </div>
                <span className="text-sm font-semibold text-white">{segment.value}</span>
              </div>
              <div className="mt-3 h-2 overflow-hidden rounded-full bg-white/5">
                <div
                  className="h-full rounded-full"
                  style={{
                    width: `${total > 0 ? (segment.value / total) * 100 : 0}%`,
                    backgroundColor: segment.color,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
