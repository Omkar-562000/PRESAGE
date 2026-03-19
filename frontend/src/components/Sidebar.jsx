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
              `block rounded-2xl border px-4 py-3 transition ${
                isActive
                  ? "border-sky/40 bg-sky/15 text-white"
                  : "border-white/8 bg-white/5 text-slate-300 hover:border-white/15 hover:bg-white/10"
              }`
            }
          >
            <div className="flex items-center justify-between gap-3">
              <div>
                <p className="text-sm font-semibold">{item.label || item.title}</p>
                <p className="mt-1 text-xs text-slate-400">{item.description || item.subtitle}</p>
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
  return (
    <aside className="flex h-full flex-col rounded-[28px] border border-white/10 bg-panel/90 p-4 shadow-panel backdrop-blur">
      <Link to="/" className="rounded-[24px] border border-white/8 bg-slate-950/50 p-4 transition hover:border-sky/35 hover:bg-slate-950">
        <p className="font-display text-2xl text-white">{APP_BRAND.name}</p>
        <p className="mt-1 text-sm text-steel">{APP_BRAND.subtitle}</p>
      </Link>

      <div className="mt-4">
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search modules or pages"
          className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-sky/40"
        />
      </div>

      <div className="mt-6 space-y-6 overflow-y-auto pr-1">
        <NavGroup title="Workspace" items={FEATURE_PAGES} query={query} />
        <NavGroup title="Attack Modules" items={ATTACKS} query={query} />
      </div>
    </aside>
  );
}
