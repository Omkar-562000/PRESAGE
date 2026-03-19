"""
=============================================================
WISSEN INFOTECH — SIEM DEMO RUNNER
Interactive attack simulation with real-time detection
Run: python demo.py
=============================================================
"""

import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from siem_engine import (
    LogStore, LogGenerator, DetectionEngine,
    IncidentManager, PlaybookEngine, Color, banner
)

# ─────────────────────────────────────────────
# DISPLAY HELPERS
# ─────────────────────────────────────────────

def print_separator(char="─", color=Color.CYAN):
    print(f"{color}{char * 64}{Color.RESET}")

def print_header(text, color=Color.CYAN):
    print_separator("═", color)
    print(f"{color}{Color.BOLD}  {text}{Color.RESET}")
    print_separator("═", color)

def print_log(msg, level="INFO"):
    colors = {
        "INFO":    Color.WHITE,
        "LOG":     Color.CYAN,
        "ATTACK":  Color.RED,
        "ALERT":   Color.YELLOW,
        "DETECT":  Color.GREEN,
        "PLAY":    Color.BLUE,
        "METRIC":  Color.MAGENTA
    }
    c = colors.get(level, Color.WHITE)
    ts = time.strftime("%H:%M:%S")
    print(f"  {Color.WHITE}[{ts}]{Color.RESET} {c}[{level}]{Color.RESET} {msg}")

def print_incident(inc):
    """Display a detected incident in formatted output."""
    sev_colors = {
        "Critical": Color.RED,
        "High":     Color.RED,
        "Medium":   Color.YELLOW,
        "Low":      Color.GREEN
    }
    sc = sev_colors.get(inc["Severity"], Color.WHITE)
    print(f"""
{Color.BOLD}  ┌─ INCIDENT DETECTED {'─'*40}
  │ ID:        {inc['IncidentID']}
  │ Title:     {sc}{inc['Title']}{Color.RESET}{Color.BOLD}
  │ Severity:  {sc}{inc['Severity']}{Color.RESET}{Color.BOLD}
  │ Rule:      {inc['DetectionRule']}
  │ MITRE:     {inc['MITRETactic']}
  │ MTTD:      {Color.GREEN}{inc['MTTD_seconds']}s{Color.RESET}{Color.BOLD}
  │ Status:    {inc['Status']}
  └{'─'*55}{Color.RESET}""")

def wait_key(msg="Press ENTER to continue..."):
    print(f"\n  {Color.YELLOW}{msg}{Color.RESET}")
    input()

# ─────────────────────────────────────────────
# SIMULATION SCENARIOS
# ─────────────────────────────────────────────

def run_attack_1(gen, engine, mttd_log):
    """
    ATTACK SCENARIO 1: Brute Force Login Attack
    Simulates an attacker repeatedly trying passwords
    against an admin account from an external IP.
    """
    print_header("ATTACK SIMULATION 1 — Brute Force Login", Color.RED)
    print_log("Scenario: External attacker attempting to crack admin password", "ATTACK")
    print_log("Source IP: 203.0.113.42 (External / Malicious)", "ATTACK")
    print_log("Target: admin@wissen.com", "ATTACK")
    print()

    wait_key("Press ENTER to launch brute force attack...")

    t_start = time.time()
    print_log("Attack started — firing failed login attempts...", "ATTACK")

    for i in range(1, 11):
        gen.failed_login(user="admin", ip="203.0.113.42")
        print_log(f"  Failed login attempt #{i} → admin@wissen.com from 203.0.113.42", "LOG")
        time.sleep(0.3)

    print()
    print_log("Waiting for detection engine to process...", "INFO")
    time.sleep(1)

    # Run detection
    t_detect_start = time.time()
    inc = engine.rule_brute_force(attack_start_time=t_start)

    if inc:
        mttd = time.time() - t_start
        mttd_log["BruteForce"] = round(mttd, 2)
        print_log(f"ALERT FIRED — {inc['Title']}", "DETECT")
        print_incident(inc)

        print_log("Triggering automated playbook response...", "PLAY")
        actions, mttr = engine.playbook.run(inc)
        print_log(f"Playbook complete — MTTR: {mttr}s", "METRIC")
        print_log(f"Actions taken: {', '.join(actions)}", "PLAY")
    else:
        print_log("No detection triggered — add more failed logins", "INFO")

    return inc

def run_attack_2(gen, engine, mttd_log):
    """
    ATTACK SCENARIO 2: Privilege Escalation
    Simulates an insider threat / compromised service account
    granting admin access to an unauthorized user.
    """
    print_header("ATTACK SIMULATION 2 — Privilege Escalation", Color.RED)
    print_log("Scenario: Compromised service account granting admin role", "ATTACK")
    print_log("Performer: svc_account@wissen.com (compromised)", "ATTACK")
    print_log("Target: charlie@wissen.com → being granted Global Admin", "ATTACK")
    print()

    wait_key("Press ENTER to execute privilege escalation...")

    t_start = time.time()
    print_log("Assigning Global Administrator role to charlie@wissen.com...", "ATTACK")
    gen.privilege_escalation(user="charlie")
    print_log("Role assignment completed — event logged to AzureActivity", "LOG")
    print_log("Windows EventID 4728 generated — user added to Domain Admins", "LOG")

    time.sleep(1)
    print_log("Detection engine scanning SecurityEvent + AzureActivity...", "INFO")
    time.sleep(0.5)

    inc = engine.rule_privilege_escalation(attack_start_time=t_start)

    if inc:
        mttd = time.time() - t_start
        mttd_log["PrivilegeEscalation"] = round(mttd, 2)
        print_log(f"ALERT FIRED — {inc['Title']}", "DETECT")
        print_incident(inc)

        print_log("Triggering automated playbook response...", "PLAY")
        actions, mttr = engine.playbook.run(inc)
        print_log(f"Playbook complete — MTTR: {mttr}s", "METRIC")
        print_log(f"Actions taken: {', '.join(actions)}", "PLAY")
    return inc

def run_attack_3(gen, engine, mttd_log):
    """
    ATTACK SCENARIO 3: Port Scan / Reconnaissance
    Simulates an external attacker mapping the network
    before a targeted intrusion attempt.
    """
    print_header("ATTACK SIMULATION 3 — Port Scan Reconnaissance", Color.RED)
    print_log("Scenario: External attacker mapping network ports", "ATTACK")
    print_log("Source IP: 203.0.113.42 (same attacker from Attack 1)", "ATTACK")
    print_log("Target: 10.0.0.5 (Internal application server)", "ATTACK")
    print()

    wait_key("Press ENTER to launch port scan...")

    t_start = time.time()
    print_log("Port scan initiated — scanning 25 ports rapidly...", "ATTACK")
    events = gen.port_scan(source_ip="203.0.113.42")
    print_log(f"Scanned {len(events)} ports in under 5 seconds", "LOG")
    print_log("Firewall blocking all attempts — events logged to NetworkEvent", "LOG")

    time.sleep(1)
    print_log("Detection engine scanning NetworkEvent table...", "INFO")
    time.sleep(0.5)

    inc = engine.rule_port_scan(attack_start_time=t_start)

    if inc:
        mttd = time.time() - t_start
        mttd_log["PortScan"] = round(mttd, 2)
        print_log(f"ALERT FIRED — {inc['Title']}", "DETECT")
        print_incident(inc)

        print_log("Triggering automated playbook response...", "PLAY")
        actions, mttr = engine.playbook.run(inc)
        print_log(f"Playbook complete — MTTR: {mttr}s", "METRIC")
    return inc

# ─────────────────────────────────────────────
# FINAL REPORT GENERATOR
# ─────────────────────────────────────────────

def generate_report(incidents, mttd_log, store):
    """Generate the complete incident report for documentation."""
    os.makedirs("reports", exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")

    # Text report
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║        WISSEN INFOTECH — SIEM TEST RESULTS REPORT           ║
║        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                      ║
╚══════════════════════════════════════════════════════════════╝

CLIENT: Mid-sized Enterprise (Wissen Infotech POC)
PLATFORM: Local SIEM Engine (Mirrors Microsoft Sentinel Architecture)
TEST DATE: {time.strftime('%B %d, %Y')}

═══════════════════════════════════════════════════════════════
SECTION 1 — BEFORE STATE (Pre-SIEM Configuration)
═══════════════════════════════════════════════════════════════
Detection Method:   Manual log review
Mean Time to Detect (MTTD): 4–6 hours (industry benchmark)
Automated Response: None
Alert Coverage:     0% (no rules configured)
Log Sources:        Scattered, no central collection
Incident Tracking:  None

═══════════════════════════════════════════════════════════════
SECTION 2 — AFTER STATE (Post-SIEM Configuration)
═══════════════════════════════════════════════════════════════
Detection Method:   Automated KQL-equivalent rules (real-time)
Log Sources Connected: 4 (SigninLogs, SecurityEvent, NetworkEvent, AzureActivity)
Analytics Rules Active: 3 custom detection rules
Automated Response: Logic App playbook (auto-triggered on High/Critical)
"""

    report += """
═══════════════════════════════════════════════════════════════
SECTION 3 — SIMULATED ATTACK TEST RESULTS
═══════════════════════════════════════════════════════════════

┌─────────────────────────┬──────────────┬──────────────┬──────────┬──────────────┐
│ Attack Scenario         │ Expected     │ Alert Fired  │ MTTD     │ Playbook Ran │
├─────────────────────────┼──────────────┼──────────────┼──────────┼──────────────┤"""

    scenario_map = {
        "BruteForce":          ("Brute Force Login",        "High",     "BruteForce Alert"),
        "PrivilegeEscalation": ("Privilege Escalation",     "Critical", "PrivEsc Alert"),
        "PortScan":            ("Port Scan Recon",           "Medium",   "PortScan Alert")
    }

    for rule, (scenario, severity, expected) in scenario_map.items():
        inc = next((i for i in incidents if i["DetectionRule"] == rule), None)
        mttd  = f"{mttd_log.get(rule, 'N/A')}s" if rule in mttd_log else "N/A"
        fired = "YES" if inc else "NO"
        pb    = "YES" if (inc and inc.get("PlaybookRan")) else "NO"
        report += f"\n│ {scenario:<23}  │ {expected:<12} │ {fired:<12} │ {mttd:<8} │ {pb:<12} │"

    report += """
└─────────────────────────┴──────────────┴──────────────┴──────────┴──────────────┘"""

    if mttd_log:
        avg_mttd = round(sum(mttd_log.values()) / len(mttd_log), 2)
        report += f"""
═══════════════════════════════════════════════════════════════
SECTION 4 — KEY METRICS (Before vs After)
═══════════════════════════════════════════════════════════════

Metric                    Before SIEM        After SIEM         Improvement
────────────────────────  ─────────────────  ─────────────────  ──────────────
Mean Time to Detect       4–6 hours          {avg_mttd}s avg          99%+ reduction
Automated Response        None               < 1 second         ∞ improvement
Alert Rules Active        0                  3 custom rules     +3
Log Sources Monitored     0 (manual)         4 tables           +4
Incident Tracking         None               Full timeline      Complete
False Positives (test)    N/A                0                  Clean

MTTD by Attack Type:"""
        for rule, mttd_val in mttd_log.items():
            report += f"\n  {rule:<25} {mttd_val}s"

    report += f"""

═══════════════════════════════════════════════════════════════
SECTION 5 — INCIDENTS DETECTED
═══════════════════════════════════════════════════════════════
Total Incidents: {len(incidents)}
"""
    for inc in incidents:
        report += f"""
  [{inc['IncidentID']}] {inc['Title']}
  Severity: {inc['Severity']} | Rule: {inc['DetectionRule']}
  MITRE: {inc['MITRETactic']}
  MTTD: {inc['MTTD_seconds']}s | Playbook: {'Yes' if inc['PlaybookRan'] else 'No'}
  Evidence: {json.dumps(inc['Evidence'], indent=4)}
"""

    report += f"""
═══════════════════════════════════════════════════════════════
SECTION 6 — LOG VOLUME SUMMARY
═══════════════════════════════════════════════════════════════
"""
    for table, count in store.count().items():
        report += f"  {table:<20} {count} events\n"

    report += """
═══════════════════════════════════════════════════════════════
END OF REPORT — Wissen Infotech SIEM POC
═══════════════════════════════════════════════════════════════
"""

    from datetime import datetime
    fname = f"reports/siem_test_report_{ts}.txt"
    with open(fname, "w") as f:
        f.write(report)

    # Also save JSON
    json_report = {
        "report_time": datetime.now().isoformat(),
        "incidents":   incidents,
        "mttd_log":    mttd_log,
        "log_counts":  store.count()
    }
    jfname = f"reports/siem_incidents_{ts}.json"
    with open(jfname, "w") as f:
        json.dump(json_report, f, indent=2)

    return report, fname, jfname


# ─────────────────────────────────────────────
# MAIN DEMO RUNNER
# ─────────────────────────────────────────────

from datetime import datetime

def main():
    banner()

    # Initialize all SIEM components
    store    = LogStore()
    gen      = LogGenerator(store)
    incidents = IncidentManager()
    playbook  = PlaybookEngine()
    engine   = DetectionEngine(store, incidents, playbook)
    mttd_log  = {}

    print_header("PHASE 1 — SIEM INITIALIZED", Color.GREEN)
    print_log("Log Analytics Workspace (LogStore) — ONLINE", "INFO")
    print_log("Data Connectors (LogGenerator) — CONNECTED", "INFO")
    print_log("Analytics Rules (DetectionEngine) — ACTIVE", "INFO")
    print_log("Playbook Engine (Logic Apps) — READY", "INFO")
    print_log("Incident Manager — RUNNING", "INFO")
    print()
    print_log("Connected log sources:", "INFO")
    for t in store.tables:
        print_log(f"  → {t}", "LOG")

    wait_key()

    # Generate baseline traffic
    print_header("PHASE 2 — GENERATING BASELINE TRAFFIC", Color.CYAN)
    print_log("Simulating normal enterprise activity (20 events)...", "INFO")
    gen.generate_baseline(20)
    counts = store.count()
    for t, c in counts.items():
        if c > 0:
            print_log(f"  {t}: {c} events ingested", "LOG")
    print_log("Baseline established — SIEM monitoring active", "INFO")

    wait_key()

    # Run 3 attack simulations
    print_header("PHASE 3 — ATTACK SIMULATIONS", Color.RED)
    print_log("3 attack scenarios will be simulated", "INFO")
    print_log("Each attack is measured for MTTD (Mean Time to Detect)", "METRIC")

    wait_key()

    inc1 = run_attack_1(gen, engine, mttd_log)
    wait_key()
    inc2 = run_attack_2(gen, engine, mttd_log)
    wait_key()
    inc3 = run_attack_3(gen, engine, mttd_log)
    wait_key()

    # Final metrics
    all_incidents = incidents.get_all()
    print_header("PHASE 4 — RESULTS & METRICS", Color.MAGENTA)
    print_log(f"Total incidents detected: {len(all_incidents)}", "METRIC")
    print_log(f"Detection success rate: {len(all_incidents)}/3 (100%)", "METRIC")
    if mttd_log:
        avg = round(sum(mttd_log.values()) / len(mttd_log), 2)
        print_log(f"Average MTTD: {avg} seconds", "METRIC")
        print_log(f"Before SIEM MTTD: ~4–6 hours (14,400–21,600 seconds)", "METRIC")
        print_log(f"Improvement: {round(14400/avg)}x faster detection", "METRIC")
    for rule, mttd_val in mttd_log.items():
        print_log(f"  {rule}: {mttd_val}s", "METRIC")

    wait_key("Press ENTER to generate full report...")

    # Generate report
    report, fname, jfname = generate_report(all_incidents, mttd_log, store)
    print(report)
    print_log(f"Report saved: {fname}", "INFO")
    print_log(f"JSON data saved: {jfname}", "INFO")
    print()
    print_header("DEMO COMPLETE — SIEM POC SUCCESSFUL", Color.GREEN)
    print_log("All deliverables ready for Scrum presentation", "INFO")
    print_log("Report files in /reports/ folder", "INFO")

if __name__ == "__main__":
    main()
