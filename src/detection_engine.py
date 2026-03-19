"""
Wissen Infotech SIEM Project
Detection Engine — KQL-equivalent rules running locally
Mirrors Microsoft Sentinel Scheduled Analytics Rules logic

Rules implemented:
  Rule 1 — Brute Force Login Detection        (MITRE: T1110)
  Rule 2 — Privilege Escalation Detection     (MITRE: T1078)
  Rule 3 — Port Scan / Reconnaissance         (MITRE: T1046)
"""

import time
import uuid
from datetime import datetime, timezone
from collections import defaultdict

# ── Alert store ──────────────────────────────────────────────────────────────
alerts   = []   # all fired alerts
incidents = []  # grouped incidents

# ── Rule state (sliding window counters) ─────────────────────────────────────
_failed_logins  = defaultdict(list)   # user -> [timestamps]
_port_hits      = defaultdict(list)   # src_ip -> [dst_ports]
_role_events    = []                  # privilege escalation events

# ── Thresholds (matching Sentinel rule defaults) ──────────────────────────────
BRUTE_FORCE_THRESHOLD   = 5    # failed logins
BRUTE_FORCE_WINDOW_SEC  = 300  # 5 minutes
PORT_SCAN_THRESHOLD     = 15   # unique ports
PORT_SCAN_WINDOW_SEC    = 60   # 1 minute


def _now():
    return time.time()

def _ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def _make_alert(rule_name, severity, description, entities, mitre_tactic, mitre_technique):
    alert = {
        "AlertId"       : str(uuid.uuid4())[:8].upper(),
        "TimeGenerated" : _ts(),
        "RuleName"      : rule_name,
        "Severity"      : severity,
        "Description"   : description,
        "Entities"      : entities,
        "MitreTactic"   : mitre_tactic,
        "MitreTechnique": mitre_technique,
        "Status"        : "New",
        "MTTD_seconds"  : None,   # filled by attack simulator
    }
    alerts.append(alert)
    incidents.append(alert)
    return alert


# ── Rule 1: Brute Force Login Detection ──────────────────────────────────────
# KQL equivalent:
#   SigninLogs
#   | where ResultType != "0"
#   | summarize FailCount = count() by UserPrincipalName, bin(TimeGenerated, 5m)
#   | where FailCount >= 5

def check_brute_force(log: dict):
    if log.get("TableName") != "SigninLogs":
        return None
    if log.get("ResultType") == "0":
        return None                          # successful login — skip

    user = log["UserPrincipalName"]
    ip   = log["IPAddress"]
    now  = _now()

    # Slide the window — keep only events within last 5 minutes
    _failed_logins[user] = [
        t for t in _failed_logins[user]
        if now - t < BRUTE_FORCE_WINDOW_SEC
    ]
    _failed_logins[user].append(now)

    count = len(_failed_logins[user])

    if count >= BRUTE_FORCE_THRESHOLD:
        _failed_logins[user] = []   # reset after alert fires
        return _make_alert(
            rule_name       = "Brute Force Login Attack Detected",
            severity        = "HIGH",
            description     = (
                f"{count} failed login attempts detected for user "
                f"'{user}' from IP {ip} within 5 minutes. "
                f"Possible credential stuffing or password spray attack."
            ),
            entities        = {"User": user, "SourceIP": ip, "FailedAttempts": count},
            mitre_tactic    = "Credential Access",
            mitre_technique = "T1110 — Brute Force",
        )
    return None


# ── Rule 2: Privilege Escalation Detection ───────────────────────────────────
# KQL equivalent:
#   AzureActivity
#   | where OperationName contains "roleAssignments/write"
#   | where ActivityStatus == "Succeeded"
#   | project TimeGenerated, Caller, OperationName, ResourceGroup

def check_privilege_escalation(log: dict):
    if log.get("TableName") != "AzureActivity":
        return None

    op     = log.get("OperationName", "")
    status = log.get("ActivityStatus", "")
    caller = log.get("Caller", "unknown")

    if "roleAssignments/write" in op and status == "Succeeded":
        return _make_alert(
            rule_name       = "Privilege Escalation — Admin Role Assigned",
            severity        = "HIGH",
            description     = (
                f"A privileged role assignment was detected. "
                f"User '{caller}' performed operation '{op}' on resource group "
                f"'{log.get('ResourceGroup', 'unknown')}'. "
                f"Verify this change was authorized."
            ),
            entities        = {
                "Caller"       : caller,
                "Operation"    : op,
                "ResourceGroup": log.get("ResourceGroup", "unknown"),
            },
            mitre_tactic    = "Privilege Escalation",
            mitre_technique = "T1078 — Valid Accounts",
        )
    return None


# ── Rule 3: Port Scan / Reconnaissance Detection ─────────────────────────────
# KQL equivalent:
#   NetworkFlow
#   | where Action == "Allow"
#   | summarize UniquePortsHit = dcount(DstPort) by SrcIP, bin(TimeGenerated, 1m)
#   | where UniquePortsHit >= 15

def check_port_scan(log: dict):
    if log.get("TableName") != "NetworkFlow":
        return None

    src_ip   = log["SrcIP"]
    dst_port = log["DstPort"]
    now      = _now()

    # Slide the window — keep hits within last 60 seconds
    _port_hits[src_ip] = [
        (t, p) for t, p in _port_hits[src_ip]
        if now - t < PORT_SCAN_WINDOW_SEC
    ]
    _port_hits[src_ip].append((now, dst_port))

    unique_ports = len(set(p for _, p in _port_hits[src_ip]))

    if unique_ports >= PORT_SCAN_THRESHOLD:
        ports_list = sorted(set(p for _, p in _port_hits[src_ip]))
        _port_hits[src_ip] = []   # reset after alert fires
        return _make_alert(
            rule_name       = "Port Scan / Network Reconnaissance Detected",
            severity        = "MEDIUM",
            description     = (
                f"Source IP {src_ip} has probed {unique_ports} unique ports "
                f"within 60 seconds. Ports targeted: {ports_list[:10]}... "
                f"Possible automated reconnaissance or vulnerability scan."
            ),
            entities        = {
                "SourceIP"   : src_ip,
                "UniquePortsHit": unique_ports,
                "PortsSample": ports_list[:10],
            },
            mitre_tactic    = "Discovery",
            mitre_technique = "T1046 — Network Service Discovery",
        )
    return None


# ── Master detection pipeline ─────────────────────────────────────────────────

RULES = [check_brute_force, check_privilege_escalation, check_port_scan]

def process_log(log: dict):
    """Run all rules against a single log entry. Returns list of alerts fired."""
    fired = []
    for rule in RULES:
        try:
            result = rule(log)
            if result:
                fired.append(result)
        except Exception as e:
            pass
    return fired

def get_all_alerts():
    return list(reversed(alerts))

def get_alert_counts():
    return {
        "total"  : len(alerts),
        "high"   : sum(1 for a in alerts if a["Severity"] == "HIGH"),
        "medium" : sum(1 for a in alerts if a["Severity"] == "MEDIUM"),
        "low"    : sum(1 for a in alerts if a["Severity"] == "LOW"),
    }
