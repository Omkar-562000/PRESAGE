import { AttackModulePage } from "../../components/AttackModulePage";
import { getAttackById } from "../../lib/ui";

const moduleConfig = getAttackById("port_scan");

export function PortScanPage({ siem }) {
  return (
    <AttackModulePage
      module={moduleConfig}
      siem={siem}
      evidenceTitle="Module Outcome"
      logicItems={[
        "Simulates reconnaissance against multiple ports from a single external source IP.",
        "Validates distinct port counting inside a short time window in network telemetry.",
        "Creates a medium-severity incident to demonstrate graded detection and triage behavior.",
      ]}
    />
  );
}
