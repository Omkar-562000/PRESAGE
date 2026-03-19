import { SectionCard } from "./SectionCard";
import { SEVERITY_STYLES } from "../lib/ui";

export function AttackModulePage({ module, siem, evidenceTitle, logicItems }) {
  const isRunning = siem.runningAttack === module.id;

  return (
    <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
      <SectionCard title={module.title} subtitle={module.subtitle}>
        <div className="space-y-6">
          <div className="flex flex-wrap items-center gap-3">
            <span className={`rounded-full px-3 py-1 text-xs font-semibold ${SEVERITY_STYLES[module.severity]}`}>
              {module.severity}
            </span>
            <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-300">MITRE: {module.mitre}</span>
            <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-300">Signal: {module.signal}</span>
            <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-300">Code: {module.code}</span>
          </div>

          <div className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
            <div className="rounded-[26px] border border-white/8 bg-gradient-to-br from-slate-950/70 via-panel/80 to-shell/70 p-5 shadow-panel">
              <p className="text-[10px] uppercase tracking-[0.3em] text-gold">Threat Brief</p>
              <p className="mt-4 text-sm leading-7 text-slate-300">{module.description}</p>
              <div className="mt-5 rounded-2xl border border-white/8 bg-slate-950/45 p-4">
                <p className="text-xs uppercase tracking-[0.22em] text-steel">Detection Logic</p>
                <p className="mt-2 text-sm leading-7 text-white">{module.logicSummary}</p>
              </div>
            </div>
            <div className="grid gap-3">
              <div className="rounded-2xl border border-white/8 bg-white/5 p-4">
                <p className="text-[10px] uppercase tracking-[0.24em] text-steel">Command Focus</p>
                <p className="mt-2 text-base font-semibold text-white">{module.command}</p>
              </div>
              <div className="rounded-2xl border border-white/8 bg-white/5 p-4">
                <p className="text-[10px] uppercase tracking-[0.24em] text-steel">Operational Risk</p>
                <p className="mt-2 text-base font-semibold text-white">{module.risk}</p>
              </div>
              <div className="rounded-2xl border border-white/8 bg-white/5 p-4">
                <p className="text-[10px] uppercase tracking-[0.24em] text-steel">Signal Source</p>
                <p className="mt-2 text-base font-semibold text-white">{module.signal}</p>
              </div>
            </div>
          </div>

          <button
            type="button"
            onClick={() => siem.runAttack(module.id)}
            className="rounded-full border border-sky/35 bg-gradient-to-r from-sky/20 via-cobalt/15 to-mint/15 px-8 py-4 text-sm font-semibold uppercase tracking-[0.22em] text-white transition hover:border-sky/50 hover:bg-sky/30"
          >
            {isRunning ? "Launching Module..." : `Run ${module.title}`}
          </button>
        </div>
      </SectionCard>

      <SectionCard title={evidenceTitle} subtitle="What this module proves inside the working SIEM flow.">
        <div className="space-y-3">
          {logicItems.map((item, index) => (
            <div key={item} className="rounded-2xl border border-white/8 bg-white/5 p-4 text-sm leading-7 text-slate-300">
              <p className="text-[10px] uppercase tracking-[0.26em] text-steel">Step {index + 1}</p>
              <p className="mt-2">{item}</p>
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
