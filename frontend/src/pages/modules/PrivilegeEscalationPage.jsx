import { AttackModulePage } from "../../components/AttackModulePage";
import { getAttackById } from "../../lib/ui";

const moduleConfig = getAttackById("privilege_escalation");

export function PrivilegeEscalationPage({ siem }) {
  return (
    <AttackModulePage
      module={moduleConfig}
      siem={siem}
      evidenceTitle="Module Outcome"
      logicItems={[
        "Simulates an unauthorized admin role assignment event in Azure activity telemetry.",
        "Validates immediate alert generation on privileged operations with no waiting threshold.",
        "Creates a high-severity incident suitable for showing automated response and investigation steps.",
      ]}
    />
  );
}
