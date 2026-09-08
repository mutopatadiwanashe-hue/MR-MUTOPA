from .transaction_schema import Transaction


def validate_transaction(transaction: Transaction) -> list[str]:
    errors = []

    if not transaction.transaction_id:
        errors.append("Transaction ID is required.")

    if not transaction.sender_account:
        errors.append("Sender account is required.")

    if not transaction.receiver_account:
        errors.append("Receiver account is required.")

    if transaction.amount <= 0:
        errors.append("Transaction amount must be greater than zero.")

    if not transaction.currency:
        errors.append("Currency is required.")

    if not transaction.transaction_type:
        errors.append("Transaction type is required.")

    if transaction.sender_account_type not in {"business", "personal"}:
        errors.append("Invalid sender account type.")

    if transaction.receiver_account_type not in {"business", "personal"}:
        errors.append("Invalid receiver account type.")

    return errors