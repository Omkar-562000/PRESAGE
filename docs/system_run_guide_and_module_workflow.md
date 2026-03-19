# Presage SIEM System Run Guide And Module Workflow

## Purpose Of This Document

This document explains how to run the project step by step and describes what each major module does in the system.

It is intended for:

- project reviewers
- demo presenters
- developers maintaining the project
- users who want to understand how the application works internally

## Before You Start

Make sure the following are available on the machine:

- Python installed
- Node.js and npm installed
- Windows environment available for PowerShell-based Windows log collection

## Step-By-Step Guide To Run The System

### Step 1: Open The Project Folder

Open a terminal in the project root:

```powershell
cd E:\Intership\PRESAGE-09
```

### Step 2: Install Backend Dependencies

Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

What this step does:

- installs Flask
- installs Faker
- installs backend runtime dependencies required by the SIEM engine

### Step 3: Install Frontend Dependencies

Install React frontend dependencies:

```powershell
npm --prefix frontend install
```

What this step does:

- installs React
- installs Vite
- installs Tailwind-related packages
- installs frontend UI dependencies

### Step 4: Choose How You Want To Run The Frontend

#### Option A: Integrated demo mode

Build the production frontend:

```powershell
npm --prefix frontend run build
```

What this step does:

- compiles the React + Tailwind frontend
- creates the `frontend/dist` output
- makes the frontend available for Flask to serve

Then start the system:

```powershell
python app.py
```

Open:

```text
http://localhost:5000
```

#### Option B: Frontend development mode

Start the backend:

```powershell
python app.py
```

In another terminal, start the React dev server:

```powershell
cd frontend
npm run start
```

Open:

```text
http://localhost:5173
```

## Optional Way To Run The System

You can also run:

```powershell
python siem.py
```

What this does:

- starts the same backend system
- provides a CLI menu for manually launching attack simulations
- allows report snapshot generation from the terminal

## What Starts Automatically When The System Runs

When `python app.py` starts the system, the following happen automatically:

- Flask API becomes available
- React frontend is served in integrated mode
- background benign traffic generation begins
- Windows Event Viewer collection begins
- attack detections remain active
- incidents and metrics become available through the API and UI

## Main Working Flow Of The System

The system works in the following sequence:

1. logs are generated or collected
2. logs are ingested into the SIEM engine
3. detection rules inspect the logs
4. alerts are created when thresholds are matched
5. incidents are created from alerts
6. playbook actions run for qualifying incidents
7. the frontend displays the updated security state

## What Each Backend Module Does

### `app.py`

Purpose:

- main project entrypoint

How it works:

- loads the backend Flask application
- starts background traffic when the app runs
- gives a simple root startup command for the project

### `backend/app.py`

Purpose:

- active Flask application

How it works:

- registers API routes
- serves frontend assets from `frontend/dist` in integrated mode
- starts runtime services before requests

### `backend/siem_engine.py`

Purpose:

- central SIEM engine of the project

How it works:

- defines log tables
- generates simulated log events
- stores logs centrally
- runs detection engine logic
- creates alerts and incidents
- tracks MTTD and platform statistics

### `backend/attack_simulator.py`

Purpose:

- attack orchestration layer

How it works:

- provides functions to simulate attack modules
- sends attack logs into the SIEM engine
- receives alert callbacks
- converts detections into incidents
- triggers playbook actions

### `backend/modules/`

Purpose:

- stores attack-specific detection and simulation logic

How it works:

- each file handles one attack type
- each module contains the logic to analyze logs for that attack
- each module can also simulate the attack pattern for demo use

Current files:

- `brute_force.py`
- `privilege_escalation.py`
- `port_scan.py`
- `windows_failed_logon.py`

### `backend/playbook/`

Purpose:

- automated response simulation

How it works:

- receives created incidents
- updates incident status
- simulates account or IP review workflows
- simulates notification and ticket generation

### `backend/routes/api.py`

Purpose:

- API access layer

How it works:

- exposes routes for health, state, logs, alerts, incidents, MTTD, and attacks
- provides POST endpoints to trigger attack modules
- provides GET endpoints for frontend data consumption

### `backend/services/runtime.py`

Purpose:

- controls system background services

How it works:

- starts simulated background traffic
- starts Windows event collection
- manages stop/start behavior for runtime threads

### `backend/services/state_service.py`

Purpose:

- shapes backend data for the frontend

How it works:

- builds state payloads
- organizes logs by source
- creates summaries like source health, alert trend, and top entities

### `backend/services/windows_event_collector.py`

Purpose:

- real Windows telemetry ingestion

How it works:

- uses PowerShell `Get-WinEvent`
- reads Application, System, and Security logs
- normalizes them into the project's `WindowsEvent` format
- ingests them into the SIEM engine

### `backend/config.py`

Purpose:

- shared configuration and rule metadata

How it works:

- stores frontend build paths
- stores rule definitions and display information

### `backend/core/`

Purpose:

- legacy helper code kept for reference

How it works:

- not part of the active web runtime
- preserved for historical reporting or older prototype logic

## What Each Frontend Module Does

### `frontend/src/App.jsx`

Purpose:

- main frontend routing layer

How it works:

- defines routes for landing page, workspace pages, and attack module pages

### `frontend/src/pages/`

Purpose:

- page-level views

How it works:

- each file represents a major screen in the dashboard
- includes overview, incidents, telemetry, attack center, and module pages

### `frontend/src/components/`

Purpose:

- reusable UI components

How it works:

- provides layout and visualization components such as sidebar, cards, panels, and grids

### `frontend/src/hooks/useSiemState.js`

Purpose:

- shared frontend data loading logic

How it works:

- requests live backend state
- keeps frontend pages updated with incidents, logs, and metrics

### `frontend/src/lib/api.js`

Purpose:

- frontend API helper layer

How it works:

- contains reusable functions for calling backend endpoints

### `frontend/src/lib/ui.js`

Purpose:

- frontend UI metadata and configuration

How it works:

- stores module definitions and shared UI data used across pages

### `frontend/src/assets/images/`

Purpose:

- branding assets

How it works:

- stores project logos and interface images

## What Each Attack Module Does

### Brute Force Module

File:

- `backend/modules/brute_force.py`

What it does:

- watches sign-in failures
- counts repeated failed login attempts for a user
- raises an alert when threshold is crossed

How it works:

- reads `SigninLogs`
- checks `ResultType`
- groups failures in a 5-minute window
- alerts after 5 failures

### Privilege Escalation Module

File:

- `backend/modules/privilege_escalation.py`

What it does:

- watches for suspicious cloud role assignment activity
- raises a high-severity alert for admin assignment behavior

How it works:

- reads `AzureActivity`
- checks `OperationName`
- alerts when role assignment write activity is seen

### Port Scan Module

File:

- `backend/modules/port_scan.py`

What it does:

- watches for reconnaissance behavior from one source IP
- alerts when many unique ports are scanned in a short period

How it works:

- reads `NetworkEvents`
- tracks `SrcIP` and `DstPort`
- counts unique ports in a 60-second window
- alerts after 20 unique ports

### Windows Failed Logon Module

File:

- `backend/modules/windows_failed_logon.py`

What it does:

- watches Windows failed authentication events
- detects repeated failed logon bursts

How it works:

- reads `WindowsEvent`
- checks for `EventID 4625`
- groups failures by account and source
- alerts after 5 failures in 5 minutes

## How The Frontend Uses These Modules

The frontend does not run attack logic directly. Instead, it:

- calls backend APIs
- receives state updates
- shows attack modules as separate pages
- displays incidents, logs, source health, trends, and telemetry

This keeps the frontend focused on user interaction and keeps the backend responsible for cybersecurity logic.

## How To Understand The System During A Demo

If you are presenting the system, the easiest explanation flow is:

1. start the app
2. open the landing page
3. enter the workspace
4. show overview metrics
5. open telemetry and incidents
6. trigger one attack module
7. show how logs become incidents
8. explain how playbook actions respond

This demonstrates both the technical working model and the cybersecurity value of the project.

## Final Summary

The project is run through a simple startup process, but internally it is composed of multiple focused modules that work together:

- backend for detection and response
- frontend for visibility and interaction
- attack modules for cybersecurity scenarios
- runtime services for live telemetry
- playbook logic for simulated response

This structure makes the project both runnable and explainable, which is important for a cybersecurity proof of concept.
