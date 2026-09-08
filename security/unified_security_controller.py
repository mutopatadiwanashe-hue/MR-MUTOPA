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
from rag.transaction_context import get_transaction_compliance_knowledge


@dataclass
class UnifiedSecurityResponse:
    decision_result: object
    alert: SecurityAlert | None
    security_lock: SecurityLock | None
    account_control: object
    transaction_monitor: object
    compliance_review: ComplianceWorkflowResult | None
    audit_log: AuditLog | None
    compliance_knowledge: object


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

    compliance_knowledge = get_transaction_compliance_knowledge(
        transaction,
        top_k=3,
    )

    security_lock = None
    compliance_review = None

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
        compliance_knowledge=compliance_knowledge,
    )