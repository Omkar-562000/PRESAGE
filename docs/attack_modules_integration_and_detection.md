# Presage SIEM Attack Modules Integration And Detection Guide

## Purpose Of This Document

This document explains each attack module implemented in the project and describes:

- how the module is integrated into the system
- the logic behind the detection
- the techniques involved in the attack
- how the system defends against the attack
- how the attack is read from logs
- how it is detected and turned into an alert and incident

This document is focused on the working implementation in the current project.

## Common Integration Flow For All Attack Modules

All attack modules in the project follow the same high-level flow:

1. an attack is simulated or a suspicious event is collected
2. the event is generated in a source-specific log format
3. the event is ingested into the SIEM engine
4. the detection engine passes the event to the relevant module logic
5. the module checks thresholds and attack conditions
6. if a match is found, an alert is raised
7. the alert is converted into an incident
8. the playbook is triggered if the severity requires response
9. the frontend displays the incident, telemetry, and response details

In the project, this flow is wired mainly through:

- `backend/attack_simulator.py`
- `backend/siem_engine.py`
- `backend/modules/`
- `backend/playbook/`
- `backend/routes/`
- `frontend/`

## Attack Module 1: Brute Force Login Attack

### What This Attack Means

A brute force login attack is an attempt to repeatedly guess credentials until access is gained. In enterprise environments this often appears as multiple failed sign-in attempts against one account from the same source IP.

### Technique Used In This Attack

- repeated invalid login attempts
- credential guessing
- concentration of failures in a short time window

Mapped technique:

- MITRE ATT&CK: `TA0006 / T1110 Brute Force`

### How It Is Integrated In The Project

This module is implemented in:

- `backend/modules/brute_force.py`
- `kql-rules/brute_force_login.kql`

It is triggered from:

- `backend/attack_simulator.py`

It reads from:

- `SigninLogs`

### Detection Logic

The brute force module checks:

- log table must be `SigninLogs`
- login result must be a failure
- failed attempts are grouped for the same user
- only events inside the configured time window are counted
- once the threshold is reached, an alert is generated

Current threshold:

- `5` failed logins in `5` minutes

The logic also includes a cooldown mechanism so repeated alerts are not generated immediately again for the same user and IP combination.

### How The Attack Is Read

The module reads fields such as:

- `UserPrincipalName`
- `IPAddress`
- `ResultType`

If `ResultType` is not success and the count reaches threshold within the time window, it is treated as a brute force pattern.

### How The System Defends Against It

The system does not directly block a user at the operating system level, but it provides a defensive workflow by:

- detecting the failed login burst
- generating a high-severity alert
- creating an incident
- recommending IP blocking and password reset
- triggering playbook actions for follow-up

### Alert And Incident Flow

Once detected:

- alert severity: `High`
- alert rule: `Brute Force Login Attack Detected`
- incident is created by the alert manager
- playbook is triggered because the incident is high severity

## Attack Module 2: Privilege Escalation

### What This Attack Means

Privilege escalation is an attack or misuse scenario where a user gains higher access rights than they should have. In cloud environments, one key indicator is suspicious role assignment or admin privilege assignment activity.

### Technique Used In This Attack

- privileged role assignment
- elevation of access rights
- misuse of administrative control paths

Mapped technique:

- MITRE ATT&CK: `TA0004 / T1078 Valid Accounts`

### How It Is Integrated In The Project

This module is implemented in:

- `backend/modules/privilege_escalation.py`
- `kql-rules/privilege_escalation_admin_assignment.kql`

It is triggered from:

- `backend/attack_simulator.py`

It reads from:

- `AzureActivity`

### Detection Logic

The privilege escalation module checks:

- log table must be `AzureActivity`
- operation name must contain `roleAssignments/write`

When this condition is met, the system treats the action as suspicious administrative privilege assignment activity and raises an alert immediately.

Current behavior:

- immediate detection on matching role assignment operation

### How The Attack Is Read

The module reads fields such as:

- `Caller`
- `OperationName`
- `ResourceGroup`

When a role assignment write operation is detected, the user connected to that action becomes the affected entity in the alert.

### How The System Defends Against It

The system helps defend by:

- detecting unauthorized or suspicious role assignment activity
- raising a high-severity alert immediately
- recommending review and revocation of the role assignment
- triggering playbook actions for investigation

### Alert And Incident Flow

Once detected:

- alert severity: `High`
- alert rule: `Privilege Escalation - Admin Role Assigned`
- incident is created
- playbook is triggered for automated response simulation

## Attack Module 3: Port Scan / Reconnaissance

### What This Attack Means

A port scan is a reconnaissance activity where an attacker probes multiple ports on a host or network to identify open services and weaknesses before attempting further exploitation.

### Technique Used In This Attack

- scanning many destination ports from one source
- service discovery
- reconnaissance before exploitation

Mapped technique:

- MITRE ATT&CK: `TA0043 / T1046 Network Service Discovery`

### How It Is Integrated In The Project

This module is implemented in:

- `backend/modules/port_scan.py`
- `kql-rules/port_scan_reconnaissance.kql`

It is triggered from:

- `backend/attack_simulator.py`

It reads from:

- `NetworkEvents`

### Detection Logic

The port scan module checks:

- log table must be `NetworkEvents`
- source IP is tracked
- destination ports are collected inside a short time window
- the number of unique ports is counted

Current threshold:

- `20` unique ports in `60` seconds

If the unique port count reaches the threshold, the system raises a medium-severity alert.

### How The Attack Is Read

The module reads fields such as:

- `SrcIP`
- `DstPort`
- `TimeGenerated`

By watching many different destination ports from the same source in a short interval, the system identifies reconnaissance behavior.

### How The System Defends Against It

The system helps defend by:

- detecting reconnaissance early
- identifying the attacking source IP
- recommending firewall blocking and lateral movement investigation
- turning the scan into an incident for analyst review

This matters because stopping reconnaissance early can prevent follow-on attacks.

### Alert And Incident Flow

Once detected:

- alert severity: `Medium`
- alert rule: `Port Scan / Network Reconnaissance Detected`
- incident is created
- playbook is not automatically triggered in the same way as high severity incidents

## Attack Module 4: Windows Failed Logon Burst

### What This Attack Means

This attack module focuses on repeated Windows authentication failures. It represents a Windows-specific credential attack pattern and is useful when reading local system security events.

### Technique Used In This Attack

- repeated failed Windows logons
- local or host-based credential attack activity
- burst failure pattern against a user account

Mapped technique:

- MITRE ATT&CK: `TA0006 / T1110 Brute Force`

### How It Is Integrated In The Project

This module is implemented in:

- `backend/modules/windows_failed_logon.py`
- `kql-rules/windows_failed_logon_burst.kql`

It is triggered from:

- `backend/attack_simulator.py`
- real Windows event collection via `backend/services/windows_event_collector.py`

It reads from:

- `WindowsEvent`

### Detection Logic

The Windows failed logon module checks:

- log table must be `WindowsEvent`
- event ID must be `4625`
- account and source are extracted from the event
- failed logons are counted within a time window
- if the threshold is crossed, an alert is raised

Current threshold:

- `5` failed Windows logons in `5` minutes

This module also includes cooldown logic to prevent repeated alerting for the same account and source too quickly.

### How The Attack Is Read

The module reads fields such as:

- `EventID`
- `TargetUserName`
- `SourceIp`
- `Channel`
- `Message`

The key detection anchor is:

- `EventID 4625` meaning a failed logon attempt

If these failures are repeated within the configured time window, the system marks the pattern as suspicious.

### How The System Defends Against It

The system helps defend by:

- reading Windows security failures from the host
- identifying repeated failed logon patterns
- creating a high-severity alert
- recommending account lock and host investigation
- triggering playbook response simulation

This makes the project more realistic because it can work with Windows-native telemetry instead of only synthetic cloud-style logs.

### Alert And Incident Flow

Once detected:

- alert severity: `High`
- alert rule: `Windows Failed Logon Burst Detected`
- incident is created
- playbook is triggered

## How The System Converts Attack Activity Into Alerts

For every attack module, the detection result is passed to the alert callback system.

That callback:

- creates an alert payload
- maps severity
- maps MITRE technique
- attaches evidence
- identifies the affected user or source IP

This alert is then passed to the incident manager, which creates a formal incident object for the system.

## How The System Converts Alerts Into Incidents

After a detection is confirmed:

- an incident number is created
- incident title is mapped from the rule
- severity is recorded
- evidence is attached
- affected entity is stored
- recommended action is stored
- MTTD is calculated if attack timing exists

This makes each alert actionable instead of leaving it as a raw event.

## How The Playbook Responds

For qualifying incidents, the playbook system performs simulated response automation by:

- tagging the incident as `Under Investigation`
- flagging a user account or IP for review
- simulating security team notification
- simulating ticket creation

This helps demonstrate how cybersecurity detection and response can be connected in one workflow.

## Summary

Each attack module in the project is implemented as a separate detection case with its own logic, thresholds, rule representation, and response path.

The system works by:

- reading source-specific telemetry
- identifying suspicious attack patterns
- generating alerts
- creating incidents
- simulating defensive response actions

This makes the project suitable as a modular cybersecurity monitoring and response demo that clearly shows how attacks are integrated, detected, and handled inside the platform.

