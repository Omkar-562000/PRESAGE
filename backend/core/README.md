Legacy backend helpers live here.

This package is not part of the active Flask + React runtime.

Current runtime paths:
- `backend/app.py`
- `backend/siem_engine.py`
- `backend/attack_simulator.py`
- `backend/playbook/`
- `backend/routes/`
- `backend/services/`

Why this folder still exists:
- It preserves earlier CLI/reporting utilities.
- It keeps older prototype code available for reference.
- It avoids breaking historical imports while the current app uses the newer backend flow.

If we do a deeper cleanup later, this folder can be archived or selectively merged.

