export const APP_BRAND = {
  name: "Presage SIEM",
  subtitle: "Real-Time Threat Detection Platform",
};

export const ATTACKS = [
  {
    id: "brute_force",
    title: "Brute Force Login",
    subtitle: "Credential attack simulation",
    description: "Triggers repeated failed sign-ins against the admin account and validates threshold-based detection.",
    mitre: "TA0006 / T1110",
    severity: "High",
    route: "/workspace/modules/brute-force",
    signal: "SigninLogs",
    logicSummary: "Counts repeated failed sign-ins from the same attacker pattern inside a five-minute window.",
  },
  {
    id: "privilege_escalation",
    title: "Privilege Escalation",
    subtitle: "Unauthorized role assignment",
    description: "Creates an Azure activity event that promotes a user to admin to prove immediate alerting.",
    mitre: "TA0004 / T1078",
    severity: "High",
    route: "/workspace/modules/privilege-escalation",
    signal: "AzureActivity",
    logicSummary: "Raises an alert as soon as a role assignment write action appears in privileged activity logs.",
  },
  {
    id: "windows_failed_logon",
    title: "Windows Failed Logon",
    subtitle: "Real Windows credential burst",
    description: "Uses Windows Event style failed logons to demonstrate host-level credential attack detection.",
    mitre: "TA0006 / T1110",
    severity: "High",
    route: "/workspace/modules/windows-failed-logon",
    signal: "WindowsEvent",
    logicSummary: "Counts repeated Windows failed logon events and opens a high-severity incident when a burst threshold is reached.",
  },
  {
    id: "port_scan",
    title: "Port Scan",
    subtitle: "Reconnaissance activity",
    description: "Sweeps multiple ports from an external IP to demonstrate network discovery detection.",
    mitre: "TA0043 / T1046",
    severity: "Medium",
    route: "/workspace/modules/port-scan",
    signal: "NetworkEvents",
    logicSummary: "Tracks distinct destination ports per source IP and triggers once the threshold is crossed in one minute.",
  },
];

export const FEATURE_PAGES = [
  { label: "Overview", route: "/workspace", description: "Executive summary and source health" },
  { label: "Incidents", route: "/workspace/incidents", description: "Incident queue and filtering" },
  { label: "Telemetry", route: "/workspace/telemetry", description: "Cross-source telemetry timeline" },
  { label: "Attack Center", route: "/workspace/attack-center", description: "All modules in one control page" },
];

export const SOURCE_STYLES = {
  SigninLogs: "bg-sky/15 text-sky ring-1 ring-inset ring-sky/30",
  SecurityEvent: "bg-amber/15 text-amber ring-1 ring-inset ring-amber/30",
  WindowsEvent: "bg-cyan-400/15 text-cyan-200 ring-1 ring-inset ring-cyan-300/30",
  AzureActivity: "bg-fuchsia-400/15 text-fuchsia-200 ring-1 ring-inset ring-fuchsia-300/30",
  NetworkEvents: "bg-mint/15 text-mint ring-1 ring-inset ring-mint/30",
};

export const SEVERITY_STYLES = {
  High: "bg-rose/15 text-rose ring-1 ring-inset ring-rose/25",
  Medium: "bg-amber/15 text-amber ring-1 ring-inset ring-amber/25",
  Low: "bg-mint/15 text-mint ring-1 ring-inset ring-mint/25",
};

export function getAttackById(id) {
  return ATTACKS.find((attack) => attack.id === id);
}

export function formatIncidentTime(value) {
  if (!value) {
    return "--";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value.slice(11, 19);
  }
  return date.toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

export function sourceSummary(log) {
  const table = log._table || log.table;
  if (table === "SigninLogs") {
    return log.ResultType === "0"
      ? `Successful sign-in for ${log.UserPrincipalName}`
      : `Failed sign-in for ${log.UserPrincipalName} from ${log.IPAddress}`;
  }
  if (table === "AzureActivity") {
    return `${log.OperationName} by ${log.Caller}`;
  }
  if (table === "WindowsEvent") {
    return `${log.Channel} event ${log.EventID} from ${log.Provider || "Windows"}`;
  }
  if (table === "NetworkEvents") {
    return `${log.SrcIP} scanned port ${log.DstPort} on ${log.DstIP}`;
  }
  return `${log.Activity || "Security event"} on ${log.Computer || "host"}`;
}

