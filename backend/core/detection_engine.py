"""
Presage SIEM Project
Detection Engine — KQL-equivalent rules running in real time
Mirrors Microsoft Sentinel Scheduled Analytics Rules

Rules:
  Rule 1 — Brute Force Login Detection        (MITRE T1110)
  Rule 2 — Privilege Escalation Detection     (MITRE T1078.004)
  Rule 3 — Port Scan / Reconnaissance         (MITRE T1046)
"""

import time
import threading
from datetime import datetime, timezone
from collections import defaultdict


# ── Incident store ────────────────────────────────────────────────────────────
incidents   = []          # all fired incidents
_inc_lock   = threading.Lock()
_alert_cbs  = []          # alert listeners (UI, reporter)

_inc_id_counter = [0]

def register_alert_callback(fn):
    _alert_cbs.append(fn)

def _fire_incident(rule_name, severity, description, entities, attack_start_time=None):
    now = datetime.now(timezone.utc)
    mttd = round((now.timestamp() - attack_start_time), 2) \
           if attack_start_time else None

    with _inc_lock:
        _inc_id_counter[0] += 1
        inc = {
            "id":           f"INC-{_inc_id_counter[0]:04d}",
            "rule":         rule_name,
            "severity":     severity,
            "status":       "New",
            "description":  description,
            "entities":     entities,
            "detected_at":  now.isoformat(),
            "mttd_seconds": mttd,
            "mitre":        _MITRE_MAP.get(rule_name, ""),
            "response":     [],
        }
        incidents.append(inc)

    for fn in _alert_cbs:
        try:
            fn(inc)
        except Exception:
            pass
    return inc


_MITRE_MAP = {
    "Brute Force Login Detection":    "T1110 — Brute Force",
    "Privilege Escalation Detected":  "T1078.004 — Valid Accounts: Cloud",
    "Port Scan Detected":             "T1046 — Network Service Discovery",
}


# ── Rule state ────────────────────────────────────────────────────────────────
# Each rule keeps lightweight sliding-window counters.
_brute_state = defaultdict(list)   # ip -> [timestamps]
_priv_seen   = set()               # (user, role) pairs already alerted
_scan_state  = defaultdict(dict)   # ip -> {port: timestamp}

# Track when attacks started (set by injectors via hooks)
_attack_timestamps = {}

def record_attack_start(attack_type: str):
    _attack_timestamps[attack_type] = time.time()

def _get_attack_start(attack_type: str):
    return _attack_timestamps.get(attack_type)


# ── Rule 1 — Brute Force ──────────────────────────────────────────────────────
BRUTE_THRESHOLD = 5      # failed logins
BRUTE_WINDOW    = 300    # seconds (5 minutes)

def _check_brute_force(event: dict):
    if event.get("table") != "SigninLogs":
        return
    if event.get("ResultType") == "0":
        return  # successful login — ignore

    ip  = event.get("IPAddress", "unknown")
    now = time.time()

    _brute_state[ip].append(now)
    # prune old entries outside window
    _brute_state[ip] = [t for t in _brute_state[ip]
                         if now - t <= BRUTE_WINDOW]

    if len(_brute_state[ip]) == BRUTE_THRESHOLD:
        user = event.get("UserPrincipalName", "unknown")
        start = _get_attack_start("brute_force")
        inc = _fire_incident(
            rule_name   = "Brute Force Login Detection",
            severity    = "High",
            description = (f"{len(_brute_state[ip])} failed login attempts "
                           f"from {ip} against {user} "
                           f"within {BRUTE_WINDOW // 60} minutes."),
            entities    = {"user": user, "ip": ip,
                           "failed_count": len(_brute_state[ip])},
            attack_start_time = start,
        )
        # reset so we don't re-alert on every subsequent event
        _brute_state[ip] = []
        return inc


# ── Rule 2 — Privilege Escalation ─────────────────────────────────────────────
HIGH_PRIV_ROLES = {
    "Global Administrator",
    "Security Administrator",
    "User Access Administrator",
    "Privileged Role Administrator",
}

def _check_privilege_escalation(event: dict):
    if event.get("table") != "AuditLogs":
        return
    if event.get("OperationName") != "Add member to role":
        return

    role = event.get("RoleAssigned", "")
    if role not in HIGH_PRIV_ROLES:
        return

    targets = event.get("TargetResources", [{}])
    user    = targets[0].get("userPrincipalName", "unknown") if targets else "unknown"
    key     = (user, role)

    if key in _priv_seen:
        return
    _priv_seen.add(key)

    start = _get_attack_start("privilege_escalation")
    return _fire_incident(
        rule_name   = "Privilege Escalation Detected",
        severity    = "High",
        description = (f"User {user} was assigned the privileged role "
                       f"'{role}'. Immediate review required."),
        entities    = {"user": user, "role": role},
        attack_start_time = start,
    )


# ── Rule 3 — Port Scan ────────────────────────────────────────────────────────
SCAN_THRESHOLD = 20     # unique ports
SCAN_WINDOW    = 60     # seconds

def _check_port_scan(event: dict):
    if event.get("table") != "NetworkAnalytics":
        return

    src  = event.get("SrcIP", "unknown")
    port = event.get("DstPort")
    now  = time.time()

    if src not in _scan_state:
        _scan_state[src] = {}
    _scan_state[src][port] = now

    # prune old entries
    _scan_state[src] = {p: t for p, t in _scan_state[src].items()
                        if now - t <= SCAN_WINDOW}

    if len(_scan_state[src]) == SCAN_THRESHOLD:
        start = _get_attack_start("port_scan")
        inc = _fire_incident(
            rule_name   = "Port Scan Detected",
            severity    = "Medium",
            description = (f"Source IP {src} scanned "
                           f"{len(_scan_state[src])} unique ports "
                           f"within {SCAN_WINDOW} seconds. "
                           f"Possible reconnaissance activity."),
            entities    = {"src_ip": src,
                           "ports_scanned": len(_scan_state[src]),
                           "sample_ports": list(_scan_state[src].keys())[:5]},
            attack_start_time = start,
        )
        _scan_state[src] = {}
        return inc


# ── Main event processor ──────────────────────────────────────────────────────
def process_event(event: dict):
    """Called by log_generator for every emitted event."""
    _check_brute_force(event)
    _check_privilege_escalation(event)
    _check_port_scan(event)


# ── Rule summary (for documentation) ─────────────────────────────────────────
RULES_SUMMARY = [
    {
        "name":      "Brute Force Login Detection",
        "severity":  "High",
        "table":     "SigninLogs",
        "logic":     f"ResultType != 0 | summarize count() by IPAddress, "
                     f"bin(TimeGenerated, 5m) | where count >= {BRUTE_THRESHOLD}",
        "mitre":     "T1110",
        "threshold": f"{BRUTE_THRESHOLD} failures in {BRUTE_WINDOW // 60} min",
    },
    {
        "name":      "Privilege Escalation Detected",
        "severity":  "High",
        "table":     "AuditLogs",
        "logic":     "OperationName == 'Add member to role' "
                     "| where RoleAssigned in (HIGH_PRIV_ROLES)",
        "mitre":     "T1078.004",
        "threshold": "Any assignment to privileged role",
    },
    {
        "name":      "Port Scan Detected",
        "severity":  "Medium",
        "table":     "NetworkAnalytics",
        "logic":     f"summarize dcount(DstPort) by SrcIP, "
                     f"bin(TimeGenerated, 1m) | where dcount >= {SCAN_THRESHOLD}",
        "mitre":     "T1046",
        "threshold": f"{SCAN_THRESHOLD} unique ports in {SCAN_WINDOW}s",
    },
]


