# PRESAGE — Workshop Delivery Guide

> How to teach this project as a hands-on cybersecurity workshop

---

## Workshop Overview

| Field | Details |
|---|---|
| **Workshop Title** | Build a Real-Time Threat Detection System from Scratch |
| **Subtitle** | SIEM Configuration using Python, Flask, React, and MITRE ATT&CK |
| **Duration** | 4–6 hours (half-day or full-day format) |
| **Format** | Hands-on build workshop — learners write code alongside the instructor |
| **Group Size** | 10–30 participants |
| **Mode** | In-person, virtual, or hybrid |

---

## Target Audience

This workshop is designed for:

- **Computer Science / IT students** (2nd year and above) curious about cybersecurity
- **Junior developers** who want to add security skills to their background
- **Security interns and freshers** entering SOC or SecOps roles
- **DevOps engineers** exploring the DevSecOps path
- **Workshop attendees** at hackathons, college tech fests, or corporate training programs

**No prior cybersecurity knowledge is required.** Learners need only basic Python and JavaScript familiarity.

---

## Prerequisites for Learners

Before attending, each learner should have:

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] npm installed
- [ ] A code editor (VS Code recommended)
- [ ] Git installed
- [ ] Basic Python knowledge (functions, loops, dictionaries)
- [ ] Basic JavaScript/React awareness (not required but helpful)

The workshop includes a 15-minute environment setup check at the start.

---

## Learning Outcomes

By the end of this workshop, every participant will be able to:

1. **Explain what a SIEM is** and why enterprises use it — in plain English, without jargon
2. **Describe the 6-layer SIEM pipeline** from data source to automated response
3. **Write a detection rule** using the sliding window algorithm for brute force detection
4. **Map an attack technique to MITRE ATT&CK** — understand Tactics, Techniques, and Procedures
5. **Configure a Flask backend** that ingests logs and fires real-time alerts
6. **Navigate a live threat detection dashboard** and interpret incident data
7. **Measure MTTD** — Mean Time to Detect — and articulate why it matters
8. **Trigger simulated attacks** and validate that the detection system catches them
9. **Generate an incident report** from a live SIEM session
10. **Understand the career path** from this workshop skill set into a real SOC role

---

## Skills Covered

### Technical Skills

| Skill | Depth |
|---|---|
| Python — threading, defaultdict, time-based algorithms | Intermediate |
| Flask REST API development | Beginner |
| React frontend navigation and state | Awareness |
| MITRE ATT&CK framework | Introductory |
| SIEM architecture (6-layer pipeline) | Foundational |
| Log schema design (matching enterprise formats) | Foundational |
| Threat detection rule logic | Introductory |
| MTTD/MTTR measurement | Conceptual |
| KQL detection rules for Microsoft Sentinel | Awareness |
| Incident response playbook automation | Conceptual |

### Soft Skills

- Technical presentation — explaining what you built and why
- Before/after impact framing with measurable metrics
- Security-aware developer mindset

---

## What Learners Will Build

By the end of the workshop, every participant will have a **fully working local SIEM platform** on their own machine:

```
✓  Flask backend running on http://localhost:5000
✓  React + Tailwind dashboard with 7 pages
✓  4 detection modules firing on simulated attacks
✓  Brute Force Login detection (MITRE T1110)
✓  Privilege Escalation detection (MITRE T1078)
✓  Port Scan / Reconnaissance detection (MITRE T1046)
✓  Windows Failed Logon Burst detection (MITRE T1110)
✓  Live incident queue with MTTD measurement per attack
✓  Automated playbook response for High severity incidents
✓  Downloadable incident report in JSON format
```

This is not a tutorial where you follow along and watch. You **write the detection rules yourself**, run them, and see your own attacks get caught.

---

## Session Breakdown

### Option A — 4-Hour Workshop (recommended for college events)

| Time | Session | What Happens |
|---|---|---|
| 0:00 – 0:30 | **Environment Setup** | Clone repo, install dependencies, run health check, confirm dashboard loads |
| 0:30 – 1:00 | **Problem + Architecture** | Industry stats, why SIEM exists, 6-layer pipeline walkthrough, live overview of the dashboard |
| 1:00 – 2:00 | **Build Detection Engine — Hour 1** | Write Brute Force rule (sliding window), write Privilege Escalation rule (event-based), understand the difference |
| 2:00 – 2:15 | **Break** | |
| 2:15 – 3:00 | **Build Detection Engine — Hour 2** | Write Port Scan rule (unique count), write Windows Logon Burst rule, run all 4 and confirm alerts fire |
| 3:00 – 3:30 | **Dashboard Walkthrough** | Navigate all 7 pages, trigger attacks live, read incidents, capture MTTD numbers |
| 3:30 – 4:00 | **Results + Reflection** | Before/after comparison, generate report, MTTD numbers, career paths discussion, Q&A |

---

### Option B — 6-Hour Workshop (recommended for corporate training)

| Time | Session | What Happens |
|---|---|---|
| 0:00 – 0:30 | **Environment Setup** | Clone, install, verify everything runs |
| 0:30 – 1:15 | **Threat Landscape + Problem** | Industry statistics, attack timeline, why existing tools fail small teams |
| 1:15 – 2:15 | **Architecture Deep Dive** | 6-layer pipeline, log schemas, KQL rules, MITRE ATT&CK framework |
| 2:15 – 3:15 | **Build the Detection Engine** | All 4 rules — participants write from scratch with guidance |
| 3:15 – 3:30 | **Break** | |
| 3:30 – 4:15 | **Connect the Dashboard** | Flask API, React frontend, live telemetry, attack simulation |
| 4:15 – 4:45 | **Full Demo Session** | All 4 attacks, MTTD measurement, incident report download |
| 4:45 – 5:15 | **Workshop Presentation Practice** | Each participant explains one module in 2 minutes — builds communication skills |
| 5:15 – 6:00 | **Extension + Career Paths** | How to evolve to production, Azure Sentinel migration path, SecOps job roles, Q&A |

---

## Instructor Notes

### Before the session

- Test the full run once on your own machine the day before
- Confirm all participants can run `python app.py` before starting the build section
- Have the GitHub repo link on the projector ready for everyone to clone
- Prepare a backup USB with the repo in case of connectivity issues

### During the session

- Keep talking while demonstrating — narrate every click
- When triggering attacks, pause and let participants watch the incident appear before explaining it
- Emphasise the MTTD number every time — it is the single most impressive metric
- Encourage participants to trigger attacks themselves, not just watch you

### Key talking points per module

- **Brute Force:** "5 is not arbitrary — it is NIST SP 800-63B. Every threshold in this system has a cited standard behind it."
- **Privilege Escalation:** "No counting needed — one event is enough. The event itself is the evidence."
- **Port Scan:** "Medium, not High — the attacker has not done anything yet. SIEM severity reflects impact, not just suspicion."
- **Windows Logon:** "This one can read real Windows Event Logs from the machine we are running on via PowerShell — not just simulated data."

---

## Workshop Deliverables for Participants

Each participant leaves with:

1. A working SIEM platform on their own laptop
2. 4 detection rules they wrote themselves
3. A JSON incident report from their own live demo session
4. An understanding of the MITRE ATT&CK framework in practice
5. A GitHub repository they can add to their portfolio

---

## How This Workshop Scales

| Format | Adaptation |
|---|---|
| College hackathon (90 min) | Condensed: setup + 1 rule + full demo. Pre-built repo branch available. |
| Corporate training half-day | Option A (4-hour) with emphasis on enterprise SIEM context |
| Corporate training full-day | Option B (6-hour) with extension topics and presentation practice |
| Online async course | Record each hour as a module. Participants run the repo locally. |
| Certification prep | Add KQL rules section and Azure Sentinel migration path |

---

## Why This Workshop Is Commercially Valuable

- **No existing free workshop** teaches SIEM implementation at this level — all commercial alternatives cost $500–$2,000 per seat
- **Immediately practical** — participants build a working system, not a tutorial exercise
- **Industry-aligned** — MITRE ATT&CK mapping means skills are directly transferable to enterprise roles
- **Portfolio-ready** — the GitHub repo participants build is immediately shareable with employers
- **Scalable** — the same instructor can run this for a college of 30 students or a corporate team of 20 engineers

---

## Contact

**Omkar Sakhalkar** — Wissen Infotech Cybersecurity SecOps Division  
GitHub: [github.com/Omkar-562000/PRESAGE](https://github.com/Omkar-562000/PRESAGE)
