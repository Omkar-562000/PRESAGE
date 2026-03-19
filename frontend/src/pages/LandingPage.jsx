import { Link } from "react-router-dom";
import { APP_BRAND } from "../lib/ui";

export function LandingPage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-6 py-10">
      <section className="w-full max-w-4xl rounded-[36px] border border-white/10 bg-gradient-to-br from-slate-950 via-panel to-slate-900 px-8 py-14 text-center shadow-panel">
        <Link
          to="/workspace"
          className="mx-auto inline-flex h-28 w-28 items-center justify-center rounded-full border border-sky/30 bg-sky/15 text-3xl font-semibold text-white shadow-[0_0_40px_rgba(110,199,255,0.2)] transition hover:border-sky/45 hover:bg-sky/25"
        >
          WS
        </Link>
        <p className="mt-6 text-[11px] uppercase tracking-[0.35em] text-mint">Cybersecurity SecOps Demo</p>
        <h1 className="mt-4 font-display text-5xl text-white sm:text-6xl">{APP_BRAND.name}</h1>
        <p className="mt-4 text-lg text-slate-300">{APP_BRAND.subtitle}</p>
        <p className="mx-auto mt-8 max-w-2xl text-base leading-8 text-slate-300">
          This project demonstrates a working SIEM proof of concept with simulated enterprise telemetry, real-time threat detection, incident generation, alert tracking, and module-based attack walkthroughs for presentation and evaluation.
        </p>
        <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <Link
            to="/workspace"
            className="rounded-full border border-sky/35 bg-sky/20 px-8 py-4 text-sm font-semibold text-white transition hover:border-sky/50 hover:bg-sky/30"
          >
            Open Main Interface
          </Link>
          <p className="text-sm text-slate-400">Click the logo or the button to enter the dashboard workspace.</p>
        </div>
      </section>
    </main>
  );
}
