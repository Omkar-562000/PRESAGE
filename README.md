# Presage

> Cybersecurity SIEM proof of concept for real-time threat detection, incident generation, telemetry visibility, and automated response simulation.

Presage is a working SecOps demo platform built with a React frontend and Flask backend. It shows how security telemetry can be collected, analyzed, converted into incidents, and presented through a polished multi-page dashboard.

It is suitable for:

- cybersecurity demonstrations
- academic and internship presentations
- product prototype reviews
- future evolution into **Presage WebShield** for website security operations

## Highlights

- multi-source telemetry monitoring
- modular attack simulation
- MITRE-aligned detection logic
- incident creation and MTTD tracking
- playbook-style automated response simulation
- Windows Event Viewer ingestion
- React + Tailwind multi-page dashboard

## Implemented Attack Modules

- Brute Force Login
- Privilege Escalation
- Port Scan / Reconnaissance
- Windows Failed Logon Burst

## Tech Stack

### Backend

- Python
- Flask
- PowerShell integration for Windows event collection
- Faker for simulated telemetry

### Frontend

- React
- Vite
- Tailwind CSS
- React Router

### Security Concepts Used

- SIEM-style log ingestion
- MITRE ATT&CK-aligned detection mapping
- incident lifecycle modeling
- playbook response simulation
- Windows security telemetry visibility

## Project Structure

```text
PRESAGE-09/
+-- backend/
|   +-- app.py
|   +-- config.py
|   +-- siem_engine.py
|   +-- attack_simulator.py
|   +-- modules/
|   +-- playbook/
|   +-- routes/
|   +-- services/
|   +-- core/        # legacy/reference helpers
+-- docs/
+-- frontend/
|   +-- package.json
|   +-- src/
|   |   +-- components/
|   |   +-- hooks/
|   |   +-- lib/
|   |   +-- pages/
|   +-- dist/        # generated after build
+-- kql-rules/
+-- app.py
+-- siem.py
+-- requirements.txt
```

## Active Runtime

Main runtime files:

- `app.py` - root entrypoint for the integrated app
- `backend/app.py` - Flask backend application
- `backend/siem_engine.py` - SIEM engine and incident model
- `backend/attack_simulator.py` - attack simulation orchestration
- `frontend/` - React dashboard

Legacy/reference area:

- `backend/core/` is retained only for older helper and reporting code and is not part of the active web runtime.

## Prerequisites

Before running Presage locally, make sure you have:

- Python 3.11+ installed
- Node.js 18+ installed
- npm installed
- Windows PowerShell available
- Git installed if you want to clone the repository

Recommended:

- a Windows machine, because the project can collect real Windows Event Viewer logs using PowerShell

## How To Clone The Repository

Replace the repository URL with your actual GitHub repository URL.

```powershell
git clone <your-repository-url>
cd PRESAGE-09
```

Example:

```powershell
git clone https://github.com/your-username/presage.git
cd PRESAGE-09
```

## Installation

### 1. Install backend dependencies

```powershell
python -m pip install -r requirements.txt
```

### 2. Install frontend dependencies

```powershell
npm --prefix frontend install
```

If your environment requires the explicit npm path, you can also run:

```powershell
D:\Nodejs\Nodejs\npm.cmd --prefix frontend install
```

## Run Options

### Option 1: Integrated App Mode

This is the recommended mode for demos, presentations, and full application use.

#### Build the frontend

```powershell
npm --prefix frontend run build
```

#### Start the backend

```powershell
python app.py
```

#### Open the app

```text
http://localhost:5000
```

What happens in this mode:

- Flask starts the backend
- the built React frontend is served from `frontend/dist`
- background telemetry starts automatically
- Windows event collection starts automatically
- the full Presage UI is available from one URL

### Option 2: Frontend Development Mode

Use this when actively editing the React UI.

#### Terminal 1: Start backend

```powershell
python app.py
```

#### Terminal 2: Start frontend dev server

```powershell
cd frontend
npm run start
```

#### Open the frontend dev app

```text
http://localhost:5173
```

What happens in this mode:

- Flask still serves the backend APIs on port `5000`
- Vite serves the React frontend on port `5173`
- React changes update with hot reload during development

### Optional CLI Demo Mode

```powershell
python siem.py
```

This starts the same backend and gives you a terminal menu for launching attack simulations and saving a report snapshot.

## How To Test The Project Quickly

### Backend health test

```powershell
python -c "from app import app; c=app.test_client(); print(c.get('/api/health').status_code); print(c.get('/api/state').status_code); print(c.get('/api/config').status_code)"
```

Expected result:

- `200`
- `200`
- `200`

### Frontend build test

```powershell
npm --prefix frontend run build
```

### Manual application test

1. Open the landing page.
2. Enter the workspace.
3. Open `Overview` and `Telemetry`.
4. Go to `Attack Center`.
5. Trigger one attack module.
6. Open `Incidents`.
7. Confirm that a new incident appears.
8. For high-severity incidents, confirm the status changes to `Under Investigation`.

## What To Show In A Demo

Recommended presentation flow:

1. Open the landing page and introduce Presage.
2. Open the workspace and explain the dashboard layout.
3. Show the `Overview` page to explain telemetry and incident visibility.
4. Show the `Telemetry` page to prove logs are actively being processed.
5. Trigger one attack from `Attack Center`.
6. Open `Incidents` and show the resulting incident.
7. Explain the playbook response and MTTD value.

## Documentation

See [docs/index.md](docs/index.md) for the full documentation map.

## Current Project Positioning

Presage should currently be presented as:

**a working SIEM and SecOps proof of concept**

It is suitable for:

- cybersecurity demonstrations
- academic and internship presentations
- product prototype reviews
- future expansion into a real web security product

It should not be presented as a full production enterprise SIEM deployment.

## Future Direction

Presage can evolve into **Presage WebShield**, a website-focused cybersecurity monitoring and response platform for business websites and web applications.

## License / Usage Note

Add your preferred license here if you plan to publish the repository publicly.
