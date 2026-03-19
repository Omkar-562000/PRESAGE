from __future__ import annotations

import threading

from backend.attack_simulator import generate_background_traffic
from backend.services.windows_event_collector import collect_windows_events

_bg_lock = threading.Lock()
_bg_stop_event = threading.Event()
_bg_thread: threading.Thread | None = None
_windows_thread: threading.Thread | None = None


def start_background_traffic() -> bool:
    global _bg_thread, _windows_thread
    with _bg_lock:
        already_running = _bg_thread and _bg_thread.is_alive()
        _bg_stop_event.clear()
        if not already_running:
            _bg_thread = threading.Thread(
                target=generate_background_traffic,
                args=(_bg_stop_event,),
                daemon=True,
                name="siem-background-traffic",
            )
            _bg_thread.start()
        if not (_windows_thread and _windows_thread.is_alive()):
            _windows_thread = threading.Thread(
                target=collect_windows_events,
                args=(_bg_stop_event,),
                daemon=True,
                name="windows-event-collector",
            )
            _windows_thread.start()
        return not already_running


def stop_background_traffic() -> None:
    with _bg_lock:
        _bg_stop_event.set()
