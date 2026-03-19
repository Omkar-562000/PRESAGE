"""
Presage SIEM Project
Log Generator — simulates real security events
Mirrors Microsoft Sentinel log table structures:
  SigninLogs, SecurityEvent, AzureActivity, NetworkAnalytics
"""

import random
import time
import json
import threading
from datetime import datetime, timezone
from faker import Faker

fake = Faker()

# ── Realistic test data ──────────────────────────────────────────────────────
USERS = [
    "alice.johnson@wissenlab.com",
    "bob.sharma@wissenlab.com",
    "carol.mehta@wissenlab.com",
    "david.kumar@wissenlab.com",
    "admin@wissenlab.com",
]

MACHINES = ["WIN-SRV-01", "WIN-WKS-42", "LINUX-DB-03", "WIN-DC-01", "WIN-SRV-02"]

KNOWN_IPS   = ["192.168.1." + str(i) for i in range(10, 30)]
EXTERNAL_IPS = [fake.ipv4_public() for _ in range(20)]
MALICIOUS_IPS = ["45.33.32.156", "198.20.70.114", "104.21.14.101",
                  "185.220.101.55", "23.129.64.190"]

ADMIN_ROLES = ["Global Administrator", "Security Administrator",
               "User Access Administrator", "Privileged Role Administrator"]

PORTS = list(range(1, 1025))
COMMON_PORTS = [22, 23, 25, 53, 80, 110, 135, 139, 143,
                443, 445, 1433, 3306, 3389, 5985, 8080]

# ── Shared live log bus ───────────────────────────────────────────────────────
live_logs   = []          # all events in memory
_lock       = threading.Lock()
_callbacks  = []          # registered listeners


def register_callback(fn):
    _callbacks.append(fn)


def _emit(event: dict):
    with _lock:
        live_logs.append(event)
        if len(live_logs) > 5000:
            live_logs.pop(0)
    for fn in _callbacks:
        try:
            fn(event)
        except Exception:
            pass


# ── Event builders ────────────────────────────────────────────────────────────
def make_signin(user=None, success=True, ip=None):
    user = user or random.choice(USERS)
    ip   = ip   or random.choice(KNOWN_IPS + EXTERNAL_IPS)
    return {
        "table":       "SigninLogs",
        "TimeGenerated": datetime.now(timezone.utc).isoformat(),
        "UserPrincipalName": user,
        "IPAddress":   ip,
        "Location":    fake.city() + ", " + fake.country_code(),
        "ResultType":  "0" if success else str(random.choice([50126, 50053, 70011])),
        "ResultDescription": "Success" if success else "Invalid credentials",
        "AppDisplayName": random.choice(["Microsoft Teams", "Office 365",
                                         "Azure Portal", "SharePoint"]),
        "DeviceDetail": {"operatingSystem": random.choice(
            ["Windows 10", "Windows 11", "Ubuntu 22.04", "macOS 13"])},
        "RiskLevel":   "none" if success else random.choice(["low", "medium", "high"]),
    }


def make_security_event(machine=None, event_id=4625, user=None):
    machine = machine or random.choice(MACHINES)
    user    = user    or random.choice(USERS)
    descriptions = {
        4625: "An account failed to log on",
        4720: "A user account was created",
        4732: "A member was added to a security-enabled local group",
        4728: "A member was added to a security-enabled global group",
        4756: "A member was added to a security-enabled universal group",
        4738: "A user account was changed",
        4648: "A logon was attempted using explicit credentials",
    }
    return {
        "table":       "SecurityEvent",
        "TimeGenerated": datetime.now(timezone.utc).isoformat(),
        "Computer":    machine,
        "EventID":     event_id,
        "Activity":    descriptions.get(event_id, "Security event"),
        "Account":     user,
        "IpAddress":   random.choice(KNOWN_IPS),
        "LogonType":   random.choice([2, 3, 10]),
        "Status":      "0xC000006D" if event_id == 4625 else "0x0",
    }


def make_admin_assignment(user=None, role=None, assigned_by=None):
    return {
        "table":       "AuditLogs",
        "TimeGenerated": datetime.now(timezone.utc).isoformat(),
        "OperationName": "Add member to role",
        "TargetResources": [{"userPrincipalName": user or random.choice(USERS)}],
        "InitiatedBy": {"user": {"userPrincipalName":
                                  assigned_by or random.choice(USERS)}},
        "RoleAssigned": role or random.choice(ADMIN_ROLES),
        "Result":      "success",
        "Category":    "RoleManagement",
    }


def make_network_event(src_ip=None, dst_port=None):
    return {
        "table":       "NetworkAnalytics",
        "TimeGenerated": datetime.now(timezone.utc).isoformat(),
        "SrcIP":       src_ip or random.choice(EXTERNAL_IPS),
        "DstIP":       random.choice(KNOWN_IPS),
        "DstPort":     dst_port or random.choice(PORTS),
        "Protocol":    random.choice(["TCP", "UDP"]),
        "BytesSent":   random.randint(40, 1500),
        "Action":      random.choice(["Allow", "Allow", "Allow", "Deny"]),
    }


# ── Background normal traffic ─────────────────────────────────────────────────
def _normal_traffic_loop():
    """Continuously emits benign background events so logs look real."""
    while True:
        roll = random.random()
        if roll < 0.50:
            _emit(make_signin(success=True))
        elif roll < 0.70:
            _emit(make_security_event(event_id=4648))
        elif roll < 0.85:
            _emit(make_network_event())
        else:
            _emit(make_security_event(
                event_id=random.choice([4720, 4738])))
        time.sleep(random.uniform(0.4, 1.2))


def start_normal_traffic():
    t = threading.Thread(target=_normal_traffic_loop, daemon=True)
    t.start()


# ── Attack injectors ──────────────────────────────────────────────────────────
def inject_brute_force(user=None, attacker_ip=None, count=10):
    """Fire rapid failed logins — triggers Rule 1."""
    user        = user        or random.choice(USERS)
    attacker_ip = attacker_ip or random.choice(MALICIOUS_IPS)
    print(f"\n[ATTACK] Injecting brute-force: {count} failed logins "
          f"from {attacker_ip} against {user}")
    for _ in range(count):
        _emit(make_signin(user=user, success=False, ip=attacker_ip))
        time.sleep(0.05)


def inject_privilege_escalation(user=None, role=None):
    """Assign admin role to user — triggers Rule 2."""
    user = user or random.choice([u for u in USERS if "admin" not in u])
    role = role or "Global Administrator"
    print(f"\n[ATTACK] Injecting privilege escalation: "
          f"{user} → {role}")
    _emit(make_admin_assignment(user=user, role=role))


def inject_port_scan(attacker_ip=None, port_count=25):
    """Hit many ports from one IP — triggers Rule 3."""
    attacker_ip = attacker_ip or random.choice(MALICIOUS_IPS)
    ports = random.sample(PORTS, port_count)
    print(f"\n[ATTACK] Injecting port scan: {port_count} ports "
          f"from {attacker_ip}")
    for port in ports:
        _emit(make_network_event(src_ip=attacker_ip, dst_port=port))
        time.sleep(0.02)


