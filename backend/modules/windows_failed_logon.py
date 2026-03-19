from __future__ import annotations

import time

RULE_NAME = "Windows Failed Logon Burst Detected"


def analyze(detector, log, config, lock):
    if log.get("table") != "WindowsEvent":
        return
    if str(log.get("EventID")) != "4625":
        return

    account = log.get("TargetUserName") or log.get("Computer") or "unknown-host"
    source = log.get("SourceIp") or log.get("Computer") or "local-system"
    now = time.time()
    window = config["alert_threshold"].get("windows_failed_logon_window_seconds", 300)
    threshold = config["alert_threshold"].get("windows_failed_logon_attempts", 5)

    with lock:
        detector._windows_failed_logons[account].append({"time": now, "source": source})
        detector._windows_failed_logons[account] = [event for event in detector._windows_failed_logons[account] if now - event["time"] <= window]
        count = len(detector._windows_failed_logons[account])

    if count >= threshold:
        alert_key = (account, source)
        last_alert_time = detector._windows_failed_logon_cooldown.get(alert_key, 0)
        if now - last_alert_time <= window:
            return
        detector.alert_callback(
            {
                "rule": RULE_NAME,
                "severity": "High",
                "mitre": "TA0006 - Credential Access / T1110 Brute Force",
                "entity_user": account,
                "entity_ip": source,
                "evidence": f"{count} Windows failed logons for {account} within {window//60} minutes",
                "table": "WindowsEvent",
                "recommended_action": "Review local security events, lock the account, and investigate the host",
                "log": log,
            }
        )
        with lock:
            detector._windows_failed_logon_cooldown[alert_key] = now
            detector._windows_failed_logons[account] = []


def simulate(simulator, username="labuser", source_ip="203.0.113.77", attempts=6):
    simulator.alert_manager.mark_attack_start("windows_failed_logon")
    for attempt in range(attempts):
        log = simulator.generate_windows_event(
            channel="Security",
            event_id=4625,
            provider="Microsoft-Windows-Security-Auditing",
            level="Error",
            message=f"An account failed to log on. TargetUserName={username} Source Network Address={source_ip}",
            target_user=username,
            source_ip=source_ip,
        )
        log["AttemptNumber"] = attempt + 1
        simulator.ingest_and_analyze(log)
        time.sleep(0.2)
    return {"attack": "windows_failed_logon", "attempts": attempts, "target_user": username}
