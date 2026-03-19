import { AttackModulePage } from "../../components/AttackModulePage";
import { getAttackById } from "../../lib/ui";

const moduleConfig = getAttackById("brute_force");

export function BruteForcePage({ siem }) {
  return (
    <AttackModulePage
      module={moduleConfig}
      siem={siem}
      evidenceTitle="Module Outcome"
      logicItems={[
        "Simulates repeated failed logins against one account from the same external source.",
        "Validates that the SIEM counts the attempts inside the configured alert window.",
        "Creates a high-severity incident and updates MTTD once the threshold is crossed.",
      ]}
    />
  );
}
