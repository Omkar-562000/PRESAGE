"""
Presage - ATTACK SIMULATOR
Module-oriented attack orchestration for the SIEM demo.
"""

from __future__ import annotations

import random
import time

from backend.modules import brute_force, port_scan, privilege_escalation, windows_failed_logon
from backend.playbook import run_playbook
from backend.siem_engine import (
    AlertManager,
    DetectionEngine,
    EXTERNAL_IPS,
    generate_azure_activity,
    generate_network_event,
    generate_security_event,
    generate_signin_log,
    generate_windows_event,
    ingest_log
)

alert_manager = AlertManager()
detection_results = []


def _on_alert(alert):
    incident, mttd = alert_manager.create_incident(alert)
    actions = run_playbook(incident)
    result = {"incident": incident, "mttd": mttd, "playbook_actions": actions}
    detection_results.append(result)
    return result


engine = DetectionEngine(alert_callback=_on_alert)


class AttackSimulator:
    def __init__(self):
        self.alert_manager = alert_manager
        self.engine = engine
        self.generate_signin_log = generate_signin_log
        self.generate_security_event = generate_security_event
        self.generate_network_event = generate_network_event
        self.generate_azure_activity = generate_azure_activity
        self.generate_windows_event = generate_windows_event

    @staticmethod
    def ingest_and_analyze(log):
        ingest_log(log)
        engine.analyze(log)


simulator = AttackSimulator()


def attack_brute_force(target_user="admin@presage.io", attacker_ip="45.33.32.156", attempts=10):
    return brute_force.simulate(simulator, target_user=target_user, attacker_ip=attacker_ip, attempts=attempts)


def attack_privilege_escalation(user="testuser@presage.io"):
    return privilege_escalation.simulate(simulator, user=user)


def attack_port_scan(attacker_ip="185.220.101.45", target_ip="192.168.1.20", num_ports=25):
    return port_scan.simulate(simulator, attacker_ip=attacker_ip, target_ip=target_ip, num_ports=num_ports)


def attack_windows_failed_logon(username="labuser", source_ip="203.0.113.77", attempts=6):
    return windows_failed_logon.simulate(simulator, username=username, source_ip=source_ip, attempts=attempts)


def generate_background_traffic(stop_event):
    while not stop_event.is_set():
        simulator.ingest_and_analyze(generate_signin_log(success=True))

        if random.random() > 0.6:
            evt = random.choice([4624, 4672, 4698])
            simulator.ingest_and_analyze(generate_security_event(event_id=evt))

        if random.random() > 0.65:
            simulator.ingest_and_analyze(generate_windows_event(channel="Application", event_id=1000, provider="Application-Noise"))

        if random.random() > 0.7:
            simulator.ingest_and_analyze(generate_azure_activity())

        if random.random() > 0.5:
            simulator.ingest_and_analyze(generate_network_event(src_ip=random.choice(EXTERNAL_IPS)))

        time.sleep(1.5)




