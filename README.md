# Presage SIEM Prototype

A working SIEM proof of concept with a separated backend and frontend structure.

## What This Project Is

- Backend: Flask API + SIEM engine + attack simulator
- Frontend: React + Tailwind multi-page dashboard
- Purpose: demonstrate real-time threat detection, incident creation, telemetry visibility, and measurable MTTD improvement

## Structure

```text
WISE-09/
+-- backend/
|   +-- app.py
|   +-- config.py
|   +-- siem_engine.py
|   +-- attack_simulator.py
|   +-- playbook/
|   +-- routes/
|   +-- services/
|   +-- core/        # legacy helpers kept for reference
+-- frontend/
|   +-- package.json
|   +-- dist/
|   +-- src/
|       +-- components/
|       +-- hooks/
|       +-- lib/
|       +-- pages/
+-- app.py
+-- siem.py
+-- siem_engine.py
+-- attack_simulator.py
+-- requirements.txt
```

## Active Runtime

- Main backend entry: `app.py`
- Backend package implementation: `backend/`
- Main frontend dashboard: `frontend/`
- Optional CLI runner: `siem.py`
- Active playbook automation: `backend/playbook/`
- Legacy helper package: `backend/core/`

The root `app.py`, `siem_engine.py`, and `attack_simulator.py` now act as compatibility wrappers around the real backend package.

The `backend/core/` package is retained only for legacy helper/reporting code and is not used by the main web runtime.

## Standard SIEM Features Added

- Multi-page dashboard
- Incident search and filtering
- Source health monitoring
- Alert severity trend panel
- Top affected entity summary
- Telemetry source filtering
- Attack simulation controls
- Windows Event Viewer ingestion

## Run The App

### 1. Install backend dependencies

```powershell
python -m pip install -r requirements.txt
```

### 2. Install frontend dependencies

```powershell
D:\Nodejs\Nodejs\npm.cmd --prefix frontend install
```

### 3. Build the React frontend

```powershell
D:\Nodejs\Nodejs\npm.cmd --prefix frontend run build
```

### 4. Start the app

```powershell
python app.py
```

Open `http://localhost:5000`

## Development Mode

Backend:

```powershell
python app.py
```

Frontend:

```powershell
D:\Nodejs\Nodejs\npm.cmd --prefix frontend run dev
```

Open `http://localhost:5173`

## Optional CLI Runner

```powershell
python siem.py
```

This starts the same backend and gives you a console menu for launching attacks and saving a report snapshot.

