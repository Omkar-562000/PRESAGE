# Presage SIEM Project Security Brief

## Project Brief

This project is a cybersecurity-focused SIEM proof of concept designed to monitor security events, detect suspicious behavior, generate incidents, and simulate response actions through a centralized web platform.

It has been built as a working model of a security operations workflow, where logs are collected, attack patterns are analyzed, alerts are raised, and incidents are tracked in a structured way.

The project is not only a dashboard. Its core logic is based on security monitoring, attack detection, and incident response principles that are commonly used in real Security Operations Center (SOC) environments.

## Logic On Which The Project Is Built

The project is built on a SIEM-style logic flow:

1. collect or generate logs
2. normalize and store them in a central engine
3. analyze each event against detection rules
4. identify suspicious patterns
5. convert detections into alerts and incidents
6. trigger automated response actions when needed
7. display the security state to the user through the interface

This logic ensures that the system behaves like a real monitoring and response platform rather than a static reporting application.

## Security Logic Used In The Project

The system currently uses attack-oriented security logic for the following scenarios:

- brute force login attempts
- privilege escalation behavior
- port scan / reconnaissance activity
- Windows failed logon bursts

Each of these attack scenarios is treated as a separate detection case. The project checks incoming logs for patterns such as:

- repeated failed logins in a time window
- suspicious role assignment activity
- repeated scanning across multiple ports
- repeated Windows security failures from a user or source

When the pattern matches a rule threshold, the system raises an alert and creates an incident.

## How The Project Ensures User Safety

The project helps protect the user environment by improving awareness and response to suspicious activity.

It ensures safety in the following ways:

- gives visibility into suspicious events from multiple sources
- reduces the time required to notice attack behavior
- groups detections into incidents for easier investigation
- records evidence connected to the incident
- simulates response actions through playbooks
- supports better operational security decisions

Although this is a prototype, the safety value comes from the fact that it is designed to detect risky behavior early and present it in a clear, actionable way.

## How It Is Carried Out As A Cybersecurity Project

This project qualifies as a cybersecurity project because its main purpose is the detection and management of security threats.

It includes key cybersecurity functions such as:

- security event monitoring
- threat detection
- incident management
- log correlation
- rule-based analysis
- automated response simulation
- Windows event visibility
- KQL-style rule representation

These are all core concepts of modern defensive security engineering and SOC operations.

The project is therefore carried out as a cybersecurity project in both design and implementation.

## Cybersecurity Components In The Project

### 1. Log Monitoring

The project monitors multiple log sources, including simulated enterprise telemetry and real Windows Event Viewer logs.

This supports:

- visibility
- event review
- central analysis

### 2. Threat Detection

The system applies detection logic against incoming logs to identify indicators of attack behavior.

This supports:

- early warning
- attack pattern recognition
- structured alert generation

### 3. Incident Handling

Detected attacks are converted into incidents instead of being left as isolated events.

This supports:

- investigation workflow
- severity tracking
- incident status management

### 4. Playbook Automation

The playbook layer simulates automated security response behavior.

This supports:

- incident state updates
- simulated account review
- simulated IP blocking workflows
- simulated notification and ticketing

### 5. User-Facing Security Dashboard

The frontend gives the user a centralized view of the current security posture.

This supports:

- rapid situational awareness
- incident visibility
- telemetry review
- attack demonstration and training

## Why The Project Is Useful

The project is useful because it converts security monitoring concepts into a visible and understandable system.

It helps users:

- understand what attacks are happening
- understand how the system detects them
- understand how incidents are created
- understand how response automation works

This makes it suitable for:

- cybersecurity demonstrations
- proof-of-concept reviews
- internship or academic presentations
- internal product or Scrum discussions

## Final Summary

This project is built on practical SIEM and SOC logic. It ensures user safety by detecting suspicious behavior, creating incidents, and simulating security response actions in a centralized interface.

Because it focuses on monitoring, detection, incident management, and response, it is correctly carried out as a cybersecurity project and can be presented as a working security operations model.

