import { SectionCard } from "./SectionCard";
import { SEVERITY_STYLES } from "../lib/ui";

export function AttackModulePage({ module, siem, evidenceTitle, logicItems }) {
  const isRunning = siem.runningAttack === module.id;

  return (
    <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
      <SectionCard title={module.title} subtitle={module.subtitle}>
        <div className="space-y-5">
          <div className="flex flex-wrap items-center gap-3">
            <span className={`rounded-full px-3 py-1 text-xs font-semibold ${SEVERITY_STYLES[module.severity]}`}>
              {module.severity}
            </span>
            <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-300">MITRE: {module.mitre}</span>
            <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-300">Signal: {module.signal}</span>
          </div>

          <p className="text-sm leading-7 text-slate-300">{module.description}</p>

          <div className="rounded-2xl border border-white/8 bg-slate-950/45 p-4">
            <p className="text-xs uppercase tracking-[0.22em] text-steel">Detection Logic</p>
            <p className="mt-2 text-sm leading-7 text-white">{module.logicSummary}</p>
          </div>

          <button
            type="button"
            onClick={() => siem.runAttack(module.id)}
            className="rounded-full border border-sky/35 bg-sky/20 px-6 py-3 text-sm font-semibold text-white transition hover:border-sky/50 hover:bg-sky/30"
          >
            {isRunning ? "Launching Module..." : `Run ${module.title}`}
          </button>
        </div>
      </SectionCard>

      <SectionCard title={evidenceTitle} subtitle="What this module proves inside the working SIEM flow.">
        <div className="space-y-3">
          {logicItems.map((item) => (
            <div key={item} className="rounded-2xl border border-white/8 bg-white/5 p-4 text-sm leading-7 text-slate-300">
              {item}
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
