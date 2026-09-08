from database.account_schema import Account


def validate_account(account: Account) -> list[str]:
    errors = []

    if not account.account_id:
        errors.append("Account ID is required.")

    if account.account_type not in {"business", "personal"}:
        errors.append("Invalid account type.")

    if not account.owner_name:
        errors.append("Owner name is required.")

    return errors
