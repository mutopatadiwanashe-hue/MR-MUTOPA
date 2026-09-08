from dataclasses import dataclass

from database.transaction_schema import Transaction
from rules.transaction_pipeline import process_transaction_pipeline
from security.alert_engine import SecurityAlert, generate_security_alert
from security.lock_manager import SecurityLock
from security.security_response import SecurityResponse, respond_to_alert


@dataclass
class SecurityControllerResult:
    transaction_id: str
    valid: bool
    alert: SecurityAlert | None
    response: SecurityResponse | None


def process_security_transaction(
    transaction: Transaction,
) -> SecurityControllerResult:

    pipeline_result = process_transaction_pipeline(transaction)

    if not pipeline_result.valid:
        return SecurityControllerResult(
            transaction_id=transaction.transaction_id,
            valid=False,
            alert=None,
            response=None,
        )

    audit_log = pipeline_result.audit_log

    alert = generate_security_alert(
        audit_log.risk_level,
        audit_log.decision,
    )

    response = respond_to_alert(alert)

    return SecurityControllerResult(
        transaction_id=transaction.transaction_id,
        valid=True,
        alert=alert,
        response=response,
    )