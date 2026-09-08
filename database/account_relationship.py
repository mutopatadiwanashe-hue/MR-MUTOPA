from database.account_schema import Account


def accounts_can_transact(
    sender: Account,
    receiver: Account,
) -> bool:

    if not sender.active:
        return False

    if not receiver.active:
        return False

    return True


def is_business_to_personal(
    sender: Account,
    receiver: Account,
) -> bool:

    return (
        sender.account_type == "business"
        and receiver.account_type == "personal"
    )
