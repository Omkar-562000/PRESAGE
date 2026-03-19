import { SectionCard } from "../components/SectionCard";
import { ATTACKS, SEVERITY_STYLES } from "../lib/ui";

export function AttackLabPage({ siem }) {
  return (
    <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
      <SectionCard title="Attack Center" subtitle="Use this command bay to launch each scenario and prove detection coverage.">
        <div className="grid gap-4 lg:grid-cols-2">
          {ATTACKS.map((attack) => {
            const isRunning = siem.runningAttack === attack.id;
            return (
              <button
                key={attack.id}
                type="button"
                onClick={() => siem.runAttack(attack.id)}
                className="group overflow-hidden rounded-[26px] border border-white/10 bg-gradient-to-br from-slate-950/70 via-panel/80 to-shell/70 p-5 text-left shadow-panel transition hover:-translate-y-1 hover:border-sky/30 hover:shadow-float"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-[10px] uppercase tracking-[0.32em] text-steel">{attack.code}</p>
                    <h3 className="mt-2 font-display text-2xl text-white">{attack.title}</h3>
                    <p className="mt-1 text-xs uppercase tracking-[0.22em] text-slate-400">{attack.command}</p>
                  </div>
                  <span className={`rounded-full px-3 py-1 text-xs font-semibold ${SEVERITY_STYLES[attack.severity]}`}>
                    {attack.severity}
                  </span>
                </div>
                <p className="mt-4 text-sm leading-7 text-slate-300">{attack.description}</p>
                <div className="mt-5 grid gap-3 sm:grid-cols-2">
                  <div className="rounded-2xl border border-white/8 bg-white/5 p-3">
                    <p className="text-[10px] uppercase tracking-[0.24em] text-steel">Signal</p>
                    <p className="mt-2 text-sm text-white">{attack.signal}</p>
                  </div>
                  <div className="rounded-2xl border border-white/8 bg-white/5 p-3">
                    <p className="text-[10px] uppercase tracking-[0.24em] text-steel">Risk</p>
                    <p className="mt-2 text-sm text-white">{attack.risk}</p>
                  </div>
                </div>
                <div className="mt-5 flex items-center justify-between text-sm">
                  <span className="text-sky">{attack.mitre}</span>
                  <span className={isRunning ? "text-amber" : "text-mint"}>{isRunning ? "Launching..." : "Run Scenario"}</span>
                </div>
              </button>
            );
          })}
        </div>
      </SectionCard>

      <SectionCard title="Moderator Script" subtitle="Use this panel to tell a sharper story while you navigate the product.">
        <div className="space-y-4 text-sm leading-7 text-slate-300">
          <div className="rounded-2xl border border-white/8 bg-white/5 p-4">
            Begin on Overview and Telemetry to prove the platform is already ingesting and monitoring live signals.
          </div>
          <div className="rounded-2xl border border-white/8 bg-white/5 p-4">
            Launch one scenario from this page, then move straight to Incidents to show the attack-to-case transition.
          </div>
          <div className="rounded-2xl border border-white/8 bg-white/5 p-4">
            Explain that the attack logic lives in backend modules while the React interface is acting as the operations console.
          </div>
          <div className="rounded-2xl border border-gold/15 bg-gradient-to-br from-gold/10 to-white/5 p-4 text-white">
            Current session: Incidents {siem.stats.total_incidents}, Alerts {siem.stats.total_alerts}, Avg MTTD {siem.mttd?.average ? `${siem.mttd.average}s` : "--"}
          </div>
        </div>
      </SectionCard>
    </div>
  );
}
