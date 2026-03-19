import { AttackModulePage } from "../../components/AttackModulePage";
import { getAttackById } from "../../lib/ui";

const moduleConfig = getAttackById("windows_failed_logon");

export function WindowsFailedLogonPage({ siem }) {
  return (
    <AttackModulePage
      module={moduleConfig}
      siem={siem}
      evidenceTitle="Module Outcome"
      logicItems={[
        "Simulates repeated failed Windows logons using the WindowsEvent source format.",
        "Validates host-level credential attack detection using failed logon event bursts.",
        "Creates a high-severity incident from Windows telemetry instead of the synthetic SigninLogs table.",
      ]}
    />
  );
}
