# Presage SIEM Project Foundation

## Project Purpose

This project is a working Security Information and Event Management (SIEM) proof of concept built for a mid-sized enterprise use case. Its purpose is to show how centralized log monitoring, attack detection, incident creation, and automated response can reduce the delay between attack activity and security team awareness.

The application is designed as a demo-ready working model that can be presented as a cybersecurity operations platform for real-time threat detection and response.

## Problem Statement

Organizations often operate with fragmented visibility across login systems, endpoint events, cloud activities, and network telemetry. Because these signals are spread across multiple sources, suspicious activity may go unnoticed for too long.

This creates several business and security problems:

- Delayed threat detection
- Increased risk of data loss and service disruption
- No unified view of alerts and incidents
- Slower response from security operations teams
- Difficulty demonstrating measurable security improvement

The project solves this by creating a centralized SIEM-style workflow that ingests logs, analyzes events, raises alerts, creates incidents, and shows the results in a web dashboard.

## Proposed Solution

The solution is a web-based SIEM prototype with a separated backend and frontend architecture.

The backend handles:

- log ingestion
- attack simulation
- detection rule execution
- incident generation
- playbook automation
- API delivery

The frontend handles:

- landing page and project branding
- dashboard navigation
- attack module pages
- incidents and telemetry views
- live state visualization for presentation and demo purposes

Together, the system demonstrates how a SOC-style platform can detect:

- brute force login attempts
- privilege escalation activity
- port scanning and reconnaissance
- Windows failed logon bursts

## Required Technologies

### Python

Python is used for the backend because it is well suited for rapid security tooling, automation, and log-processing workflows.

Why it was chosen:

- simple to build security prototypes quickly
- strong ecosystem for automation and data handling
- easy integration with Windows and scripting workflows
- clear and readable for backend rule logic

What it is used for in this project:

- SIEM engine
- attack simulator
- detection logic
- Windows log collection
- playbook automation

### Flask

Flask is the backend web framework used to expose the SIEM functionality as HTTP APIs.

Why it was chosen:

- lightweight and easy to structure
- suitable for API-first development
- simple to integrate with a React frontend
- ideal for a prototype that needs fast iteration

What it is used for in this project:

- API routes such as `/api/state`, `/api/incidents`, and `/api/attack/*`
- backend runtime entrypoint
- serving the built frontend during demo mode

### React

React is used to build the user interface for the SIEM dashboard.

Why it was chosen:

- component-based structure for scalable UI development
- suitable for multi-page dashboard experiences
- easy state-driven rendering for incidents, logs, and metrics
- widely used and presentation-friendly for modern web apps

What it is used for in this project:

- landing page
- workspace layout
- attack module pages
- incident and telemetry pages
- dynamic UI updates from backend APIs

### Tailwind CSS

Tailwind CSS is used for styling the React frontend.

Why it was chosen:

- fast UI development
- consistent styling system
- easy to create a dashboard layout with reusable utility classes
- useful for responsive layouts without heavy custom CSS overhead

What it is used for in this project:

- sidebar layout
- landing page styling
- cards, grids, panels, and workspace structure
- responsive presentation-ready UI styling

### PowerShell

PowerShell is used to collect real Windows Event Viewer logs from the local system.

Why it was chosen:

- native access to Windows event data
- practical for real local telemetry ingestion
- strong fit for Windows security operations workflows

What it is used for in this project:

- calling `Get-WinEvent`
- collecting Application, System, and Security logs
- feeding real Windows telemetry into the SIEM pipeline

### KQL-Style Rules

Kusto Query Language (KQL) is represented in this project through separate rule files to mirror real SIEM analytics rule design.

Why it was chosen:

- aligns with Microsoft Sentinel style analytics
- makes the project easier to explain in enterprise SIEM terms
- helps connect backend logic to real-world detection engineering practices

What it is used for in this project:

- documenting detection intent
- mapping each attack module to a rule definition
- supporting presentation and technical explanation

## Technology Objects and Their Purpose

### Backend Objects

- `backend/app.py`
  Main Flask application and runtime entrypoint.

- `backend/siem_engine.py`
  Core SIEM engine for log generation, ingestion, alerting, incidents, and metrics.

- `backend/attack_simulator.py`
  Orchestrates attack execution and sends logs into the SIEM engine.

- `backend/modules/`
  Holds module-specific detection and simulation logic for each attack type.

- `backend/playbook/`
  Holds automated response logic triggered after incident creation.

- `backend/routes/`
  Contains API routing logic used by the frontend.

- `backend/services/`
  Contains supporting services such as runtime management, state shaping, and Windows event collection.

### Frontend Objects

- `frontend/src/pages/`
  Separate pages for overview, incidents, telemetry, attack center, and attack modules.

- `frontend/src/components/`
  Reusable interface elements such as workspace shell and sidebar.

- `frontend/src/hooks/`
  Shared frontend state logic.

- `frontend/src/lib/`
  Utility modules such as API helpers and UI metadata.

- `frontend/src/assets/images/`
  Reserved folder for project logos and interface branding assets.

## Why This Architecture Was Chosen

The project uses a separated frontend and backend architecture because it improves clarity, scalability, and maintainability.

Reasons:

- keeps UI logic separate from security logic
- makes API testing easier
- allows the frontend to evolve independently
- makes the backend more reusable for future integrations
- creates a cleaner enterprise-style project structure

This structure also makes the project easier to explain during a presentation because each layer has a clear responsibility.

## Final Outcome

The result is a working SIEM demo platform that shows:

- centralized monitoring
- real-time detection
- incident generation
- automated response behavior
- measurable operational value through faster detection

This makes the project suitable as a working cybersecurity model for demonstration, technical review, and presentation in a Scrum or product discussion setting.

