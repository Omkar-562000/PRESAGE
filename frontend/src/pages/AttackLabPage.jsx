import { SectionCard } from "../components/SectionCard";
import { ATTACKS, SEVERITY_STYLES } from "../lib/ui";

export function AttackLabPage({ siem }) {
  return (
    <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
      <SectionCard title="Attack Center" subtitle="Central control room for all attack modules.">
        <div className="grid gap-4 lg:grid-cols-1">
          {ATTACKS.map((attack) => {
            const isRunning = siem.runningAttack === attack.id;
            return (
              <button
                key={attack.id}
                type="button"
                onClick={() => siem.runAttack(attack.id)}
                className="group rounded-[24px] border border-white/10 bg-slate-950/50 p-5 text-left transition hover:-translate-y-0.5 hover:border-sky/40 hover:bg-slate-950"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-xs uppercase tracking-[0.3em] text-steel">{attack.subtitle}</p>
                    <h3 className="mt-2 text-xl font-semibold text-white">{attack.title}</h3>
                  </div>
                  <span className={`rounded-full px-3 py-1 text-xs font-semibold ${SEVERITY_STYLES[attack.severity]}`}>
                    {attack.severity}
                  </span>
                </div>
                <p className="mt-4 text-sm leading-6 text-slate-300">{attack.description}</p>
                <div className="mt-5 flex items-center justify-between text-sm">
                  <span className="text-sky">{attack.mitre}</span>
                  <span className={isRunning ? "text-amber" : "text-mint"}>{isRunning ? "Launching..." : "Run Attack"}</span>
                </div>
              </button>
            );
          })}
        </div>
      </SectionCard>

      <SectionCard title="Presentation Flow" subtitle="Suggested storytelling order for the Scrum or review meeting.">
        <div className="space-y-4 text-sm leading-7 text-slate-300">
          <div className="rounded-2xl border border-white/8 bg-white/5 p-4">
            Start on the landing page, then enter the workspace to establish the product identity and project purpose.
          </div>
          <div className="rounded-2xl border border-white/8 bg-white/5 p-4">
            Show the source health and telemetry pages to prove ongoing monitoring before any simulated attack is launched.
          </div>
          <div className="rounded-2xl border border-white/8 bg-white/5 p-4">
            Open each module page from the sidebar, run the attack, and then move to the incidents page to show immediate outcomes.
          </div>
          <div className="rounded-2xl border border-mint/20 bg-mint/10 p-4 text-white">
            Current session: Incidents {siem.stats.total_incidents}, Alerts {siem.stats.total_alerts}, Avg MTTD {siem.mttd?.average ? `${siem.mttd.average}s` : "--"}
          </div>
        </div>
      </SectionCard>
    </div>
  );
}
