import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { WorkspaceShell } from "./components/WorkspaceShell";
import { useSiemState } from "./hooks/useSiemState";
import { AttackLabPage } from "./pages/AttackLabPage";
import { IncidentsPage } from "./pages/IncidentsPage";
import { LandingPage } from "./pages/LandingPage";
import { OverviewPage } from "./pages/OverviewPage";
import { ReportsPage } from "./pages/ReportsPage";
import { TelemetryPage } from "./pages/TelemetryPage";
import { BruteForcePage } from "./pages/modules/BruteForcePage";
import { PortScanPage } from "./pages/modules/PortScanPage";
import { PrivilegeEscalationPage } from "./pages/modules/PrivilegeEscalationPage";
import { WindowsFailedLogonPage } from "./pages/modules/WindowsFailedLogonPage";

export default function App() {
  const siem = useSiemState();

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/workspace" element={<WorkspaceShell siem={siem} />}>
          <Route index element={<OverviewPage siem={siem} />} />
          <Route path="incidents" element={<IncidentsPage siem={siem} />} />
          <Route path="telemetry" element={<TelemetryPage siem={siem} />} />
          <Route path="reports" element={<ReportsPage siem={siem} />} />
          <Route path="attack-center" element={<AttackLabPage siem={siem} />} />
          <Route path="modules/brute-force" element={<BruteForcePage siem={siem} />} />
          <Route path="modules/privilege-escalation" element={<PrivilegeEscalationPage siem={siem} />} />
          <Route path="modules/port-scan" element={<PortScanPage siem={siem} />} />
          <Route path="modules/windows-failed-logon" element={<WindowsFailedLogonPage siem={siem} />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
