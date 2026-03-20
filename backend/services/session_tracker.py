# backend/services/session_tracker.py

import time
import threading
from datetime import datetime, timezone
import copy
import uuid

_lock = threading.Lock()

SESSION = {
    "session_id": None,
    "started_at": None,
    "started_at_epoch": None,
    "events": [],
    "attacks": {},
    "pages_visited": [],
    "summary": {}
}


def init_session():
    now = datetime.now(timezone.utc)
    with _lock:
        SESSION["session_id"] = str(uuid.uuid4())
        SESSION["started_at"] = now.isoformat()
        SESSION["started_at_epoch"] = time.time()
        SESSION["events"] = []
        SESSION["attacks"] = {}
        SESSION["pages_visited"] = []
        SESSION["summary"] = {}

    record_event("session_start", {
        "message": "PRESAGE session initialised"
    }, source="system")


def record_event(event_type, data=None, source="system"):
    now = datetime.now(timezone.utc)
    epoch = time.time()

    with _lock:
        event = {
            "event_id": len(SESSION["events"]) + 1,
            "event_type": event_type,
            "timestamp": now.isoformat(),
            "timestamp_epoch": epoch,
            "elapsed_seconds": round(epoch - SESSION["started_at_epoch"], 2)
            if SESSION["started_at_epoch"] else 0,
            "source": source,
            "data": data or {}
        }
        SESSION["events"].append(event)

    return event


def record_page_visit(page_name):
    with _lock:
        SESSION["pages_visited"].append({
            "page": page_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "elapsed_seconds": round(time.time() - SESSION["started_at_epoch"], 2)
        })

    record_event("page_visit", {"page": page_name}, source="user")


def record_attack_start(attack_type):
    epoch = time.time()

    with _lock:
        SESSION["attacks"][attack_type] = {
            "attack_type": attack_type,
            "triggered_at": datetime.now(timezone.utc).isoformat(),
            "triggered_at_epoch": epoch,
            "elapsed_at_trigger": round(epoch - SESSION["started_at_epoch"], 2),
            "detected_at": None,
            "mttd_seconds": None,
            "incident_title": None,
            "severity": None,
            "playbook_ran": False,
            "playbook_actions": []
        }

    record_event("attack_triggered", {
        "attack_type": attack_type
    }, source="user")


def record_attack_detected(attack_type, incident_title, severity, mttd_seconds):
    with _lock:
        if attack_type in SESSION["attacks"]:
            SESSION["attacks"][attack_type].update({
                "detected_at": datetime.now(timezone.utc).isoformat(),
                "mttd_seconds": round(mttd_seconds, 2),
                "incident_title": incident_title,
                "severity": severity
            })

    record_event("attack_detected", {
        "attack_type": attack_type,
        "mttd_seconds": round(mttd_seconds, 2),
        "severity": severity,
        "incident_title": incident_title
    }, source="system")


def record_playbook_action(attack_type, action_name, action_index):
    with _lock:
        if attack_type in SESSION["attacks"]:
            SESSION["attacks"][attack_type]["playbook_ran"] = True
            SESSION["attacks"][attack_type]["playbook_actions"].append({
                "step": action_index,
                "action": action_name,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

    record_event("playbook_action", {
        "attack_type": attack_type,
        "step": action_index,
        "action": action_name
    }, source="system")


def get_full_session():
    with _lock:
        session = copy.deepcopy(SESSION)

    attacks = list(session["attacks"].values())
    mttd_values = [a["mttd_seconds"] for a in attacks if a["mttd_seconds"]]

    avg_mttd = (sum(mttd_values) / len(mttd_values)) if mttd_values else None

    session["summary"] = {
        "total_events": len(session["events"]),
        "pages_visited_count": len(session["pages_visited"]),
        "attacks_triggered": len(attacks),
        "attacks_detected": len(mttd_values),
        "average_mttd_seconds": round(avg_mttd, 2) if avg_mttd else None,
        "best_mttd_seconds": min(mttd_values) if mttd_values else None,
        "worst_mttd_seconds": max(mttd_values) if mttd_values else None,
        "session_duration_seconds": round(
            time.time() - session["started_at_epoch"], 2
        ) if session["started_at_epoch"] else None,
        "industry_baseline_seconds": 14400,
        "improvement_factor": round(14400 / avg_mttd, 0)
        if avg_mttd else None
    }

    return session