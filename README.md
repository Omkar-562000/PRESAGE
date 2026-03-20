# Presage

> Cybersecurity SIEM proof of concept for real-time threat detection, incident generation, telemetry visibility, and automated response simulation.

---

## 🎬 Demo Video

📽 **[Watch Full Demo on Google Drive](YOUR_DRIVE_LINK_HERE)**

> Replace `YOUR_DRIVE_LINK_HERE` with your actual Google Drive share link after recording.

The demo video covers: project explanation · workflow walkthrough · live attack simulation · code overview · workshop learning outcomes.

---

## Overview

Presage is a working SecOps demo platform built with a React frontend and Flask backend. It shows how security telemetry can be collected, analysed, converted into incidents, and presented through a polished multi-page dashboard.

It is suitable for:

- Cybersecurity demonstrations and internship presentations
- Academic and product prototype reviews
- Hands-on workshop delivery for students and developers
- Future evolution into **Presage WebShield** for website security operations

---

## Highlights

- Multi-source telemetry monitoring across 4 log types
- 4 MITRE ATT&CK-aligned attack simulation modules
- Real-time incident creation with MTTD measurement
- Automated playbook response for High severity incidents
- Windows Event Viewer integration via PowerShell
- React + Tailwind multi-page dashboard — 7 pages
- CLI demo mode via `python siem.py`

---

## Attack Modules

| Module | MITRE Technique | Severity | Detection Logic |
|---|---|---|---|
| Brute Force Login | T1110 — Credential Access | High | 5 failed logins per user in 5-minute window |
| Privilege Escalation | T1078 — Privilege Escalation | High | Single roleAssignments/write event — immediate |
| Port Scan / Reconnaissance | T1046 — Reconnaissance | Medium | 20 unique ports from same IP within 60 seconds |
| Windows Failed Logon Burst | T1110 — Credential Access | High | 5 Event ID 4625 failures in 5-minute window |

---

## Tech Stack

### Backend
- Python 3.11+
- Flask 3.x
- Faker 24.x — realistic telemetry simulation
- psutil — real system metrics
- PowerShell integration for Windows Event Viewer

### Frontend
- React 18
- Vite
- Tailwind CSS
- React Router

### Security Concepts
- SIEM-style log ingestion across 4 data sources
- MITRE ATT&CK-aligned detection rules
- Incident lifecycle modelling with MTTD measurement
- Automated playbook response simulation
- Windows security telemetry ingestion

---

## Project Structure

```
PRESAGE/
├── backend/
│   ├── app.py                  Flask application and routes
│   ├── config.py               Configuration settings
│   ├── siem_engine.py          Detection engine and incident model
│   ├── attack_simulator.py     Attack simulation orchestration
│   ├── modules/                Detection rule modules
│   ├── playbook/               Automated response playbooks
│   ├── routes/                 API route handlers
│   └── services/               Business logic services
├── docs/
│   ├── index.md                Documentation map
│   └── workshop.md             Workshop delivery guide
├── frontend/
│   ├── package.json
│   └── src/
│       ├── components/         Reusable UI components
│       ├── hooks/              Custom React hooks
│       ├── lib/                Utilities
│       └── pages/              Dashboard pages
├── kql-rules/                  Microsoft Sentinel KQL detection queries
├── app.py                      Root entrypoint
├── siem.py                     CLI demo mode
└── requirements.txt            Python dependencies
```

---

## Prerequisites

Before running Presage locally, make sure you have:

- Python 3.11+ installed
- Node.js 18+ installed
- npm installed
- Git installed
- Windows PowerShell available (Windows only — enables real Event Viewer ingestion)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Omkar-562000/PRESAGE
cd PRESAGE
```

### 2. Install backend dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Install frontend dependencies

```bash
npm --prefix frontend install
```

---

## Run Options

### Option 1 — Integrated App Mode (recommended for demos)

This is the recommended mode for demonstrations and presentations.

#### Step 1: Build the frontend

```bash
npm --prefix frontend run build
```

#### Step 2: Start the backend

```bash
python app.py
```

#### Step 3: Open the app

```
http://localhost:5000
```

What happens in this mode:
- Flask starts the backend and serves the built React frontend
- Background telemetry generation starts automatically
- Windows event collection starts automatically (Windows machines only)
- The full 7-page PRESAGE dashboard is available from one URL

---

### Option 2 — Frontend Development Mode

Use this when actively editing the React UI.

#### Terminal 1: Start backend

```bash
python app.py
```

#### Terminal 2: Start frontend dev server

```bash
cd frontend
npm run start
```

#### Open the dev app

```
http://localhost:5173
```

---

### Option 3 — CLI Demo Mode

```bash
python siem.py
```

Starts the platform with a terminal menu for triggering attacks, viewing incidents, and saving report snapshots. Useful for live command-line demonstrations.

---

## Quick Health Check

```bash
python -c "from app import app; c=app.test_client(); print(c.get('/api/health').status_code); print(c.get('/api/state').status_code)"
```

Expected output: `200` for each endpoint.

---

## Demo Flow

Recommended live demonstration sequence:

1. Open the landing page — introduce PRESAGE
2. Navigate to Overview — show live KPI stats and log stream
3. Open Telemetry — prove logs are actively being ingested
4. Go to Attack Center — trigger Brute Force Login
5. Open Incidents — show incident with MTTD in seconds
6. Show MTTD comparison — before: 4–6 hours, after: seconds
7. Trigger remaining 3 modules — Privilege Escalation, Port Scan, Windows Logon Burst
8. Download the incident report from Reports page

---

## Workshop Delivery

See [`docs/workshop.md`](docs/workshop.md) for the full workshop delivery guide.

**Quick summary:**
- **Target audience:** CS/IT students, junior developers, security interns
- **Duration:** 4–6 hours (half-day workshop)
- **What learners build:** A fully working SIEM platform with 4 MITRE-mapped detection modules and live dashboard
- **Prerequisites:** Basic Python and JavaScript knowledge

---

## Documentation

- [`docs/index.md`](docs/index.md) — full documentation map
- [`docs/workshop.md`](docs/workshop.md) — workshop delivery guide
- [`kql-rules/`](kql-rules/) — Microsoft Sentinel KQL detection queries

---

## Project Positioning

Presage should be presented as **a working SIEM and SecOps proof of concept** suitable for:

- Cybersecurity demonstrations and academic presentations
- Internship project reviews
- Hands-on workshop delivery
- Foundation for future expansion into Presage WebShield

It is not positioned as a full production enterprise SIEM deployment.

---

## Future Direction

Presage can evolve into **Presage WebShield** — a website-focused cybersecurity monitoring and response platform for business websites and web applications.

---

## License

MIT License — free to use, modify, and redistribute.

See [LICENSE](LICENSE) for full terms.

---

## Author

**Omkar Sakhalkar** — Cybersecurity SecOps Intern, Wissen Infotech

GitHub: [github.com/Omkar-562000/PRESAGE](https://github.com/Omkar-562000/PRESAGE)