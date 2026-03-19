export function IncidentFilters({ search, severity, status, onSearch, onSeverity, onStatus }) {
  return (
    <div className="grid gap-3 rounded-2xl border border-white/8 bg-slate-950/45 p-4 md:grid-cols-3">
      <input
        value={search}
        onChange={(event) => onSearch(event.target.value)}
        placeholder="Search title, entity, MITRE"
        className="rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-sky/40"
      />
      <select
        value={severity}
        onChange={(event) => onSeverity(event.target.value)}
        className="rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none focus:border-sky/40"
      >
        <option value="All">All severities</option>
        <option value="High">High</option>
        <option value="Medium">Medium</option>
        <option value="Low">Low</option>
      </select>
      <select
        value={status}
        onChange={(event) => onStatus(event.target.value)}
        className="rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none focus:border-sky/40"
      >
        <option value="All">All statuses</option>
        <option value="New">New</option>
        <option value="Under Investigation">Under Investigation</option>
      </select>
    </div>
  );
}
