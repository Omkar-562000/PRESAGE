import { Link } from "react-router-dom";
import { APP_BRAND } from "../lib/ui";

export function LandingPage() {
  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden px-6 py-10">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-64 bg-gradient-to-b from-gold/10 to-transparent" />
      <div className="pointer-events-none absolute -left-24 top-20 h-72 w-72 rounded-full bg-sky/10 blur-3xl animate-float-slow" />
      <div className="pointer-events-none absolute -right-16 bottom-10 h-80 w-80 rounded-full bg-mint/10 blur-3xl animate-float-slow" />
      <section className="relative w-full max-w-6xl overflow-hidden rounded-[40px] border border-white/10 bg-gradient-to-br from-slate-950 via-panel to-shell px-8 py-14 text-center shadow-panel sm:px-12">
        <div className="pointer-events-none absolute inset-x-10 top-0 h-px bg-gradient-to-r from-transparent via-gold/70 to-transparent" />
        <Link
          to="/workspace"
          className="mx-auto inline-flex h-32 w-32 items-center justify-center rounded-[34px] border border-white/10 bg-gradient-to-br from-sky/20 via-cobalt/10 to-mint/10 text-3xl font-semibold text-white shadow-float transition hover:-translate-y-1 hover:border-sky/45 hover:bg-sky/25"
        >
          PR
        </Link>
        <p className="mt-8 text-[11px] uppercase tracking-[0.42em] text-gold">Cybersecurity Command Experience</p>
        <h1 className="mx-auto mt-5 max-w-4xl font-display text-6xl leading-[0.9] text-white sm:text-7xl">{APP_BRAND.name}</h1>
        <p className="mt-5 text-xl text-slate-300">{APP_BRAND.subtitle}</p>
        <p className="mx-auto mt-8 max-w-3xl text-base leading-8 text-slate-300 sm:text-lg">
          Presage transforms attack telemetry into a polished executive-grade operations experience, combining live monitoring, incident intelligence, attack simulation, and response storytelling in one focused interface.
        </p>
        <div className="mx-auto mt-10 grid max-w-4xl gap-4 text-left md:grid-cols-3">
          <div className="rounded-[24px] border border-white/8 bg-white/5 p-5 backdrop-blur">
            <p className="text-[11px] uppercase tracking-[0.28em] text-steel">Visibility</p>
            <p className="mt-3 text-lg font-semibold text-white">Unified telemetry across identity, cloud, host, and network signals.</p>
          </div>
          <div className="rounded-[24px] border border-white/8 bg-white/5 p-5 backdrop-blur">
            <p className="text-[11px] uppercase tracking-[0.28em] text-steel">Detection</p>
            <p className="mt-3 text-lg font-semibold text-white">Focused attack modules with MITRE-aligned rules and real incident creation.</p>
          </div>
          <div className="rounded-[24px] border border-white/8 bg-white/5 p-5 backdrop-blur">
            <p className="text-[11px] uppercase tracking-[0.28em] text-steel">Response</p>
            <p className="mt-3 text-lg font-semibold text-white">Playbook-driven follow-up that makes the demo feel operational, not academic.</p>
          </div>
        </div>
        <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <Link
            to="/workspace"
            className="rounded-full border border-sky/35 bg-sky/20 px-10 py-4 text-sm font-semibold uppercase tracking-[0.22em] text-white transition hover:border-sky/50 hover:bg-sky/30"
          >
            Enter Presage
          </Link>
          <p className="text-sm text-slate-400">Click the logo or enter directly to open the operations workspace.</p>
        </div>
      </section>
    </main>
  );
}
