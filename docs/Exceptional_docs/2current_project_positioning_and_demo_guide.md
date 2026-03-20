# Current Project Positioning And Demo Guide

## Purpose Of This Document

This document explains:

- where the current Presage project stands today
- what category of project it currently belongs to
- how to demonstrate it to a moderator
- how to show the internal logic working during a presentation

It is intended to help present the project clearly and honestly.

## What The Current Project Is

The current Presage project is a:

- working SIEM proof of concept
- cybersecurity monitoring and response demo platform
- modular attack detection dashboard
- local security operations model

It is not yet a full production security platform for live enterprise deployment.

The correct positioning is:

**Presage is a working cybersecurity SIEM prototype that demonstrates how logs are collected, analyzed, detected, converted into incidents, and handled through response logic.**

## What Category The Current Project Falls Under

The project currently falls under these categories:

- cybersecurity proof of concept
- SecOps demonstration platform
- SIEM-style monitoring tool
- incident detection and response model
- product prototype for future expansion

So when speaking to a moderator, the safest and strongest description is:

**This is a working SIEM and SecOps prototype that demonstrates real-time threat detection, incident generation, telemetry visibility, and automated response simulation.**

## What The Current Project Already Proves

The current project already proves these technical ideas:

- centralized log ingestion
- cross-source telemetry visibility
- modular attack simulation
- rule-based detection logic
- incident creation
- MTTD measurement
- playbook-style response behavior
- real Windows event ingestion
- frontend visualization of the security state

This means it is more than a static UI. It is a functioning cybersecurity system model.

## How To Explain The Project Logic To A Moderator

The simplest explanation is:

1. the system receives logs
2. the SIEM engine analyzes those logs
3. attack rules detect suspicious patterns
4. alerts are created
5. alerts become incidents
6. playbooks simulate defensive response
7. the dashboard shows everything live

This is the main logic chain you should keep repeating during the demonstration.

## Recommended Demonstration Flow

### Step 1: Start With The Product Identity

Open the landing page first and explain:

- this is Presage
- it is a cybersecurity SIEM prototype
- it is meant to demonstrate monitoring, detection, incidents, and response

### Step 2: Explain The User Problem

Tell the moderator:

- organizations struggle with delayed threat detection
- their logs are often spread across multiple systems
- Presage solves that by centralizing telemetry and detecting attacks quickly

### Step 3: Open The Workspace

Enter the main interface and explain:

- the sidebar contains each attack module and feature area
- the dashboard is split into overview, incidents, telemetry, and attack modules
- this structure mirrors a security operations workflow

### Step 4: Show Background Monitoring

Open:

- Overview
- Telemetry

Explain:

- the system is already ingesting logs
- multiple sources are active
- the platform already has a security monitoring posture before any manual attack is triggered

### Step 5: Trigger One Attack

Use one of the attack modules, for example:

- Brute Force
- Windows Failed Logon

Explain before clicking:

- this module simulates a real attack pattern
- the attack logs are sent into the SIEM engine
- the detection rule will analyze them in real time

### Step 6: Show The Detection Result

After the attack is triggered:

- open the Incidents page
- show the new incident
- explain the severity
- explain the evidence
- explain the MITRE mapping

This is where you clearly show that the project is not static. It is actually producing an alert and incident from log activity.

### Step 7: Show The Response Logic

Point out:

- status changes such as `Under Investigation`
- playbook-triggered behavior
- recommended actions
- MTTD value

Explain:

- once the rule detects the attack, the alert manager creates the incident
- for high-severity incidents, the playbook simulates response steps

### Step 8: Connect Frontend To Backend Logic

Tell the moderator clearly:

- the frontend is only displaying the output
- the actual attack logic is in the backend
- the backend modules detect patterns from logs and generate the incidents

This is an important point because it shows real system design, not just interface design.

## How To Show The Logic Working Technically

You can explain the logic using the current module structure:

- `backend/siem_engine.py`
  central telemetry and incident engine

- `backend/attack_simulator.py`
  launches attack scenarios

- `backend/modules/`
  holds attack-specific detection logic

- `backend/playbook/`
  handles automated response simulation

- `backend/routes/api.py`
  exposes the backend results to the frontend

- `frontend/`
  presents the live security state to the user

Use this sentence:

**The attack is generated in the simulator, ingested by the SIEM engine, checked by a module-level rule, converted into an incident, then displayed in the React dashboard.**

## Best Way To Demonstrate One Attack End To End

Example with brute force:

1. open Attack Center
2. click Brute Force
3. mention that repeated failed sign-ins are being generated
4. mention that `SigninLogs` are being analyzed
5. move to Incidents
6. show the high-severity brute force incident
7. mention that the playbook has changed the status to `Under Investigation`

This gives the moderator a full attack-to-response story.

## What To Emphasize During The Demo

Focus on these points:

- this is a working logic model, not just a UI
- attacks are modular and separated
- incidents are created dynamically
- response is simulated through playbooks
- telemetry is visible across multiple sources
- the architecture is separated into frontend and backend

## Honest Positioning For Moderators

Be clear that:

- it is a working prototype
- it is not yet a production enterprise deployment
- it is built to demonstrate real SIEM and SecOps logic
- it can evolve into a real product such as Presage WebShield

This honesty makes the project stronger, not weaker.

## Short Moderator Summary

If you need one short explanation, use this:

**Presage is a working SIEM proof of concept that simulates and detects cybersecurity attacks in real time, converts them into incidents, and demonstrates response logic through a modern dashboard.**
