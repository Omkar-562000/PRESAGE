"""
Wissen Infotech SIEM Project
Attack Simulator — fires controlled simulated attacks
Measures MTTD (Mean Time to Detect) precisely

Attacks:
  1. Brute Force Login
  2. Privilege Escalation
  3. Port Scan
"""

import time
import json
from datetime import datetime, timezone
from src.log_generator import signin_log, azure_activity, network_flow, EXTERNAL_IPS
from src.detection_engine import process_log, alerts

ATTACKER_IP = "185.220.101.34"
TARGET_USER = "admin@wissen-client.com"

def _ts():
    return datetime.now(timezone.utc).strftime("%H:%M:%S")

def _banner(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")


# ── Attack 1: Brute Force ─────────────────────────────────────────────────────

def simulate_brute_force(on_alert=None):
    _banner("ATTACK 1 — Brute Force Login (T1110)")
    print(f"  Target user : {TARGET_USER}")
    print(f"  Attacker IP : {ATTACKER_IP}")
    print(f"  Method      : 10 failed login attempts\n")

    attack_start = time.time()
    alert_fired  = None

    for i in range(1, 11):
        log = signin_log(
            user     = TARGET_USER,
            success  = False,
            ip       = ATTACKER_IP,
            location = "Moscow, Russia"
        )
        fired = process_log(log)
        print(f"  [{_ts()}] Failed login attempt #{i} — ResultType: {log['ResultType']}")

        if fired and not alert_fired:
            mttd = round(time.time() - attack_start, 2)
            alert_fired = fired[0]
            alert_fired["MTTD_seconds"] = mttd
            print(f"\n  🚨 ALERT FIRED at attempt #{i}")
            print(f"  ⏱  MTTD: {mttd} seconds")
            if on_alert:
                on_alert(alert_fired)

        time.sleep(0.3)

    return {
        "attack"      : "Brute Force Login",
        "mitre"       : "T1110",
        "alert_fired" : alert_fired is not None,
        "mttd_seconds": alert_fired["MTTD_seconds"] if alert_fired else None,
        "alert"       : alert_fired,
    }


# ── Attack 2: Privilege Escalation ───────────────────────────────────────────

def simulate_privilege_escalation(on_alert=None):
    _banner("ATTACK 2 — Privilege Escalation (T1078)")
    print(f"  Attacker    : {TARGET_USER}")
    print(f"  Method      : Assign Global Admin role via Azure API\n")

    attack_start = time.time()

    log = azure_activity(
        user      = TARGET_USER,
        operation = "Microsoft.Authorization/roleAssignments/write",
        status    = "Succeeded"
    )

    print(f"  [{_ts()}] Role assignment operation executed")
    print(f"  Operation : {log['OperationName']}")
    print(f"  Status    : {log['ActivityStatus']}")

    fired = process_log(log)
    alert_fired = None

    if fired:
        mttd = round(time.time() - attack_start, 2)
        alert_fired = fired[0]
        alert_fired["MTTD_seconds"] = mttd
        print(f"\n  🚨 ALERT FIRED immediately")
        print(f"  ⏱  MTTD: {mttd} seconds")
        if on_alert:
            on_alert(alert_fired)

    return {
        "attack"      : "Privilege Escalation",
        "mitre"       : "T1078",
        "alert_fired" : alert_fired is not None,
        "mttd_seconds": alert_fired["MTTD_seconds"] if alert_fired else None,
        "alert"       : alert_fired,
    }


# ── Attack 3: Port Scan ───────────────────────────────────────────────────────

def simulate_port_scan(on_alert=None):
    _banner("ATTACK 3 — Port Scan / Reconnaissance (T1046)")
    print(f"  Attacker IP : {ATTACKER_IP}")
    print(f"  Method      : Nmap-style sweep across 20 ports\n")

    attack_start = time.time()
    alert_fired  = None

    ports_to_scan = [21,22,23,25,53,80,110,135,139,143,
                     443,445,3306,3389,5432,5900,6379,8080,8443,9200]

    for port in ports_to_scan:
        log = network_flow(src_ip=ATTACKER_IP, dst_port=port)
        fired = process_log(log)
        print(f"  [{_ts()}] Probe → port {str(port).ljust(5)}  [{log['Action']}]")

        if fired and not alert_fired:
            mttd = round(time.time() - attack_start, 2)
            alert_fired = fired[0]
            alert_fired["MTTD_seconds"] = mttd
            print(f"\n  🚨 ALERT FIRED after {port} port hits")
            print(f"  ⏱  MTTD: {mttd} seconds")
            if on_alert:
                on_alert(alert_fired)

        time.sleep(0.15)

    return {
        "attack"      : "Port Scan",
        "mitre"       : "T1046",
        "alert_fired" : alert_fired is not None,
        "mttd_seconds": alert_fired["MTTD_seconds"] if alert_fired else None,
        "alert"       : alert_fired,
    }


# ── Full attack suite ─────────────────────────────────────────────────────────

def run_all_attacks(on_alert=None):
    results = []
    results.append(simulate_brute_force(on_alert))
    time.sleep(1)
    results.append(simulate_privilege_escalation(on_alert))
    time.sleep(1)
    results.append(simulate_port_scan(on_alert))
    return results
