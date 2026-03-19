import { startTransition, useEffect, useMemo, useState } from "react";
import { getState, triggerAttack } from "../lib/api";

function formatClock() {
  return new Date().toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    timeZone: "Asia/Kolkata",
  });
}

export function useSiemState() {
  const [clock, setClock] = useState(formatClock());
  const [state, setState] = useState({
    config: null,
    stats: null,
    incidents: [],
    recent_logs: [],
    logs_by_table: {},
    source_health: [],
    alert_trend: { by_severity: {}, recent_windows: [] },
    top_entities: [],
    mttd: { average: 0, records: [] },
    alerts: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [runningAttack, setRunningAttack] = useState("");

  useEffect(() => {
    const timer = window.setInterval(() => setClock(formatClock()), 1000);
    return () => window.clearInterval(timer);
  }, []);

  useEffect(() => {
    let active = true;

    const fetchState = async () => {
      try {
        const payload = await getState();
        if (!active) {
          return;
        }
        startTransition(() => {
          setState(payload);
          setError("");
          setLoading(false);
        });
      } catch (err) {
        if (!active) {
          return;
        }
        setError(err.message || "Unable to reach the SIEM backend.");
        setLoading(false);
      }
    };

    fetchState();
    const interval = window.setInterval(fetchState, 2000);
    return () => {
      active = false;
      window.clearInterval(interval);
    };
  }, []);

  async function runAttack(attackId) {
    setRunningAttack(attackId);
    try {
      await triggerAttack(attackId);
    } catch (err) {
      setError(err.message || "Attack could not be started.");
    } finally {
      window.setTimeout(() => setRunningAttack(""), 1800);
    }
  }

  const stats = useMemo(
    () =>
      state.stats || {
        total_logs: 0,
        total_alerts: 0,
        total_incidents: 0,
        high_severity: 0,
        sources_active: 4,
      },
    [state.stats],
  );

  return {
    ...state,
    stats,
    clock,
    loading,
    error,
    runningAttack,
    runAttack,
  };
}
