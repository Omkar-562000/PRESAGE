from __future__ import annotations

import time

RULE_NAME = "Port Scan / Network Reconnaissance Detected"


def analyze(detector, log, config, lock):
    if log.get("table") != "NetworkEvents":
        return

    src_ip = log["SrcIP"]
    port = log["DstPort"]
    now = time.time()
    window = config["alert_threshold"]["port_scan_window_seconds"]

    with lock:
        detector._port_scans[src_ip].append({"time": now, "port": port})
        detector._port_scans[src_ip] = [event for event in detector._port_scans[src_ip] if now - event["time"] <= window]
        unique_ports = len(set(event["port"] for event in detector._port_scans[src_ip]))

    threshold = config["alert_threshold"]["port_scan_ports"]
    if unique_ports >= threshold:
        detector.alert_callback(
            {
                "rule": RULE_NAME,
                "severity": "Medium",
                "mitre": "TA0043 - Reconnaissance / T1046 Network Service Discovery",
                "entity_user": "N/A",
                "entity_ip": src_ip,
                "evidence": f"{unique_ports} unique ports scanned from {src_ip} in {window}s",
                "table": "NetworkEvents",
                "recommended_action": "Block source IP at firewall, investigate for lateral movement",
                "log": log,
            }
        )
        with lock:
            detector._port_scans[src_ip] = []


def simulate(simulator, attacker_ip="185.220.101.45", target_ip="192.168.1.20", num_ports=25):
    simulator.alert_manager.mark_attack_start("port_scan")
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443, 8888, 9200, 27017, 6379, 5432]
    for port in common_ports[:num_ports]:
        log = simulator.generate_network_event(src_ip=attacker_ip, target_ip=target_ip, port=port)
        simulator.ingest_and_analyze(log)
        time.sleep(0.1)
    return {"attack": "port_scan", "ports_scanned": num_ports, "attacker_ip": attacker_ip}
