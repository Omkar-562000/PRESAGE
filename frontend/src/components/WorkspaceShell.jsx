import { NavLink, Outlet } from "react-router-dom";
import { useState } from "react";
import { Sidebar } from "./Sidebar";
import { APP_BRAND, FEATURE_PAGES } from "../lib/ui";

export function WorkspaceShell({ siem }) {
  const [query, setQuery] = useState("");

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-[1680px] gap-5 px-4 py-5 sm:px-6 lg:px-8">
      <div className="hidden w-[340px] shrink-0 lg:block">
        <Sidebar query={query} setQuery={setQuery} />
      </div>
      <section className="min-w-0 flex-1 space-y-6">
        <header className="relative overflow-hidden rounded-[34px] border border-white/10 bg-gradient-to-br from-slate-950 via-panel to-shell px-6 py-7 shadow-panel">
          <div className="pointer-events-none absolute -right-16 top-0 h-44 w-44 rounded-full bg-sky/10 blur-3xl" />
          <div className="pointer-events-none absolute bottom-0 left-10 h-24 w-56 rounded-full bg-gold/10 blur-3xl" />
          <div className="flex flex-col gap-6 xl:flex-row xl:items-end xl:justify-between">
            <div className="max-w-4xl">
              <p className="text-[11px] uppercase tracking-[0.36em] text-mint">{APP_BRAND.motto}</p>
              <h1 className="mt-4 max-w-3xl font-display text-5xl leading-[0.95] text-white xl:text-6xl">Presage Cyber Defense Console</h1>
              <p className="mt-4 max-w-3xl text-base leading-8 text-slate-300">
                A refined operations workspace for live telemetry, incident review, attack simulation, and executive-friendly security storytelling. Every view is arranged like a mission console rather than a simple academic dashboard.
              </p>
            </div>
            <div className="grid gap-3 md:grid-cols-3 xl:min-w-[640px]">
              <div className="rounded-[24px] border border-white/8 bg-white/5 px-4 py-4 backdrop-blur">
                <p className="text-xs uppercase tracking-[0.22em] text-steel">Client</p>
                <p className="mt-3 text-sm text-white">{siem.config?.client || "Mid-Size Enterprise Client"}</p>
              </div>
              <div className="rounded-[24px] border border-white/8 bg-white/5 px-4 py-4 backdrop-blur">
                <p className="text-xs uppercase tracking-[0.22em] text-steel">Workspace</p>
                <p className="mt-3 text-sm text-white">{siem.config?.workspace_name || "presage-siem-workspace"}</p>
              </div>
              <div className="rounded-[24px] border border-gold/15 bg-gradient-to-br from-gold/10 to-white/5 px-4 py-4 backdrop-blur">
                <p className="text-xs uppercase tracking-[0.22em] text-steel">Time</p>
                <p className="mt-3 text-sm text-white">{siem.clock} IST</p>
              </div>
            </div>
          </div>
        </header>

        <section className="rounded-[30px] border border-white/8 bg-shell/55 p-3 shadow-panel backdrop-blur">
          <div className="flex flex-wrap gap-3">
            {FEATURE_PAGES.map((item) => (
              <NavLink
                key={item.route}
                to={item.route}
                end={item.route === "/workspace"}
                className={({ isActive }) =>
                  `group min-w-[170px] flex-1 rounded-[24px] border px-4 py-4 transition ${
                    isActive
                      ? "border-sky/40 bg-gradient-to-r from-sky/15 via-cobalt/10 to-mint/10 text-white shadow-float"
                      : "border-white/8 bg-white/5 text-slate-300 hover:border-white/15 hover:bg-white/10"
                  }`
                }
              >
                <p className="text-[10px] uppercase tracking-[0.3em] text-steel">{item.tag}</p>
                <p className="mt-2 text-base font-semibold">{item.label}</p>
                <p className="mt-2 text-xs leading-5 text-slate-400">{item.description}</p>
              </NavLink>
            ))}
          </div>
        </section>

        {siem.error ? (
          <div className="rounded-2xl border border-rose/25 bg-rose/10 px-5 py-4 text-sm text-rose">{siem.error}</div>
        ) : null}

        <Outlet />
      </section>
    </main>
  );
}
