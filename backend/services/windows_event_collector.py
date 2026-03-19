from __future__ import annotations

import json
import subprocess
import time

from backend.siem_engine import ingest_log

WINDOWS_LOG_CHANNELS = ["Application", "System", "Security"]
MAX_EVENTS_PER_POLL = 8
POLL_INTERVAL_SECONDS = 12

_channel_watermarks = {channel: 0 for channel in WINDOWS_LOG_CHANNELS}


def _powershell_json_command(channel: str) -> list[dict]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        (
            f"Get-WinEvent -LogName '{channel}' -MaxEvents {MAX_EVENTS_PER_POLL} -ErrorAction SilentlyContinue | "
            "Select-Object "
            "@{Name='TimeGenerated';Expression={$_.TimeCreated.ToString('o')}},"
            "@{Name='Channel';Expression={$_.LogName}},"
            "@{Name='EventID';Expression={$_.Id}},"
            "@{Name='RecordId';Expression={$_.RecordId}},"
            "@{Name='Provider';Expression={$_.ProviderName}},"
            "@{Name='Level';Expression={$_.LevelDisplayName}},"
            "@{Name='MachineName';Expression={$_.MachineName}},"
            "@{Name='Message';Expression={if ($_.Message) { $_.Message.Substring(0, [Math]::Min($_.Message.Length, 280)) } else { '' }}},"
            "@{Name='Keywords';Expression={$_.KeywordsDisplayNames -join ', '}} | "
            "ConvertTo-Json -Compress"
        ),
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=15, check=False)
    if result.returncode != 0:
        return []
    payload = result.stdout.strip()
    if not payload:
        return []
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return []
    if isinstance(parsed, dict):
        return [parsed]
    if isinstance(parsed, list):
        return parsed
    return []


def _normalize_event(raw: dict) -> dict:
    message = raw.get("Message") or ""
    return {
        "TimeGenerated": raw.get("TimeGenerated"),
        "Channel": raw.get("Channel"),
        "EventID": raw.get("EventID"),
        "RecordId": raw.get("RecordId"),
        "Provider": raw.get("Provider"),
        "Level": raw.get("Level") or "Informational",
        "Computer": raw.get("MachineName"),
        "Message": message,
        "Keywords": raw.get("Keywords") or "",
        "table": "WindowsEvent",
    }


def collect_windows_events(stop_event):
    while not stop_event.is_set():
        for channel in WINDOWS_LOG_CHANNELS:
            raw_events = _powershell_json_command(channel)
            if not raw_events:
                continue
            for raw_event in sorted(raw_events, key=lambda item: item.get("RecordId", 0)):
                record_id = int(raw_event.get("RecordId") or 0)
                if record_id <= _channel_watermarks[channel]:
                    continue
                ingest_log(_normalize_event(raw_event))
                _channel_watermarks[channel] = record_id
        time.sleep(POLL_INTERVAL_SECONDS)
