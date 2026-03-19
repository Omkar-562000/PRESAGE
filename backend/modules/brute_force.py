from __future__ import annotations

import time

RULE_NAME = "Brute Force Login Attack Detected"


def analyze(detector, log, config, lock):
    if log.get("table") != "SigninLogs":
        return
    if log.get("ResultType") == "0":
        return

    user = log["UserPrincipalName"]
    ip = log["IPAddress"]
    now = time.time()
    window = config["alert_threshold"]["brute_force_window_seconds"]

    with lock:
        detector._failed_logins[user].append({"time": now, "ip": ip})
        detector._failed_logins[user] = [event for event in detector._failed_logins[user] if now - event["time"] <= window]
        count = len(detector._failed_logins[user])

    threshold = config["alert_threshold"]["brute_force_attempts"]
    if count >= threshold:
        alert_key = (user, ip)
        last_alert_time = detector._bruteforce_cooldown.get(alert_key, 0)
        if now - last_alert_time <= window:
            return
        detector.alert_callback(
            {
                "rule": RULE_NAME,
                "severity": "High",
                "mitre": "TA0006 - Credential Access / T1110 Brute Force",
                "entity_user": user,
                "entity_ip": ip,
                "evidence": f"{count} failed login attempts in {window//60} minutes",
                "table": "SigninLogs",
                "recommended_action": "Block IP, reset user password, enable MFA",
                "log": log,
            }
        )
        with lock:
            detector._bruteforce_cooldown[alert_key] = now
            detector._failed_logins[user] = []


def simulate(simulator, target_user="admin@presage.io", attacker_ip="45.33.32.156", attempts=10):
    simulator.alert_manager.mark_attack_start("brute_force")
    for attempt in range(attempts):
        log = simulator.generate_signin_log(user=target_user, success=False, ip=attacker_ip)
        log["AttemptNumber"] = attempt + 1
        simulator.ingest_and_analyze(log)
        time.sleep(0.3)
    return {"attack": "brute_force", "attempts": attempts, "target": target_user}

