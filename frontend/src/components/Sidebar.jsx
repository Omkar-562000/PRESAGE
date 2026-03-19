import { Link, NavLink } from "react-router-dom";
import { APP_BRAND, ATTACKS, FEATURE_PAGES, SEVERITY_STYLES } from "../lib/ui";

function NavGroup({ title, items, query }) {
  const filtered = items.filter((item) => {
    const text = `${item.label || item.title} ${item.description || item.subtitle || ""}`.toLowerCase();
    return !query || text.includes(query.toLowerCase());
  });

  if (filtered.length === 0) {
    return null;
  }

  return (
    <div>
      <p className="px-3 text-[11px] uppercase tracking-[0.28em] text-steel">{title}</p>
      <div className="mt-3 space-y-2">
        {filtered.map((item) => (
          <NavLink
            key={item.route}
            to={item.route}
            end={item.route === "/workspace"}
            className={({ isActive }) =>
              `block rounded-[22px] border px-4 py-4 transition ${
                isActive
                  ? "border-sky/40 bg-gradient-to-r from-sky/15 via-cobalt/10 to-mint/10 text-white shadow-float"
                  : "border-white/8 bg-white/5 text-slate-300 hover:border-white/15 hover:bg-white/10"
              }`
            }
          >
            <div className="flex items-start justify-between gap-3">
              <div>
                {item.tag ? <p className="text-[10px] uppercase tracking-[0.28em] text-steel">{item.tag}</p> : null}
                <p className="mt-1 text-sm font-semibold">{item.label || item.title}</p>
                <p className="mt-1 text-xs leading-5 text-slate-400">{item.description || item.subtitle}</p>
              </div>
              {item.severity ? (
                <span className={`rounded-full px-2 py-1 text-[10px] font-semibold ${SEVERITY_STYLES[item.severity]}`}>
                  {item.severity}
                </span>
              ) : null}
            </div>
          </NavLink>
        ))}
      </div>
    </div>
  );
}

export function Sidebar({ query, setQuery }) {
  const featuredAttack = ATTACKS[0];

  return (
    <aside className="relative flex h-full flex-col overflow-hidden rounded-[32px] border border-white/10 bg-shell/85 p-4 shadow-panel backdrop-blur">
      <div className="pointer-events-none absolute inset-x-6 top-0 h-px bg-gradient-to-r from-transparent via-sky/60 to-transparent" />
      <Link to="/" className="rounded-[26px] border border-white/8 bg-gradient-to-br from-slate-950/80 via-slate-900/70 to-shell/80 p-5 transition hover:border-sky/35 hover:bg-slate-950">
        <div className="flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl border border-sky/20 bg-gradient-to-br from-sky/20 via-cobalt/15 to-mint/10 text-lg font-semibold text-white shadow-float animate-pulse-glow">
            PR
          </div>
          <div>
            <p className="font-display text-2xl text-white">{APP_BRAND.name}</p>
            <p className="mt-1 text-sm text-steel">{APP_BRAND.subtitle}</p>
          </div>
        </div>
      </Link>

      <div className="mt-4">
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search modules or views"
          className="w-full rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-sky/40 focus:bg-slate-950"
        />
      </div>

      <div className="mt-5 rounded-[24px] border border-gold/15 bg-gradient-to-br from-gold/10 via-white/5 to-transparent p-4">
        <p className="text-[10px] uppercase tracking-[0.28em] text-gold">Featured Scenario</p>
        <p className="mt-3 text-lg font-semibold text-white">{featuredAttack.title}</p>
        <p className="mt-2 text-sm leading-6 text-slate-300">{featuredAttack.risk}</p>
        <Link to={featuredAttack.route} className="mt-4 inline-flex rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.22em] text-white transition hover:border-sky/30 hover:bg-sky/10">
          Open Module
        </Link>
      </div>

      <div className="mt-6 space-y-6 overflow-y-auto pr-1">
        <NavGroup title="Workspace" items={FEATURE_PAGES} query={query} />
        <NavGroup title="Attack Modules" items={ATTACKS} query={query} />
      </div>
    </aside>
  );
}
