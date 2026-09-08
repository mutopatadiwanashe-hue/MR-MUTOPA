from dataclasses import dataclass


@dataclass
class BankGuardWorkflowState:
    transaction: dict

    fraud_result: object | None = None
    kyc_result: object | None = None
    aml_result: object | None = None

    transaction_monitor_result: object | None = None
    compliance_knowledge: object | None = None

    decision_result: object | None = None
    security_response: object | None = None


def create_workflow_state(transaction: dict) -> BankGuardWorkflowState:
    return BankGuardWorkflowState(
        transaction=transaction,
    )