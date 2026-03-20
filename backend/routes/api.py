from __future__ import annotations

import datetime as dt
import threading

from flask import Blueprint, jsonify, request, send_file

from backend.attack_simulator import attack_brute_force, attack_port_scan, attack_privilege_escalation, attack_windows_failed_logon
from backend.services.report_service import build_report_payload, generate_pdf_report
from backend.services.state_service import get_config_payload, get_state_payload
from backend.siem_engine import get_alerts, get_incidents, get_logs, get_mttd_summary, get_stats

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _run_attack_in_background(handler, attack_name: str):
    worker = threading.Thread(target=handler, daemon=True, name=f"attack-{attack_name}")
    worker.start()
    return {"status": "started", "attack": attack_name}


@api_bp.get("/health")
def api_health():
    return jsonify(
        {
            "status": "ok",
            "service": "presage-siem",
            "timestamp": dt.datetime.now().isoformat(),
        }
    )


@api_bp.get("/config")
def api_config():
    return jsonify(get_config_payload())


@api_bp.get("/state")
def api_state():
    return jsonify(get_state_payload())


@api_bp.get("/stats")
def api_stats():
    return jsonify(get_stats())


@api_bp.get("/incidents")
def api_incidents():
    return jsonify(get_incidents())


@api_bp.get("/alerts")
def api_alerts():
    return jsonify(get_alerts())


@api_bp.get("/logs/<table>")
def api_logs(table: str):
    limit = int(request.args.get("limit", 50))
    return jsonify(get_logs(table, limit))


@api_bp.get("/mttd")
def api_mttd():
    return jsonify(get_mttd_summary())


@api_bp.post("/attack/brute_force")
def api_brute_force():
    return jsonify(_run_attack_in_background(attack_brute_force, "brute_force"))


@api_bp.post("/attack/privilege_escalation")
def api_privilege_escalation():
    return jsonify(_run_attack_in_background(attack_privilege_escalation, "privilege_escalation"))


@api_bp.post("/attack/port_scan")
def api_port_scan():
    return jsonify(_run_attack_in_background(attack_port_scan, "port_scan"))


@api_bp.post("/attack/windows_failed_logon")
def api_windows_failed_logon():
    return jsonify(_run_attack_in_background(attack_windows_failed_logon, "windows_failed_logon"))


@api_bp.get("/report")
def api_report():
    return jsonify(build_report_payload())


@api_bp.get("/report/pdf")
def api_report_pdf():
    pdf_path = generate_pdf_report()
    return send_file(
        pdf_path,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=pdf_path.name,
    )

