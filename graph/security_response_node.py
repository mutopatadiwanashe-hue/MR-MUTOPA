from security.alert_engine import generate_security_alert
from security.account_control import check_business_to_personal_control
from security.lock_manager import create_lock
from security.compliance_workflow import create_review_for_transaction

from graph.bankguard_workflow import BankGuardWorkflowState


def run_security_response_node(
    state: BankGuardWorkflowState,
) -> BankGuardWorkflowState:

    if state.decision_result is None:
        raise ValueError(
            "Decision result is required before running the security response node."
        )

    transaction = state.transaction
    decision_result = state.decision_result

    account_control = check_business_to_personal_control(
        transaction.get("sender_type", ""),
        transaction.get("receiver_type", ""),
    )

    alert = generate_security_alert(
        decision_result.final_risk_level,
        decision_result.final_decision,
    )

    compliance_review = None
    security_lock = None

    if decision_result.final_decision == "REVIEW":
        compliance_review = create_review_for_transaction(
            transaction_id=transaction.get(
                "transaction_id",
                "UNKNOWN_TRANSACTION",
            ),
            risk_level=decision_result.final_risk_level,
            reason="Transaction requires compliance review.",
        )

    if alert is not None and alert.requires_lock:
        security_lock = create_lock(
            reason="High-risk transaction blocked by BankGuard AI.",
        )

    if account_control.requires_admin and security_lock is None:
        security_lock = create_lock(
            reason=account_control.warning,
        )

    state.security_response = {
        "account_control": account_control,
        "alert": alert,
        "security_lock": security_lock,
        "compliance_review": compliance_review,
    }

    return state