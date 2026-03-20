"""
Presage SIEM Project
Unified runner for the current Flask backend + React dashboard.

Run with:
    python siem.py

What this does:
  1. Starts the current Flask backend on http://localhost:5000
  2. Serves the React dashboard from frontend/dist
  3. Provides a small CLI menu to trigger attack simulations
  4. Saves a report snapshot on exit
"""

from __future__ import annotations

import json
import os
import threading
import time

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app import app, start_background_traffic
from backend.attack_simulator import attack_brute_force, attack_port_scan, attack_privilege_escalation, attack_windows_failed_logon
from backend.services.report_service import build_report_payload, generate_pdf_report
from backend.siem_engine import get_incidents

console = Console()


def print_banner():
    console.print(
        Panel.fit(
            "[bold cyan]Presage - Local SIEM System[/bold cyan]\n"
            "[dim]Current stack: Flask API + React/Tailwind dashboard[/dim]\n\n"
            "[green]Dashboard :[/green] http://localhost:5000\n"
            "[green]Sources   :[/green] 5 active log sources\n"
            "[green]Rules     :[/green] 4 active detections\n"
            "[green]Client    :[/green] Mid-Size Enterprise POC",
            title="[bold]SIEM ONLINE[/bold]",
            border_style="cyan",
        )
    )


def print_rules():
    rules = [
        ("Brute Force Login Attack Detected", "High", "SigninLogs", "5 failed logins / 5 min", "TA0006 / T1110"),
        ("Privilege Escalation - Admin Role Assigned", "High", "AzureActivity", "Immediate on role assignment", "TA0004 / T1078"),
        ("Port Scan / Network Reconnaissance Detected", "Medium", "NetworkEvents", "20 ports / 60 sec", "TA0043 / T1046"),
        ("Windows Failed Logon Burst Detected", "High", "WindowsEvent", "5 failed Windows logons / 5 min", "TA0006 / T1110"),
    ]
    table = Table(title="Active Detection Rules", box=box.SIMPLE_HEAVY, header_style="bold cyan")
    table.add_column("Rule", style="white", min_width=30)
    table.add_column("Severity", min_width=8)
    table.add_column("Table", style="dim", min_width=16)
    table.add_column("Threshold", style="green", min_width=24)
    table.add_column("MITRE", style="blue", min_width=14)
    for rule, severity, log_table, threshold, mitre in rules:
        sev_style = "red" if severity == "High" else "yellow"
        table.add_row(rule, f"[{sev_style}]{severity}[/{sev_style}]", log_table, threshold, mitre)
    console.print(table)


def print_menu():
    console.print("\n[bold]Attack Simulation Menu[/bold]")
    console.print("  [cyan]1[/cyan] - Brute Force Login Attack")
    console.print("  [cyan]2[/cyan] - Privilege Escalation")
    console.print("  [cyan]3[/cyan] - Port Scan / Recon")
    console.print("  [cyan]4[/cyan] - Windows Failed Logon Burst")
    console.print("  [cyan]5[/cyan] - Run ALL 4 attacks")
    console.print("  [cyan]6[/cyan] - Show incident summary")
    console.print("  [cyan]7[/cyan] - Save report snapshot")
    console.print("  [cyan]q[/cyan] - Quit\n")


def show_incidents():
    incidents = get_incidents()
    if not incidents:
        console.print("[dim]No incidents detected yet.[/dim]")
        return

    table = Table(title=f"Incidents ({len(incidents)} total)", box=box.SIMPLE_HEAVY, header_style="bold cyan")
    table.add_column("#", min_width=6)
    table.add_column("Rule", min_width=30)
    table.add_column("Severity", min_width=8)
    table.add_column("MTTD(s)", min_width=8)
    table.add_column("Status", min_width=18)

    for incident in incidents:
        severity = incident["Severity"]
        sev_style = "red" if severity == "High" else "yellow"
        table.add_row(
            str(incident["IncidentNumber"]),
            incident["Title"],
            f"[{sev_style}]{severity}[/{sev_style}]",
            str(incident.get("MTTD_seconds", "-")),
            incident["Status"],
        )
    console.print(table)


def save_report_snapshot():
    os.makedirs("reports", exist_ok=True)
    payload = build_report_payload()
    output_path = os.path.join("reports", "incident_report.json")
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)
    pdf_path = generate_pdf_report(os.path.join("reports", "incident_report.pdf"))
    console.print(f"\n[bold green]JSON report saved to {output_path}[/bold green]")
    console.print(f"[bold green]PDF report saved to {pdf_path}[/bold green]")


def run_attack(choice: str):
    if choice == "1":
        attack_brute_force()
    elif choice == "2":
        attack_privilege_escalation()
    elif choice == "3":
        attack_port_scan()
    elif choice == "4":
        attack_windows_failed_logon()
    elif choice == "5":
        console.print("\n[bold yellow]Running all 4 attacks in sequence...[/bold yellow]")
        attack_brute_force()
        time.sleep(1)
        attack_privilege_escalation()
        time.sleep(1)
        attack_port_scan()
        time.sleep(1)
        attack_windows_failed_logon()
        console.print("[green]All 4 attacks completed.[/green]")


def run_server():
    start_background_traffic()
    app.run(debug=False, host="0.0.0.0", port=5000, threaded=True, use_reloader=False)


if __name__ == "__main__":
    print_banner()
    print_rules()

    server_thread = threading.Thread(target=run_server, daemon=True, name="flask-server")
    server_thread.start()
    console.print("[green]Dashboard running at http://localhost:5000[/green]\n")

    time.sleep(1)
    print_menu()

    while True:
        try:
            choice = input("Enter choice: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            choice = "q"

        if choice == "q":
            save_report_snapshot()
            show_incidents()
            console.print("\n[bold cyan]SIEM session ended.[/bold cyan]")
            break
        if choice in {"1", "2", "3", "4", "5"}:
            run_attack(choice)
            time.sleep(2)
            continue
        if choice == "6":
            show_incidents()
            continue
        if choice == "7":
            save_report_snapshot()
            continue
        print_menu()


