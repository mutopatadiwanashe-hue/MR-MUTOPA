from dataclasses import dataclass

from agents.decision_agent import make_final_decision
from security.account_control import check_business_to_personal_control
from security.transaction_monitor import monitor_transaction
from security.alert_engine import SecurityAlert, generate_security_alert
from security.lock_manager import SecurityLock, create_lock
from security.compliance_workflow import (
    ComplianceWorkflowResult,
    create_review_for_transaction,
)
from database.audit_log import AuditLog, create_audit_log
from database.audit_repository import save_audit_log


@dataclass
class UnifiedSecurityResponse:
    decision_result: object
    alert: SecurityAlert | None
    security_lock: SecurityLock | None
    account_control: object
    transaction_monitor: object
    compliance_review: ComplianceWorkflowResult | None
    audit_log: AuditLog | None


def process_transaction_security(transaction: dict) -> UnifiedSecurityResponse:
    account_control = check_business_to_personal_control(
        transaction.get("sender_type", ""),
        transaction.get("receiver_type", ""),
    )

    transaction_monitor = monitor_transaction(
        amount=transaction.get("amount", 0),
        sender_type=transaction.get("sender_type", ""),
        receiver_type=transaction.get("receiver_type", ""),
    )

    decision_result = make_final_decision(transaction)

    alert = generate_security_alert(
        decision_result.final_risk_level,
        decision_result.final_decision,
    )

    security_lock = None
    compliance_review = None

    # Stage 11: Human compliance review
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

    if account_control.requires_admin:
        if security_lock is None:
            security_lock = create_lock(
                reason=account_control.warning,
            )

    # Stage 12: Audit logging
    transaction_id = transaction.get(
        "transaction_id",
        "UNKNOWN_TRANSACTION",
    )

    audit_flags = list(transaction_monitor.reasons)

    if account_control.requires_admin:
        audit_flags.append("ADMIN_AUTHORIZATION_REQUIRED")

    if alert is not None:
        audit_flags.append(alert.alert_type)

    audit_reason = " | ".join(decision_result.reasons)

    audit_log = create_audit_log(
        transaction_id=transaction_id,
        risk_level=decision_result.final_risk_level,
        decision=decision_result.final_decision,
        reason=audit_reason,
        flags=audit_flags,
    )

    save_audit_log(audit_log)

    return UnifiedSecurityResponse(
        decision_result=decision_result,
        alert=alert,
        security_lock=security_lock,
        account_control=account_control,
        transaction_monitor=transaction_monitor,
        compliance_review=compliance_review,
        audit_log=audit_log,
    )


if __name__ == "__main__":
    transaction = {
        "transaction_id": "TX_UNIFIED_SECURITY_TEST",
        "amount": 18000.00,
        "sender_type": "business",
        "receiver_type": "personal",
        "transaction_type": "transfer",
        "sender_kyc_verified": False,
        "receiver_kyc_verified": True,
        "ecocash_connected": False,
        "transaction_frequency": 25,
        "international": True,
    }

    response = process_transaction_security(transaction)

    print("BANKGUARD AI UNIFIED SECURITY CONTROLLER")
    print("----------------------------------------")
    print(f"Account Control Allowed: {response.account_control.allowed}")
    print(f"Admin Required: {response.account_control.requires_admin}")
    print(f"Account Warning: {response.account_control.warning}")
    print(f"Transaction Flagged: {response.transaction_monitor.flagged}")
    print(f"Monitoring Reasons: {response.transaction_monitor.reasons}")
    print(f"Review Required: {response.transaction_monitor.requires_review}")
    print(f"Fraud Risk: {response.decision_result.fraud_risk}")
    print(f"KYC Risk: {response.decision_result.kyc_risk}")
    print(f"AML Risk: {response.decision_result.aml_risk}")
    print(f"Final Risk: {response.decision_result.final_risk_level}")
    print(f"Final Decision: {response.decision_result.final_decision}")

    if response.compliance_review:
        print("\nHUMAN COMPLIANCE REVIEW")
        print("-----------------------")
        print(f"Review Status: {response.compliance_review.review.status}")
        print(
            f"Review Transaction ID: "
            f"{response.compliance_review.review.transaction_id}"
        )
        print(
            f"Review Risk Level: "
            f"{response.compliance_review.review.risk_level}"
        )
    else:
        print("\nHuman Compliance Review: NONE")

    if response.alert:
        print(f"\nAlert Level: {response.alert.level}")
        print(f"Alert Type: {response.alert.alert_type}")
        print(f"System Lock Required: {response.alert.requires_lock}")
        print(f"Alert Admin Required: {response.alert.requires_admin}")
    else:
        print("Alert Level: NONE")

    print(f"System Locked: {response.security_lock is not None}")

    if response.audit_log:
        print("\nAUDIT LOG")
        print("---------")
        print(f"Audit Transaction ID: {response.audit_log.transaction_id}")
        print(f"Audit Risk Level: {response.audit_log.risk_level}")
        print(f"Audit Decision: {response.audit_log.decision}")
        print(f"Audit Reason: {response.audit_log.reason}")
        print(f"Audit Flags: {response.audit_log.flags}")
        print(f"Audit Timestamp: {response.audit_log.timestamp}")
