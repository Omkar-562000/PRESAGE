from __future__ import annotations

import datetime as dt
from collections import Counter

from backend.config import SIEM_RULES
from backend.siem_engine import CONFIG, get_alerts, get_incidents, get_logs, get_mttd_summary, get_stats

LOG_TABLES = ["SigninLogs", "SecurityEvent", "WindowsEvent", "AzureActivity", "NetworkEvents"]


def get_config_payload():
    return {
        "organization": CONFIG["organization"],
        "client": CONFIG["client"],
        "workspace_name": CONFIG["workspace_name"],
        "workspace_id": CONFIG["workspace_id"],
        "log_retention_days": CONFIG["log_retention_days"],
        "sources": LOG_TABLES,
        "rules": SIEM_RULES,
    }


def build_source_health(logs_by_table):
    health = []
    for table, entries in logs_by_table.items():
        last_seen = entries[0]["TimeGenerated"] if entries else None
        if entries:
            status = "Healthy"
        else:
            status = "Idle"
        health.append(
            {
                "source": table,
                "recent_events": len(entries),
                "last_seen": last_seen,
                "status": status,
            }
        )
    return health


def build_alert_trend(incidents):
    severity_counts = Counter(incident["Severity"] for incident in incidents)
    incident_counts = Counter((incident.get("CreatedTime") or "")[:13] for incident in incidents if incident.get("CreatedTime"))
    top_window = [
        {"window": window, "count": count}
        for window, count in sorted(incident_counts.items(), reverse=True)[:6]
    ]
    return {
        "by_severity": {
            "High": severity_counts.get("High", 0),
            "Medium": severity_counts.get("Medium", 0),
            "Low": severity_counts.get("Low", 0),
        },
        "recent_windows": top_window,
    }


def build_entity_summary(incidents):
    entity_counter = Counter(incident.get("AffectedEntity") for incident in incidents if incident.get("AffectedEntity"))
    return [
        {"entity": entity, "incidents": count}
        for entity, count in entity_counter.most_common(5)
    ]


def get_state_payload():
    logs_by_table = {table: get_logs(table, 20) for table in LOG_TABLES}
    merged_logs = []
    for table, entries in logs_by_table.items():
        for entry in entries:
            merged_logs.append({**entry, "_table": table})
    merged_logs.sort(key=lambda item: item.get("TimeGenerated", ""), reverse=True)

    incidents = get_incidents()[:20]
    return {
        "generated_at": dt.datetime.now().isoformat(),
        "config": {
            "organization": CONFIG["organization"],
            "client": CONFIG["client"],
            "workspace_name": CONFIG["workspace_name"],
        },
        "stats": get_stats(),
        "alerts": get_alerts()[:10],
        "incidents": incidents,
        "mttd": get_mttd_summary(),
        "logs_by_table": logs_by_table,
        "recent_logs": merged_logs[:40],
        "source_health": build_source_health(logs_by_table),
        "alert_trend": build_alert_trend(incidents),
        "top_entities": build_entity_summary(incidents),
    }
