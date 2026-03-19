# Presage SIEM Project Architecture And Objectives

## Project Background

This project was created as a working SIEM proof of concept for a mid-sized enterprise cybersecurity use case. The goal was not only to build a dashboard, but to demonstrate a practical security monitoring system that can ingest logs, detect suspicious behavior, raise incidents, and present the results through a usable web interface.

The project was shaped around a real business-oriented objective: reducing the uncertainty and delay involved in identifying security threats.

## Core Objectives Behind The Project

The project was built around the following objectives:

- centralize security visibility from multiple log sources
- detect attacks in near real time
- demonstrate measurable improvement in detection speed
- provide a usable interface for security monitoring
- simulate SOC-style alerting and incident response
- create a presentation-ready working model for review and demonstration

These objectives guided both the technology choices and the architecture of the system.

## How The Project Was Created

The project was built in stages so that each layer supported the next.

### Stage 1: Define The Security Use Case

The first step was to identify a realistic enterprise security problem:

- delayed detection of suspicious activity
- fragmented logs across systems
- lack of centralized visibility
- weak incident response visibility

From that, the project scope was narrowed to a SIEM-style solution that could simulate real-world detection and response.

### Stage 2: Build The SIEM Logic

The next step was to create the backend logic responsible for:

- generating and ingesting logs
- running attack detection logic
- converting alerts into incidents
- tracking MTTD
- triggering automated playbook actions

This created the security brain of the project.

### Stage 3: Add Attack Modules

The project was then organized around attack-focused modules so each detection case could be demonstrated clearly.

Current attack modules include:

- brute force login attack
- privilege escalation
- port scan / reconnaissance
- Windows failed logon burst

Each module was separated so that the system is easier to maintain, explain, and extend.

### Stage 4: Build The User Interface

After the backend logic was stable, the frontend was created in React and Tailwind CSS to provide:

- a branded landing page
- a main workspace interface
- a sidebar-based dashboard
- separate pages for each feature and attack module
- a dynamic presentation-ready experience

This made the project usable as a real demo product instead of just a backend prototype.

### Stage 5: Add Realistic Telemetry

To make the system more practical, real Windows Event Viewer logs were integrated using PowerShell.

This improved the realism of the project by allowing it to work with:

- simulated SIEM events
- real local Windows logs

## Main Objectives Achieved In The Current Project

The current implementation achieves the following:

- separated backend and frontend architecture
- centralized log handling
- modular attack simulation
- modular detection logic
- modular playbook automation
- live incident creation
- telemetry visibility
- Windows event ingestion
- multi-page React dashboard

## Architecture Of The Project

The project follows a separated architecture with clear responsibilities.

### 1. Frontend Layer

The frontend is built in React + Tailwind and is located in `frontend/`.

Responsibilities:

- provides the landing page
- provides the user dashboard
- displays incidents, logs, metrics, and attack modules
- communicates with the backend using API calls

Main frontend areas:

- `frontend/src/pages/`
- `frontend/src/components/`
- `frontend/src/hooks/`
- `frontend/src/lib/`

### 2. Backend Layer

The backend is built in Flask and Python and is located in `backend/`.

Responsibilities:

- exposes API endpoints
- runs background traffic generation
- processes logs
- executes detection rules
- creates incidents
- triggers playbooks
- collects Windows events

Main backend areas:

- `backend/app.py`
- `backend/siem_engine.py`
- `backend/attack_simulator.py`
- `backend/modules/`
- `backend/playbook/`
- `backend/routes/`
- `backend/services/`

### 3. Detection Layer

The detection layer is responsible for identifying suspicious behavior from incoming logs.

It currently covers:

- brute force detection
- privilege escalation detection
- port scan detection
- Windows failed logon burst detection

This layer is implemented through backend module logic and mirrored by separate KQL-style rule files.

### 4. Automation Layer

The automation layer is implemented through the playbook system in `backend/playbook/`.

Responsibilities:

- change incident status
- add playbook actions
- simulate account review
- simulate IP blocking workflows
- simulate security team notification
- simulate ticket creation

### 5. Documentation And Rule Layer

Supporting artifacts are stored in:

- `kql-rules/`
- `notes/`
- `docs/`

These help explain the system, its detections, and its purpose.

## High-Level Workflow

The project works in the following sequence:

1. logs are generated or collected
2. logs are ingested into the SIEM engine
3. detection rules analyze each event
4. alerts are generated when conditions match
5. incidents are created from alerts
6. playbook automation runs for qualifying incidents
7. the frontend displays the latest state to the user

This creates a complete demo flow from telemetry to response.

## Who This Project Is Made For

This project is made for an economic customer represented as a mid-sized enterprise that struggles with delayed threat detection and limited centralized monitoring.

The intended users are:

- security analysts
- SOC operators
- product leadership reviewing cybersecurity capabilities
- internal demo or Scrum stakeholders

It is also suitable for:

- client demonstrations
- academic or internship presentations
- cybersecurity proof-of-concept showcases

## How The User Benefits From This Project

For the target user, this project provides:

- visibility into security events in one place
- faster awareness of suspicious activity
- a clearer incident trail
- a usable interface for monitoring and demo
- a simple model of automated response behavior

Even as a prototype, it helps show how a business can move from reactive monitoring to structured security operations.

## Why This Project Matters

This project is important because it turns a security concept into a working model. Instead of describing SIEM capabilities only in theory, it demonstrates:

- how logs are collected
- how detections are triggered
- how incidents are managed
- how response actions can be automated
- how all of this can be presented to the end user through a web dashboard

That makes it useful both as a technical build and as a product demonstration.

