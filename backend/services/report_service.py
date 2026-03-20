from __future__ import annotations

import datetime as dt
from collections import Counter
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from backend.siem_engine import CONFIG, LOG_TABLES, get_incidents, get_logs, get_mttd_summary, get_stats

REPORTS_DIR = Path.cwd() / "reports"
EXCLUDED_TABLES = {"Alerts", "Incidents"}
RECENT_INCIDENT_LIMIT = 10
RECENT_EVIDENCE_LIMIT = 15
SAMPLE_ROWS_PER_TABLE = 3


def _timestamp_slug() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def _stringify(value) -> str:
    if value is None:
        return "-"
    if isinstance(value, dict):
        return ", ".join(f"{key}={_stringify(item)}" for key, item in value.items())
    if isinstance(value, list):
        return ", ".join(_stringify(item) for item in value)
    return str(value)


def _build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="SectionBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TinyTable",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9,
        )
    )
    return styles


def _paragraph(value, style):
    return Paragraph(_stringify(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), style)


def _section_heading(title: str, styles):
    return [Paragraph(title, styles["Heading2"]), Spacer(1, 0.12 * inch)]


def _table(data, col_widths=None, repeat_rows=1):
    table = Table(data, colWidths=col_widths, repeatRows=repeat_rows)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("LEADING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def _all_log_tables():
    return [table for table in LOG_TABLES.keys() if table not in EXCLUDED_TABLES]


def _load_log_tables() -> dict:
    return {table: get_logs(table, limit=len(LOG_TABLES.get(table, []))) for table in _all_log_tables()}


def _parse_timestamp(value):
    if not value:
        return dt.datetime.min
    try:
        return dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return dt.datetime.min


def _severity_breakdown(incidents: list[dict]) -> dict:
    counter = Counter(incident.get("Severity", "Unknown") for incident in incidents)
    order = ["Critical", "High", "Medium", "Low"]
    result = {label: counter[label] for label in order if counter[label]}
    for label, count in sorted(counter.items()):
        if label not in result:
            result[label] = count
    return result


def _source_breakdown(incidents: list[dict]) -> dict:
    counter = Counter(incident.get("SourceTable", "Unknown") for incident in incidents)
    return dict(sorted(counter.items(), key=lambda item: (-item[1], item[0])))


def _incident_snapshot(incident: dict) -> dict:
    return {
        "incident_number": incident.get("IncidentNumber"),
        "created_at": incident.get("CreatedTime"),
        "title": incident.get("Title"),
        "severity": incident.get("Severity"),
        "status": incident.get("Status"),
        "affected_entity": incident.get("AffectedEntity"),
        "source": incident.get("SourceTable"),
        "mitre_tactic": incident.get("MITRETactic"),
        "evidence": incident.get("Evidence"),
        "recommended_action": incident.get("RecommendedAction"),
        "playbook_triggered": incident.get("PlaybookTriggered"),
        "playbook_actions": incident.get("PlaybookActions", []),
        "playbook_duration": incident.get("PlaybookDuration"),
        "mttd_seconds": incident.get("MTTD_seconds"),
    }


def _summarize_log_entry(table_name: str, entry: dict) -> str:
    if table_name == "SigninLogs":
        return (
            f"{entry.get('UserPrincipalName', 'Unknown user')} -> {entry.get('AppDisplayName', 'Unknown app')} "
            f"from {entry.get('IPAddress', '-')}: {entry.get('ResultDescription', 'No result')}"
        )
    if table_name == "AzureActivity":
        return (
            f"{entry.get('Caller', 'Unknown caller')} performed {entry.get('OperationName', 'Unknown operation')} "
            f"on {entry.get('ResourceGroup', '-') }"
        )
    if table_name == "SecurityEvent":
        return (
            f"{entry.get('Account', 'Unknown account')} on {entry.get('Computer', '-')} - "
            f"{entry.get('Activity', 'No activity')}"
        )
    if table_name == "NetworkEvents":
        return (
            f"{entry.get('Action', 'Unknown action')} {entry.get('Protocol', '-') } traffic "
            f"{entry.get('SrcIP', '-') } -> {entry.get('DstIP', '-') }:{entry.get('DstPort', '-') }"
        )
    if table_name == "WindowsEvent":
        return (
            f"{entry.get('Computer', 'Unknown host')} {entry.get('Provider', 'Unknown provider')} "
            f"Event {entry.get('EventID', '-') } on {entry.get('Channel', '-') }"
        )
    return ", ".join(f"{key}={value}" for key, value in entry.items() if key != "table")


def _trim_evidence_entry(table_name: str, entry: dict) -> dict:
    return {
        "timestamp": entry.get("TimeGenerated"),
        "table": table_name,
        "summary": _summarize_log_entry(table_name, entry),
        "key_fields": {key: value for key, value in entry.items() if key in {"UserPrincipalName", "IPAddress", "Caller", "OperationName", "Account", "Computer", "Activity", "SrcIP", "DstIP", "DstPort", "Action", "EventID", "Provider", "Channel", "ResultDescription"} and value is not None},
    }


def _build_telemetry_overview(log_tables: dict) -> dict:
    overview = {}
    for table_name, entries in log_tables.items():
        latest_timestamp = entries[0].get("TimeGenerated") if entries else None
        overview[table_name] = {
            "record_count": len(entries),
            "latest_timestamp": latest_timestamp,
            "sample_records": [_trim_evidence_entry(table_name, entry) for entry in entries[:SAMPLE_ROWS_PER_TABLE]],
        }
    return overview


def _build_recent_evidence(log_tables: dict) -> list[dict]:
    merged = []
    for table_name, entries in log_tables.items():
        for entry in entries:
            merged.append((table_name, entry))
    merged.sort(key=lambda item: _parse_timestamp(item[1].get("TimeGenerated")), reverse=True)
    return [_trim_evidence_entry(table_name, entry) for table_name, entry in merged[:RECENT_EVIDENCE_LIMIT]]


def build_full_report_payload() -> dict:
    log_tables = _load_log_tables()
    return {
        "generated_at": dt.datetime.now().isoformat(),
        "organization": CONFIG["organization"],
        "client": CONFIG["client"],
        "workspace_name": CONFIG["workspace_name"],
        "workspace_id": CONFIG["workspace_id"],
        "summary": get_stats(),
        "mttd_summary": get_mttd_summary(),
        "incidents": get_incidents(),
        "logs_by_table": log_tables,
    }


def build_report_payload() -> dict:
    full_payload = build_full_report_payload()
    incidents = full_payload["incidents"]
    log_tables = full_payload["logs_by_table"]
    mttd = full_payload["mttd_summary"]
    high_severity_entities = sorted(
        {
            incident.get("AffectedEntity")
            for incident in incidents
            if incident.get("Severity") == "High" and incident.get("AffectedEntity")
        }
    )

    return {
        "report_metadata": {
            "generated_at": full_payload["generated_at"],
            "organization": full_payload["organization"],
            "client": full_payload["client"],
            "workspace_name": full_payload["workspace_name"],
            "workspace_id": full_payload["workspace_id"],
            "report_type": "executive_incident_report",
        },
        "executive_summary": {
            "total_logs": full_payload["summary"].get("total_logs", 0),
            "total_alerts": full_payload["summary"].get("total_alerts", 0),
            "total_incidents": full_payload["summary"].get("total_incidents", 0),
            "high_severity_incidents": full_payload["summary"].get("high_severity", 0),
            "active_log_sources": full_payload["summary"].get("sources_active", 0),
            "average_mttd_seconds": mttd.get("average"),
            "mttd_records": len(mttd.get("records", [])),
            "priority_entities": high_severity_entities[:10],
        },
        "incident_overview": {
            "severity_breakdown": _severity_breakdown(incidents),
            "source_breakdown": _source_breakdown(incidents),
            "open_incidents": sum(1 for incident in incidents if incident.get("Status") != "Closed"),
            "playbooks_triggered": sum(1 for incident in incidents if incident.get("PlaybookTriggered")),
        },
        "recent_incidents": [_incident_snapshot(incident) for incident in incidents[:RECENT_INCIDENT_LIMIT]],
        "detection_performance": {
            "average_mttd_seconds": mttd.get("average"),
            "records": mttd.get("records", []),
        },
        "telemetry_overview": _build_telemetry_overview(log_tables),
        "recent_evidence_timeline": _build_recent_evidence(log_tables),
    }


def _summary_table(payload, styles):
    summary = payload["summary"]
    mttd = payload["mttd_summary"]
    rows = [
        [_paragraph("Metric", styles["TinyTable"]), _paragraph("Value", styles["TinyTable"])],
        [_paragraph("Generated At", styles["TinyTable"]), _paragraph(payload["generated_at"], styles["TinyTable"])],
        [_paragraph("Organization", styles["TinyTable"]), _paragraph(payload["organization"], styles["TinyTable"])],
        [_paragraph("Client", styles["TinyTable"]), _paragraph(payload["client"], styles["TinyTable"])],
        [_paragraph("Workspace", styles["TinyTable"]), _paragraph(payload["workspace_name"], styles["TinyTable"])],
        [_paragraph("Workspace ID", styles["TinyTable"]), _paragraph(payload["workspace_id"], styles["TinyTable"])],
        [_paragraph("Total Logs", styles["TinyTable"]), _paragraph(summary["total_logs"], styles["TinyTable"])],
        [_paragraph("Total Alerts", styles["TinyTable"]), _paragraph(summary["total_alerts"], styles["TinyTable"])],
        [_paragraph("Total Incidents", styles["TinyTable"]), _paragraph(summary["total_incidents"], styles["TinyTable"])],
        [_paragraph("High Severity Incidents", styles["TinyTable"]), _paragraph(summary["high_severity"], styles["TinyTable"])],
        [_paragraph("Sources Active", styles["TinyTable"]), _paragraph(summary["sources_active"], styles["TinyTable"])],
        [_paragraph("Average MTTD (s)", styles["TinyTable"]), _paragraph(mttd["average"], styles["TinyTable"])],
        [_paragraph("MTTD Records", styles["TinyTable"]), _paragraph(len(mttd["records"]), styles["TinyTable"])],
    ]
    return _table(rows, col_widths=[2.4 * inch, 4.4 * inch])


def _incidents_table(payload, styles):
    rows = [[
        _paragraph("Incident #", styles["TinyTable"]),
        _paragraph("Created", styles["TinyTable"]),
        _paragraph("Title", styles["TinyTable"]),
        _paragraph("Severity", styles["TinyTable"]),
        _paragraph("Status", styles["TinyTable"]),
        _paragraph("Entity", styles["TinyTable"]),
        _paragraph("Source", styles["TinyTable"]),
        _paragraph("MTTD (s)", styles["TinyTable"]),
    ]]

    incidents = payload["incidents"]
    if not incidents:
        rows.append([_paragraph("No incidents detected yet.", styles["TinyTable"])] + [""] * 7)
    else:
        for incident in incidents:
            rows.append(
                [
                    _paragraph(incident.get("IncidentNumber"), styles["TinyTable"]),
                    _paragraph(incident.get("CreatedTime"), styles["TinyTable"]),
                    _paragraph(incident.get("Title"), styles["TinyTable"]),
                    _paragraph(incident.get("Severity"), styles["TinyTable"]),
                    _paragraph(incident.get("Status"), styles["TinyTable"]),
                    _paragraph(incident.get("AffectedEntity"), styles["TinyTable"]),
                    _paragraph(incident.get("SourceTable"), styles["TinyTable"]),
                    _paragraph(incident.get("MTTD_seconds"), styles["TinyTable"]),
                ]
            )
    return _table(rows, col_widths=[0.8 * inch, 1.55 * inch, 2.45 * inch, 0.7 * inch, 1.0 * inch, 1.35 * inch, 0.95 * inch, 0.7 * inch])


def _mttd_table(payload, styles):
    rows = [[
        _paragraph("Timestamp", styles["TinyTable"]),
        _paragraph("Attack", styles["TinyTable"]),
        _paragraph("MTTD (s)", styles["TinyTable"]),
    ]]
    records = payload["mttd_summary"]["records"]
    if not records:
        rows.append([
            _paragraph("No completed MTTD records yet.", styles["TinyTable"]),
            "",
            "",
        ])
    else:
        for record in records:
            rows.append(
                [
                    _paragraph(record.get("timestamp"), styles["TinyTable"]),
                    _paragraph(record.get("attack"), styles["TinyTable"]),
                    _paragraph(record.get("mttd_seconds"), styles["TinyTable"]),
                ]
            )
    return _table(rows, col_widths=[2.2 * inch, 4.3 * inch, 1.1 * inch])


def _log_table(table_name: str, entries: list[dict], styles):
    columns = ["TimeGenerated"] + [key for key in entries[0].keys() if key != "TimeGenerated"] if entries else ["TimeGenerated", "Details"]
    rows = [[_paragraph(column, styles["TinyTable"]) for column in columns]]

    if not entries:
        rows.append([
            _paragraph("-", styles["TinyTable"]),
            _paragraph("No log records captured for this table.", styles["TinyTable"]),
        ])
        return _table(rows, col_widths=[1.8 * inch, 8.6 * inch])

    for entry in entries:
        rows.append([_paragraph(entry.get(column), styles["TinyTable"]) for column in columns])

    page_width = landscape(A4)[0] - 0.8 * inch
    first_col = 1.8 * inch
    remaining = max(page_width - first_col, 2 * inch)
    per_col = remaining / max(len(columns) - 1, 1)
    col_widths = [first_col] + [per_col] * (len(columns) - 1)
    return _table(rows, col_widths=col_widths)


def generate_pdf_report(output_path: str | Path | None = None) -> Path:
    payload = build_full_report_payload()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    pdf_path = Path(output_path) if output_path else REPORTS_DIR / f"presage_siem_report_{_timestamp_slug()}.pdf"
    styles = _build_styles()
    elements = []

    elements.append(Paragraph("PRESAGE SIEM RECORD EXPORT", styles["Title"]))
    elements.append(Spacer(1, 0.12 * inch))
    elements.append(
        Paragraph(
            (
                f"Comprehensive SIEM snapshot for {payload['organization']} / {payload['client']}."
                f" Includes summary metrics, incidents, MTTD records, and full in-memory log tables"
                f" captured at {payload['generated_at']}."
            ),
            styles["SectionBody"],
        )
    )
    elements.append(Spacer(1, 0.12 * inch))

    elements.extend(_section_heading("1. Executive Summary", styles))
    elements.append(_summary_table(payload, styles))
    elements.append(Spacer(1, 0.2 * inch))

    elements.extend(_section_heading("2. Incident Register", styles))
    elements.append(_incidents_table(payload, styles))
    elements.append(Spacer(1, 0.2 * inch))

    elements.extend(_section_heading("3. MTTD Timeline", styles))
    elements.append(_mttd_table(payload, styles))

    for index, (table_name, entries) in enumerate(payload["logs_by_table"].items(), start=4):
        elements.append(PageBreak())
        elements.extend(_section_heading(f"{index}. {table_name} Log Records", styles))
        elements.append(
            Paragraph(
                f"Total records included for {table_name}: {len(entries)}. Each row reflects the captured SIEM event payload and timestamp.",
                styles["SectionBody"],
            )
        )
        elements.append(_log_table(table_name, entries, styles))

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=landscape(A4),
        leftMargin=0.4 * inch,
        rightMargin=0.4 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.45 * inch,
        title="Presage SIEM Record Export",
        author="Presage",
    )
    doc.build(elements)
    return pdf_path
