"""
=============================================================
WISSEN INFOTECH — LOCAL SIEM ENGINE
Project: SIEM Configuration & Real-Time Threat Detection
Platform: Local Python (mirrors Microsoft Sentinel architecture)
Author: Team Wissen
Date: March 2026
=============================================================

ARCHITECTURE NOTE:
This engine mirrors Microsoft Sentinel's core components:
  Log Analytics Workspace  →  LogStore (in-memory + file)
  Data Connectors          →  LogGenerator (simulates sources)
  Analytics Rules (KQL)    →  DetectionEngine (Python rules)
  Automation Playbooks     →  PlaybookEngine (auto response)
  Incidents Queue          →  IncidentManager
=============================================================
"""

import time
import json
import random
import threading
import os
from datetime import datetime, timedelta
from collections import defaultdict

# ─────────────────────────────────────────────
# COLOUR OUTPUT (terminal colors for demo)
# ─────────────────────────────────────────────
class Color:
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN    = '\033[96m'
    WHITE   = '\033[97m'
    BOLD    = '\033[1m'
    RESET   = '\033[0m'

def banner():
    print(f"""
{Color.CYAN}{Color.BOLD}
╔══════════════════════════════════════════════════════════════╗
║          WISSEN INFOTECH — LOCAL SIEM ENGINE v1.0           ║
║     Real-Time Threat Detection & Automated Response         ║
║     Mirrors: Microsoft Sentinel + IBM QRadar Architecture   ║
╚══════════════════════════════════════════════════════════════╝
{Color.RESET}""")

# ─────────────────────────────────────────────
# LOG STORE (mirrors Log Analytics Workspace)
# ─────────────────────────────────────────────
class LogStore:
    """
    Central log storage — equivalent to Log Analytics Workspace.
    Tables mirror Sentinel's actual table names:
      SigninLogs      → Azure AD / Entra ID login events
      SecurityEvent   → Windows Security events
      NetworkEvent    → Network traffic and connection logs
      AzureActivity   → Resource management events
    """
    def __init__(self):
        self.tables = {
            "SigninLogs":    [],
            "SecurityEvent": [],
            "NetworkEvent":  [],
            "AzureActivity": []
        }
        self.lock = threading.Lock()
        os.makedirs("logs", exist_ok=True)

    def insert(self, table, record):
        """Insert a log record into the appropriate table."""
        record["TimeGenerated"] = datetime.now().isoformat()
        record["_table"] = table
        with self.lock:
            self.tables[table].append(record)
        # Write to file (persistent log)
        with open(f"logs/{table}.jsonl", "a") as f:
            f.write(json.dumps(record) + "\n")
        return record

    def query(self, table, window_seconds=300):
        """
        Query a table for records within the time window.
        Equivalent to KQL: TableName | where TimeGenerated > ago(5m)
        """
        cutoff = datetime.now() - timedelta(seconds=window_seconds)
        with self.lock:
            return [
                r for r in self.tables[table]
                if datetime.fromisoformat(r["TimeGenerated"]) > cutoff
            ]

    def count(self):
        """Return total log count across all tables."""
        return {t: len(v) for t, v in self.tables.items()}


# ─────────────────────────────────────────────
# LOG GENERATOR (mirrors Data Connectors)
# ─────────────────────────────────────────────
class LogGenerator:
    """
    Simulates security events from multiple data sources.
    Each method = one Data Connector in Microsoft Sentinel.
    """
    USERS   = ["alice", "bob", "charlie", "david", "admin", "svc_account"]
    IPS     = ["192.168.1.10", "192.168.1.25", "10.0.0.5",
               "203.0.113.42", "198.51.100.7", "172.16.0.99"]
    DEVICES = ["DESKTOP-WKS01", "LAPTOP-DEV02", "SERVER-PROD01",
               "VM-TEST01", "WORKSTATION-HR"]

    def __init__(self, store: LogStore):
        self.store = store

    def normal_login(self):
        """Simulate a successful login — normal baseline traffic."""
        return self.store.insert("SigninLogs", {
            "EventType":      "UserLogin",
            "ResultType":     "Success",
            "UserPrincipalName": random.choice(self.USERS) + "@wissen.com",
            "IPAddress":      random.choice(self.IPS[:3]),
            "Location":       random.choice(["Mumbai", "Pune", "Bangalore"]),
            "DeviceName":     random.choice(self.DEVICES),
            "RiskLevel":      "None"
        })

    def failed_login(self, user=None, ip=None):
        """
        Simulate a failed login attempt.
        Used in: Brute Force Attack simulation (Rule 1).
        """
        return self.store.insert("SigninLogs", {
            "EventType":      "UserLogin",
            "ResultType":     "Failure",
            "ResultDescription": "Invalid password",
            "UserPrincipalName": (user or random.choice(self.USERS)) + "@wissen.com",
            "IPAddress":      ip or random.choice(self.IPS[3:]),
            "Location":       "Unknown",
            "DeviceName":     "UNKNOWN-DEVICE",
            "RiskLevel":      "High"
        })

    def privilege_escalation(self, user=None):
        """
        Simulate admin role assignment to a user.
        Used in: Privilege Escalation simulation (Rule 2).
        """
        target = user or random.choice(self.USERS[:4])
        self.store.insert("AzureActivity", {
            "OperationName":  "Microsoft.Authorization/roleAssignments/write",
            "ActivityStatus": "Succeeded",
            "Caller":         "svc_account@wissen.com",
            "TargetUser":     target + "@wissen.com",
            "RoleAssigned":   "Global Administrator",
            "ResourceGroup":  "wissen-prod-rg",
            "Severity":       "Critical"
        })
        return self.store.insert("SecurityEvent", {
            "EventID":        4728,
            "EventType":      "GroupMembershipChange",
            "Description":    "User added to privileged group",
            "TargetUser":     target + "@wissen.com",
            "GroupName":      "Domain Admins",
            "SubjectAccount": "svc_account@wissen.com",
            "Severity":       "Critical"
        })

    def port_scan(self, source_ip=None):
        """
        Simulate rapid port scanning from an external IP.
        Used in: Port Scan / Reconnaissance simulation (Rule 3).
        """
        src = source_ip or "203.0.113.42"
        ports = random.sample(range(1, 65535), 25)
        records = []
        for port in ports:
            r = self.store.insert("NetworkEvent", {
                "EventType":      "ConnectionAttempt",
                "SourceIP":       src,
                "DestinationIP":  "10.0.0.5",
                "DestinationPort": port,
                "Protocol":       "TCP",
                "Action":         "Blocked",
                "BytesSent":      0,
                "Severity":       "Medium"
            })
            records.append(r)
        return records

    def normal_network(self):
        """Simulate normal network traffic — baseline noise."""
        return self.store.insert("NetworkEvent", {
            "EventType":      "Connection",
            "SourceIP":       random.choice(self.IPS[:3]),
            "DestinationIP":  random.choice(self.IPS[:3]),
            "DestinationPort": random.choice([80, 443, 8080, 3389]),
            "Protocol":       "TCP",
            "Action":         "Allowed",
            "BytesSent":      random.randint(500, 50000)
        })

    def generate_baseline(self, count=20):
        """Generate baseline normal traffic for realistic demo context."""
        for _ in range(count):
            r = random.random()
            if r < 0.5:
                self.normal_login()
            elif r < 0.8:
                self.normal_network()
            else:
                self.failed_login()  # occasional single failure = normal


# ─────────────────────────────────────────────
# INCIDENT MANAGER
# ─────────────────────────────────────────────
class IncidentManager:
    """Manages all detected incidents — mirrors Sentinel's Incidents queue."""
    def __init__(self):
        self.incidents = []
        self.counter   = 1

    def create(self, title, severity, rule, evidence, mttd):
        incident = {
            "IncidentID":    f"INC-{self.counter:04d}",
            "Title":         title,
            "Severity":      severity,
            "Status":        "New",
            "DetectionRule": rule,
            "MITRETactic":   self._mitre(rule),
            "Evidence":      evidence,
            "MTTD_seconds":  round(mttd, 2),
            "CreatedTime":   datetime.now().isoformat(),
            "PlaybookRan":   False,
            "Response":      None
        }
        self.incidents.append(incident)
        self.counter += 1
        return incident

    def _mitre(self, rule):
        mapping = {
            "BruteForce":          "TA0006 — Credential Access",
            "PrivilegeEscalation": "TA0004 — Privilege Escalation",
            "PortScan":            "TA0043 — Reconnaissance"
        }
        return mapping.get(rule, "Unknown")

    def get_all(self):
        return self.incidents


# ─────────────────────────────────────────────
# PLAYBOOK ENGINE (mirrors Logic Apps)
# ─────────────────────────────────────────────
class PlaybookEngine:
    """
    Automated response — mirrors Azure Logic App Playbooks.
    Triggers automatically on High/Critical severity incidents.
    """
    def __init__(self):
        os.makedirs("reports", exist_ok=True)

    def run(self, incident):
        """Execute automated response actions for an incident."""
        actions_taken = []
        t_start = time.time()

        # Action 1: Send alert notification (simulates Teams/Email)
        self._notify(incident)
        actions_taken.append("Alert notification sent (Teams/Email)")

        # Action 2: Tag incident
        incident["Status"] = "Under Investigation"
        actions_taken.append("Incident tagged: Under Investigation")

        # Action 3: Block IP if brute force
        if incident["DetectionRule"] == "BruteForce":
            ip = incident["Evidence"].get("SourceIP", "Unknown")
            self._block_ip(ip)
            actions_taken.append(f"IP blocked: {ip}")

        # Action 4: Revoke session if privilege escalation
        if incident["DetectionRule"] == "PrivilegeEscalation":
            user = incident["Evidence"].get("TargetUser", "Unknown")
            self._revoke_session(user)
            actions_taken.append(f"Session revoked: {user}")

        mttr = round(time.time() - t_start, 3)
        incident["PlaybookRan"] = True
        incident["Response"]    = {
            "ActionsTaken": actions_taken,
            "MTTR_seconds": mttr,
            "ResponseTime": datetime.now().isoformat()
        }
        return actions_taken, mttr

    def _notify(self, incident):
        print(f"\n  {Color.BLUE}[PLAYBOOK]{Color.RESET} Sending alert notification...")
        print(f"  {Color.BLUE}[PLAYBOOK]{Color.RESET} To: soc-team@wissen.com | Teams: #security-alerts")
        print(f"  {Color.BLUE}[PLAYBOOK]{Color.RESET} Subject: [{incident['Severity']}] {incident['Title']}")

    def _block_ip(self, ip):
        print(f"  {Color.BLUE}[PLAYBOOK]{Color.RESET} Firewall rule added — blocking IP: {ip}")

    def _revoke_session(self, user):
        print(f"  {Color.BLUE}[PLAYBOOK]{Color.RESET} Session revoked for user: {user}")


# ─────────────────────────────────────────────
# DETECTION ENGINE (mirrors KQL Analytics Rules)
# ─────────────────────────────────────────────
class DetectionEngine:
    """
    Core detection logic — equivalent to KQL Scheduled Analytics Rules.
    Each method = one detection rule in Microsoft Sentinel.

    KQL Equivalent Comments included for documentation.
    """
    def __init__(self, store: LogStore, incidents: IncidentManager,
                 playbook: PlaybookEngine):
        self.store    = store
        self.incidents = incidents
        self.playbook  = playbook
        self.fired    = set()   # prevent duplicate alerts

    # ── RULE 1: BRUTE FORCE DETECTION ──────────────────────────
    def rule_brute_force(self, attack_start_time=None):
        """
        KQL Equivalent:
        SigninLogs
        | where TimeGenerated > ago(5m)
        | where ResultType == "Failure"
        | summarize FailCount = count() by IPAddress, UserPrincipalName
        | where FailCount >= 5
        | extend Severity = "High"

        Threshold: 5+ failed logins from same IP in 5 minutes.
        MITRE ATT&CK: T1110 — Brute Force (TA0006 Credential Access)
        """
        logs    = self.store.query("SigninLogs", window_seconds=300)
        fails   = [l for l in logs if l.get("ResultType") == "Failure"]
        by_ip   = defaultdict(list)
        for l in fails:
            by_ip[l.get("IPAddress", "")].append(l)

        for ip, events in by_ip.items():
            key = f"brute_{ip}"
            if len(events) >= 5 and key not in self.fired:
                self.fired.add(key)
                mttd = time.time() - attack_start_time if attack_start_time else 0
                users = list({e.get("UserPrincipalName","") for e in events})
                inc = self.incidents.create(
                    title    = f"Brute Force Attack Detected — {ip}",
                    severity = "High",
                    rule     = "BruteForce",
                    evidence = {
                        "SourceIP":         ip,
                        "FailedAttempts":   len(events),
                        "TargetUsers":      users,
                        "TimeWindowMins":   5,
                        "FirstAttempt":     events[0]["TimeGenerated"],
                        "LastAttempt":      events[-1]["TimeGenerated"]
                    },
                    mttd = mttd
                )
                return inc
        return None

    # ── RULE 2: PRIVILEGE ESCALATION ───────────────────────────
    def rule_privilege_escalation(self, attack_start_time=None):
        """
        KQL Equivalent:
        SecurityEvent
        | where TimeGenerated > ago(5m)
        | where EventID == 4728
        | where GroupName contains "Admin"
        | join kind=inner AzureActivity on $left.TargetUser == $right.TargetUser
        | where RoleAssigned contains "Administrator"
        | extend Severity = "Critical"

        Threshold: Any admin role assignment = immediate alert.
        MITRE ATT&CK: T1078 — Valid Accounts (TA0004 Privilege Escalation)
        """
        sec_logs = self.store.query("SecurityEvent", window_seconds=300)
        az_logs  = self.store.query("AzureActivity", window_seconds=300)

        priv_events = [
            l for l in sec_logs
            if l.get("EventID") == 4728
            and "Admin" in l.get("GroupName", "")
        ]
        role_events = [
            l for l in az_logs
            if "Administrator" in l.get("RoleAssigned", "")
        ]

        for event in priv_events:
            key = f"priv_{event.get('TargetUser','')}"
            if key not in self.fired:
                self.fired.add(key)
                mttd = time.time() - attack_start_time if attack_start_time else 0
                role_info = role_events[-1] if role_events else {}
                inc = self.incidents.create(
                    title    = f"Privilege Escalation — {event.get('TargetUser','')}",
                    severity = "Critical",
                    rule     = "PrivilegeEscalation",
                    evidence = {
                        "TargetUser":     event.get("TargetUser", ""),
                        "GroupAssigned":  event.get("GroupName", ""),
                        "RoleAssigned":   role_info.get("RoleAssigned", "Global Administrator"),
                        "PerformedBy":    event.get("SubjectAccount", ""),
                        "EventID":        4728,
                        "EventTime":      event["TimeGenerated"]
                    },
                    mttd = mttd
                )
                return inc
        return None

    # ── RULE 3: PORT SCAN / RECONNAISSANCE ─────────────────────
    def rule_port_scan(self, attack_start_time=None):
        """
        KQL Equivalent:
        NetworkEvent
        | where TimeGenerated > ago(1m)
        | where Action == "Blocked"
        | summarize PortCount = dcount(DestinationPort) by SourceIP
        | where PortCount >= 20
        | extend Severity = "Medium"

        Threshold: 20+ unique ports from same IP in 1 minute.
        MITRE ATT&CK: T1046 — Network Service Discovery (TA0043 Reconnaissance)
        """
        logs    = self.store.query("NetworkEvent", window_seconds=60)
        blocked = [l for l in logs if l.get("Action") == "Blocked"]
        by_ip   = defaultdict(set)
        for l in blocked:
            by_ip[l.get("SourceIP","")].add(l.get("DestinationPort", 0))

        for ip, ports in by_ip.items():
            key = f"scan_{ip}"
            if len(ports) >= 20 and key not in self.fired:
                self.fired.add(key)
                mttd = time.time() - attack_start_time if attack_start_time else 0
                inc = self.incidents.create(
                    title    = f"Port Scan / Reconnaissance Detected — {ip}",
                    severity = "Medium",
                    rule     = "PortScan",
                    evidence = {
                        "SourceIP":        ip,
                        "PortsScanned":    len(ports),
                        "TargetIP":        "10.0.0.5",
                        "SamplePorts":     sorted(list(ports))[:10],
                        "TimeWindowSecs":  60,
                        "Protocol":        "TCP"
                    },
                    mttd = mttd
                )
                return inc
        return None

    def run_all_rules(self, attack_times={}):
        """Run all three detection rules and return any new incidents."""
        results = []
        for rule_fn, name in [
            (self.rule_brute_force,          "BruteForce"),
            (self.rule_privilege_escalation, "PrivilegeEscalation"),
            (self.rule_port_scan,            "PortScan")
        ]:
            inc = rule_fn(attack_times.get(name))
            if inc:
                results.append(inc)
        return results
