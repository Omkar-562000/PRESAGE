import { Outlet } from "react-router-dom";
import { useState } from "react";
import { Sidebar } from "./Sidebar";

export function WorkspaceShell({ siem }) {
  const [query, setQuery] = useState("");

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-[1600px] gap-4 px-4 py-4 sm:px-6 lg:px-8">
      <div className="hidden w-[340px] shrink-0 lg:block">
        <Sidebar query={query} setQuery={setQuery} />
      </div>
      <section className="min-w-0 flex-1 space-y-6">
        <header className="rounded-[30px] border border-white/10 bg-gradient-to-br from-slate-950 via-panel to-slate-900 px-6 py-6 shadow-panel">
          <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <p className="text-[11px] uppercase tracking-[0.32em] text-mint">Security Operations Workspace</p>
              <h1 className="mt-3 font-display text-4xl text-white">Presage SIEM Interface</h1>
              <p className="mt-3 max-w-3xl text-sm leading-7 text-slate-300">
                Search the left navigation to jump between modules and features. Each route isolates a specific part of the SIEM story for cleaner demos and easier extension.
              </p>
            </div>
            <div className="grid gap-3 sm:grid-cols-3">
              <div className="rounded-2xl border border-white/8 bg-white/5 px-4 py-3">
                <p className="text-xs uppercase tracking-[0.22em] text-steel">Client</p>
                <p className="mt-2 text-sm text-white">{siem.config?.client || "Mid-Size Enterprise Client"}</p>
              </div>
              <div className="rounded-2xl border border-white/8 bg-white/5 px-4 py-3">
                <p className="text-xs uppercase tracking-[0.22em] text-steel">Workspace</p>
                <p className="mt-2 text-sm text-white">{siem.config?.workspace_name || "presage-siem-workspace"}</p>
              </div>
              <div className="rounded-2xl border border-white/8 bg-white/5 px-4 py-3">
                <p className="text-xs uppercase tracking-[0.22em] text-steel">Time</p>
                <p className="mt-2 text-sm text-white">{siem.clock} IST</p>
              </div>
            </div>
          </div>
        </header>

        {siem.error ? (
          <div className="rounded-2xl border border-rose/25 bg-rose/10 px-5 py-4 text-sm text-rose">{siem.error}</div>
        ) : null}

        <Outlet />
      </section>
    </main>
  );
}

