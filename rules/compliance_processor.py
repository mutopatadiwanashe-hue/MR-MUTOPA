from database.audit_log import AuditLog, create_audit_log
from database.transaction_schema import Transaction
from rules.decision_engine import make_risk_decision


def process_transaction(transaction: Transaction) -> AuditLog:
    decision = make_risk_decision(transaction)

    assessment_flags = []

    if decision.risk_level == "HIGH":
        assessment_flags = [
            "HIGH_RISK_TRANSACTION"
        ]
    elif decision.risk_level == "MEDIUM":
        assessment_flags = [
            "MEDIUM_RISK_TRANSACTION"
        ]

    return create_audit_log(
        transaction_id=decision.transaction_id,
        risk_level=decision.risk_level,
        decision=decision.decision,
        reason=decision.reason,
        flags=assessment_flags,
    )