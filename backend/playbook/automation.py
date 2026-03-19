"""
Presage - PLAYBOOK AUTOMATION
Automated response actions for high-severity incidents.
"""

from __future__ import annotations

import time


def run_playbook(incident):
    """
    Execute the demo response workflow for high-severity incidents.
    Mirrors a Sentinel automation rule invoking a Logic App playbook.
    """
    if not incident.get("PlaybookTriggered"):
        return

    playbook_start = time.time()
    inc_num = incident["IncidentNumber"]

    print(f"\n  [PLAYBOOK] Triggered for Incident #{inc_num} - {incident['Severity']} severity")
    time.sleep(0.3)

    actions_taken = []

    incident["Status"] = "Under Investigation"
    actions_taken.append("Incident tagged as Under Investigation")

    entity = incident.get("AffectedEntity", "")
    if "@" in str(entity):
        actions_taken.append(f"User account flagged for review: {entity}")
    else:
        actions_taken.append(f"IP address queued for firewall block: {entity}")

    actions_taken.append("Security team notified via Teams/Email alert")
    actions_taken.append("Incident ticket created in ITSM system")

    playbook_duration = round(time.time() - playbook_start, 2)
    incident["PlaybookActions"] = actions_taken
    incident["PlaybookDuration"] = f"{playbook_duration}s"

    return actions_taken

