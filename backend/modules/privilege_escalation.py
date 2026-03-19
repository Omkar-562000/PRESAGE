from __future__ import annotations

import time

RULE_NAME = "Privilege Escalation - Admin Role Assigned"


def analyze(detector, log, _config, _lock):
    if log.get("table") != "AzureActivity":
        return
    if "roleAssignments/write" not in log.get("OperationName", ""):
        return

    detector.alert_callback(
        {
            "rule": RULE_NAME,
            "severity": "High",
            "mitre": "TA0004 - Privilege Escalation / T1078 Valid Accounts",
            "entity_user": log.get("Caller"),
            "entity_ip": "N/A",
            "evidence": f"Role assignment operation: {log.get('OperationName')} on {log.get('ResourceGroup')}",
            "table": "AzureActivity",
            "recommended_action": "Review role assignment, verify with user's manager, revoke if unauthorized",
            "log": log,
        }
    )


def simulate(simulator, user="testuser@presage.io"):
    simulator.alert_manager.mark_attack_start("privilege_escalation")
    for _ in range(3):
        log = simulator.generate_azure_activity(user=user)
        simulator.ingest_and_analyze(log)
        time.sleep(0.1)

    escalation_log = simulator.generate_azure_activity(user=user, operation="Microsoft.Authorization/roleAssignments/write")
    escalation_log["NewRole"] = "Global Administrator"
    escalation_log["TargetUser"] = user
    simulator.ingest_and_analyze(escalation_log)
    return {"attack": "privilege_escalation", "user": user}

