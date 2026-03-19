import { useMemo, useState } from "react";
import { IncidentCard } from "../components/IncidentCard";
import { IncidentFilters } from "../components/IncidentFilters";
import { SectionCard } from "../components/SectionCard";

export function IncidentsPage({ siem }) {
  const [search, setSearch] = useState("");
  const [severity, setSeverity] = useState("All");
  const [status, setStatus] = useState("All");

  const filteredIncidents = useMemo(() => {
    return siem.incidents.filter((incident) => {
      const haystack = [incident.Title, incident.AffectedEntity, incident.MITRETactic, incident.SourceTable]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      const matchesSearch = !search || haystack.includes(search.toLowerCase());
      const matchesSeverity = severity === "All" || incident.Severity === severity;
      const matchesStatus = status === "All" || incident.Status === status;
      return matchesSearch && matchesSeverity && matchesStatus;
    });
  }, [search, severity, status, siem.incidents]);

  return (
    <SectionCard title="Incident Queue" subtitle="A dedicated page for active incidents, response status, and investigation details.">
      <div className="space-y-4">
        <IncidentFilters
          search={search}
          severity={severity}
          status={status}
          onSearch={setSearch}
          onSeverity={setSeverity}
          onStatus={setStatus}
        />
        <div className="flex items-center justify-between text-sm text-slate-400">
          <span>{filteredIncidents.length} incidents shown</span>
          <span>Live refresh every 2 seconds</span>
        </div>
        {siem.loading ? <p className="text-sm text-steel">Loading incidents...</p> : null}
        {!siem.loading && filteredIncidents.length === 0 ? <p className="text-sm text-steel">No incidents match the current filters.</p> : null}
        {filteredIncidents.map((incident) => (
          <IncidentCard key={`${incident.IncidentNumber}-${incident.CreatedTime}`} incident={incident} />
        ))}
      </div>
    </SectionCard>
  );
}
