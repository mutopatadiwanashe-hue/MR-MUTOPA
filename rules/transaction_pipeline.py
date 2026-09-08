from dataclasses import dataclass

from database.audit_log import AuditLog
from database.transaction_schema import Transaction
from database.validator import validate_transaction
from rules.compliance_processor import process_transaction


@dataclass
class TransactionProcessingResult:
    transaction_id: str
    valid: bool
    validation_errors: list[str]
    audit_log: AuditLog | None


def process_transaction_pipeline(
    transaction: Transaction,
) -> TransactionProcessingResult:

    validation_errors = validate_transaction(transaction)

    if validation_errors:
        return TransactionProcessingResult(
            transaction_id=transaction.transaction_id,
            valid=False,
            validation_errors=validation_errors,
            audit_log=None,
        )

    audit_log = process_transaction(transaction)

    return TransactionProcessingResult(
        transaction_id=transaction.transaction_id,
        valid=True,
        validation_errors=[],
        audit_log=audit_log,
    )