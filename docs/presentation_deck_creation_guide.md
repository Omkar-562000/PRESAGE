# Presentation Deck Creation Guide

## Purpose Of This Document

This guide explains how to create a presentation deck for the Presage project.

It is meant to help you convert the working project into a professional presentation for:

- moderators
- reviewers
- interviewers
- internship evaluators
- Scrum or product meetings

## Presentation Goal

The main goal of the deck is to show that Presage is:

- a working cybersecurity SIEM proof of concept
- not just a dashboard UI
- capable of simulating attacks, detecting threats, generating incidents, and showing response logic

Your presentation should make the audience understand:

- what problem Presage solves
- how it works
- what has been built already
- why it matters
- how it can evolve in the future

## Recommended Deck Structure

### Slide 1: Title Slide

Include:

- Project name: `Presage`
- short subtitle such as `Cybersecurity SIEM Proof of Concept`
- your name
- organization or internship name
- date or review context

### Slide 2: Problem Statement

Explain:

- organizations face delayed threat detection
- logs are often fragmented across systems
- lack of centralized visibility increases risk
- incidents may go unnoticed for too long

Keep this slide business-focused.

### Slide 3: Project Objective

Explain what Presage aims to do:

- centralize telemetry
- detect attacks in real time
- create incidents automatically
- simulate response actions
- provide a modern security monitoring dashboard

### Slide 4: What Presage Is

Describe Presage as:

- a working SIEM proof of concept
- a SecOps demo model
- a modular threat detection platform
- a future foundation for Presage WebShield

This helps set honest expectations.

### Slide 5: Technology Stack

Show the main stack:

- Python
- Flask
- React
- Tailwind CSS
- PowerShell
- KQL-style rules

You can briefly mention why each was chosen.

### Slide 6: Architecture Overview

Explain the architecture in a simple diagram or flow:

- frontend
- backend
- SIEM engine
- attack modules
- playbook automation
- log sources

A simple block diagram works well here.

### Slide 7: Core Workflow

Show the logic flow:

1. logs are generated or collected
2. logs are ingested
3. detection rules analyze them
4. alerts are created
5. incidents are created
6. playbook actions are triggered
7. dashboard shows the result

This is one of the most important slides.

### Slide 8: Implemented Attack Modules

Show the currently supported attack modules:

- Brute Force Login
- Privilege Escalation
- Port Scan / Reconnaissance
- Windows Failed Logon Burst

Optionally add MITRE mapping beside each one.

### Slide 9: Detection Logic

Explain that each module has:

- its own backend logic
- its own thresholds
- its own rule representation
- its own incident path

This proves the modular architecture.

### Slide 10: Dashboard And UI

Show screenshots of:

- landing page
- workspace
- overview page
- incidents page
- attack center

Explain that the frontend is React-based and dynamically connected to backend APIs.

### Slide 11: Demonstration Flow

Explain the live demo steps:

1. open landing page
2. enter workspace
3. show telemetry
4. trigger attack
5. show incident creation
6. explain playbook response

This prepares the audience for the working demo.

### Slide 12: Measurable Outcomes

Show measurable value such as:

- incidents generated
- alerts detected
- MTTD improvement
- source health visibility
- live telemetry monitoring

This slide should show business impact, not just implementation details.

### Slide 13: Current Positioning

Be honest and clear:

- Presage is a working prototype
- it is not yet a full enterprise production deployment
- it demonstrates real SIEM and SecOps logic
- it is strong as a proof of concept and product foundation

### Slide 14: Future Scope

Introduce Presage WebShield as the next stage:

- website security monitoring
- ingestion APIs
- real customer telemetry
- SaaS security product direction

This helps show vision and product thinking.

### Slide 15: Conclusion

Close with:

- what was built
- what was proven
- why it matters
- what comes next

## Best Visual Style For The Deck

Use a professional style that matches the project:

- dark, clean backgrounds
- strong contrast
- limited accent colors such as blue, gold, mint
- minimal clutter
- large readable headings
- screenshots with labels

Avoid overly text-heavy slides.

## Best Content Style

For each slide:

- keep points short
- avoid long paragraphs
- focus on one message per slide
- explain logic in simple terms
- combine business meaning with technical proof

## Best Live Demo Pairing

If you are presenting the deck with the working app:

- use the deck to explain context and architecture
- use the app to prove functionality
- move from theory to live demonstration smoothly

Recommended order:

1. present slides up to architecture and workflow
2. open the live app
3. trigger attack and show incidents
4. return to final slides for outcome and future scope

## What To Say During The Demo Section

Useful lines:

- “The dashboard is not static; it is driven by backend attack and detection logic.”
- “Each attack module is implemented separately and generates its own detection path.”
- “The SIEM engine ingests logs, applies rules, creates incidents, and the playbook simulates response.”
- “This demonstrates the core workflow of a modern cybersecurity monitoring platform.”

## Final Advice

Your deck should not try to say everything.

It should do three things well:

- explain the problem
- prove the logic
- show the product value

If the audience understands those three things, the presentation will feel strong and professional.
