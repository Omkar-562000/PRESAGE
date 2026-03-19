# Presage WebShield Product Roadmap

## Product Vision

Presage WebShield is the future product direction of the current Presage SIEM project. It is designed to become a cybersecurity monitoring and response tool for customer-facing websites and web applications.

The idea is to evolve the current SIEM proof of concept into a practical product that can help economic customers protect their websites from attacks such as credential abuse, suspicious admin activity, bot traffic, API abuse, and reconnaissance.

## What Presage WebShield Will Be

Presage WebShield will be a web security operations platform that:

- ingests website and application activity
- detects attack patterns in real time
- creates alerts and incidents
- helps business users and analysts respond quickly
- provides visibility into website security posture

This makes it suitable for:

- e-commerce websites
- SaaS platforms
- admin portals
- customer dashboards
- fintech and service websites

## Why This Product Is Valuable

Many businesses cannot afford a full Security Operations Center, but they still face risks such as:

- brute force login attacks
- account takeover attempts
- admin misuse
- bot abuse
- suspicious API traffic
- reconnaissance against exposed services

Presage WebShield would give those businesses:

- one place to monitor security events
- faster threat detection
- lightweight incident response
- practical visibility without enterprise SIEM complexity

## Current Project As The Foundation

The current Presage project already provides a strong starting foundation:

- centralized telemetry handling
- detection logic
- modular attack simulation
- incident creation
- playbook automation
- React dashboard
- Windows event integration

To become WebShield, the next step is to connect this platform to real website and application telemetry.

## Product Roadmap

### Phase 1: MVP

Goal:

- turn Presage into a working website-focused security monitoring prototype

Main features:

- website log ingestion API
- authentication event ingestion
- admin action ingestion
- failed login detection
- brute force detection
- suspicious IP detection
- basic bot and abuse monitoring
- incident dashboard for website threats
- email or Slack notifications
- simple playbook responses

Key modules:

- Auth Security
- Admin Activity Monitor
- Incident Center
- Telemetry Viewer

Recommended technical additions:

- web event ingestion endpoint
- application event schema
- database-backed storage for logs and incidents
- website integration middleware or SDK

### Phase 2: Production-Ready Platform

Goal:

- make the system usable for real customer websites continuously

Main features:

- persistent alert and incident storage
- alert deduplication
- multi-user access
- role-based views
- API abuse monitoring
- suspicious geo and device login tracking
- signup abuse detection
- audit trails
- exportable reports
- stronger playbook workflows

Key modules:

- Bot and Abuse Detection
- API Threat Monitoring
- Threat Intel Enrichment
- Response Automation

Recommended integrations:

- nginx logs
- apache logs
- node or express apps
- django or flask apps
- php or laravel apps
- cloud firewall or CDN logs

### Phase 3: SaaS Product Version

Goal:

- make Presage WebShield a business-ready cybersecurity product

Main features:

- hosted cloud deployment
- tenant-based customer separation
- onboarding flow
- pricing and package model
- custom alerting policies
- executive summary dashboards
- customer-specific rule packs
- security posture analytics
- cross-customer product maturity

Advanced features:

- anomaly detection
- behavior analytics
- risk scoring
- attack trend analytics
- compliance or audit summaries
- managed response workflows

## Recommended Website Attack Detection Pack

For the first real product version, Presage WebShield should support:

- brute force login attempts
- credential stuffing patterns
- suspicious admin login behavior
- repeated password reset abuse
- API rate abuse
- bot or fake account creation abuse
- repeated 401 and 403 attack patterns
- reconnaissance and port scan activity

These are practical, explainable, and useful to real businesses.

## Recommended Architecture For WebShield

### Frontend

The frontend should remain a React dashboard and evolve into:

- customer security overview
- auth risk module
- admin actions module
- API risk page
- incident center
- reports and exports

### Backend

The backend should be expanded into:

- ingestion service
- normalization service
- detection engine
- incident management service
- playbook service
- notification service
- tenant and user management

### Data Flow

1. website or app sends events
2. Presage receives the events
3. events are normalized into a common schema
4. rules analyze them
5. alerts are created
6. incidents are opened
7. playbook actions are triggered
8. the frontend updates for the customer

## Immediate Next Build Priorities

The best next steps to move from the current project to WebShield are:

1. create a website event schema
2. create a web ingestion API
3. add persistent storage
4. add website-specific detection rules
5. add account lock and IP block playbooks
6. add dashboard sections for website security telemetry

## Final Summary

Presage WebShield is the natural product evolution of the current Presage SIEM project. The current platform already proves the core logic of detection, incidents, and response. The roadmap focuses on transforming that logic into a real cybersecurity tool for business websites and web applications.

This makes the current project not just a demo, but a foundation for a real security product.
