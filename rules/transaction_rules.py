from database.transaction_schema import Transaction


HIGH_VALUE_THRESHOLD = 10000.00


def check_high_value_transaction(transaction: Transaction) -> str | None:
    if (
        transaction.sender_account_type == "business"
        and transaction.amount > HIGH_VALUE_THRESHOLD
    ):
        return "HIGH_VALUE_TRANSACTION"

    return None


def check_business_to_personal_transfer(transaction: Transaction) -> str | None:
    if (
        transaction.sender_account_type == "business"
        and transaction.receiver_account_type == "personal"
    ):
        return "BUSINESS_TO_PERSONAL_TRANSFER"

    return None


def check_kyc_verification(transaction: Transaction) -> str | None:
    if not transaction.sender_kyc_verified:
        return "SENDER_KYC_NOT_VERIFIED"

    if not transaction.receiver_kyc_verified:
        return "RECEIVER_KYC_NOT_VERIFIED"

    return None