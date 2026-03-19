from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIST_DIR = BASE_DIR / "frontend" / "dist"
STATIC_ASSETS_DIR = FRONTEND_DIST_DIR / "assets"

SIEM_RULES = [
    {
        "id": "brute_force",
        "title": "Brute Force Login Attack Detected",
        "severity": "High",
        "mitre": "TA0006 / T1110",
        "table": "SigninLogs",
        "threshold": "5 failed logins in 5 minutes",
    },
    {
        "id": "privilege_escalation",
        "title": "Privilege Escalation - Admin Role Assigned",
        "severity": "High",
        "mitre": "TA0004 / T1078",
        "table": "AzureActivity",
        "threshold": "Immediate on role assignment",
    },
    {
        "id": "port_scan",
        "title": "Port Scan / Network Reconnaissance Detected",
        "severity": "Medium",
        "mitre": "TA0043 / T1046",
        "table": "NetworkEvents",
        "threshold": "20 unique ports in 60 seconds",
    },
    {
        "id": "windows_failed_logon",
        "title": "Windows Failed Logon Burst Detected",
        "severity": "High",
        "mitre": "TA0006 / T1110",
        "table": "WindowsEvent",
        "threshold": "5 failed Windows logons in 5 minutes",
    },
]
