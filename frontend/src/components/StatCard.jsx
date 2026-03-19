export function StatCard({ label, value, accent, hint }) {
  return (
    <div className="group relative overflow-hidden rounded-[28px] border border-white/8 bg-panel/75 p-5 shadow-panel backdrop-blur transition duration-300 hover:-translate-y-1 hover:border-sky/20 hover:shadow-float">
      <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-sky/80 via-gold/70 to-mint/80 opacity-70" />
      <p className="text-[11px] uppercase tracking-[0.3em] text-steel">{label}</p>
      <p className={`mt-4 text-4xl font-semibold tracking-tight ${accent}`}>{value}</p>
      <p className="mt-3 text-sm leading-6 text-slate-400">{hint}</p>
    </div>
  );
}
