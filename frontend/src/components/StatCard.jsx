export function StatCard({ label, value, accent, hint }) {
  return (
    <div className="rounded-3xl border border-white/8 bg-panel/80 p-5 shadow-panel backdrop-blur">
      <p className="text-[11px] uppercase tracking-[0.3em] text-steel">{label}</p>
      <p className={`mt-3 text-3xl font-semibold ${accent}`}>{value}</p>
      <p className="mt-2 text-sm text-slate-400">{hint}</p>
    </div>
  );
}
