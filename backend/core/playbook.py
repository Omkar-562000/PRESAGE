"""
Presage SIEM Project
Automated Playbook — mirrors Microsoft Sentinel Logic App automation
Triggers on High/Medium severity incidents and executes response actions
"""

import time
import json
from datetime import datetime, timezone
from backend.core.detection_engine import incidents


# ── Playbook actions ──────────────────────────────────────────────────────────
def _action_send_alert(incident: dict) -> dict:
    """Simulate sending email/Teams notification."""
    msg = (f"[SECURITY ALERT] {incident['severity'].upper()} — "
           f"{incident['rule']}\n"
           f"Incident ID : {incident['id']}\n"
           f"Detected at : {incident['detected_at']}\n"
           f"Description : {incident['description']}\n"
           f"MTTD        : {incident['mttd_seconds']}s\n"
           f"MITRE       : {incident['mitre']}")
    print(f"\n{'='*60}")
    print(f"  PLAYBOOK — TEAMS/EMAIL NOTIFICATION SENT")
    print(f"{'='*60}")
    print(msg)
    print(f"{'='*60}\n")
    return {"action": "send_notification", "status": "sent",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message_preview": incident['rule']}


def _action_tag_incident(incident: dict) -> dict:
    """Tag incident as Under Investigation."""
    incident["status"] = "Under Investigation"
    print(f"  PLAYBOOK — Incident {incident['id']} tagged: "
          f"Under Investigation")
    return {"action": "tag_incident", "status": "tagged",
            "new_status": "Under Investigation",
            "timestamp": datetime.now(timezone.utc).isoformat()}


def _action_block_ip(incident: dict) -> dict:
    """Simulate blocking attacker IP (High severity only)."""
    ip = incident.get("entities", {}).get("ip") or \
         incident.get("entities", {}).get("src_ip")
    if not ip:
        return {"action": "block_ip", "status": "skipped",
                "reason": "no IP entity"}
    print(f"  PLAYBOOK — Firewall rule added: BLOCK {ip}")
    return {"action": "block_ip", "status": "executed",
            "ip_blocked": ip,
            "timestamp": datetime.now(timezone.utc).isoformat()}


def _action_create_ticket(incident: dict) -> dict:
    """Simulate creating a ServiceNow/Jira ticket."""
    ticket_id = f"TICK-{abs(hash(incident['id'])) % 90000 + 10000}"
    print(f"  PLAYBOOK — Ticket created: {ticket_id} "
          f"[{incident['severity']} Priority]")
    return {"action": "create_ticket", "status": "created",
            "ticket_id": ticket_id,
            "priority": incident["severity"],
            "timestamp": datetime.now(timezone.utc).isoformat()}


# ── Playbook runner ───────────────────────────────────────────────────────────
def run_playbook(incident: dict):
    """
    Automation rule logic:
      IF severity == High   → notify + tag + block IP + create ticket
      IF severity == Medium → notify + tag + create ticket
      IF severity == Low    → tag only
    """
    severity = incident.get("severity", "Low")
    print(f"\n[PLAYBOOK] Triggered for {incident['id']} "
          f"({severity}) — executing response actions...")
    start = time.time()
    responses = []

    responses.append(_action_send_alert(incident))
    responses.append(_action_tag_incident(incident))

    if severity == "High":
        responses.append(_action_block_ip(incident))

    responses.append(_action_create_ticket(incident))

    elapsed = round(time.time() - start, 3)
    print(f"[PLAYBOOK] All actions completed in {elapsed}s\n")

    incident["response"] = responses
    incident["mttr_seconds"] = elapsed
    return responses


