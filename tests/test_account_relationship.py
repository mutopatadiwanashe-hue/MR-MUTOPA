from database.account_schema import Account
from database.account_relationship import (
    accounts_can_transact,
    is_business_to_personal,
)


def test_active_accounts_can_transact():
    sender = Account(
        account_id="BUS001",
        account_type="business",
        owner_name="Demo Business",
        ecocash_connected=True,
        kyc_verified=True,
        active=True,
    )

    receiver = Account(
        account_id="PER001",
        account_type="personal",
        owner_name="Demo Customer",
        ecocash_connected=True,
        kyc_verified=True,
        active=True,
    )

    assert accounts_can_transact(sender, receiver) is True


def test_inactive_sender_cannot_transact():
    sender = Account(
        account_id="BUS001",
        account_type="business",
        owner_name="Demo Business",
        ecocash_connected=True,
        kyc_verified=True,
        active=False,
    )

    receiver = Account(
        account_id="PER001",
        account_type="personal",
        owner_name="Demo Customer",
        ecocash_connected=True,
        kyc_verified=True,
        active=True,
    )

    assert accounts_can_transact(sender, receiver) is False


def test_inactive_receiver_cannot_transact():
    sender = Account(
        account_id="BUS001",
        account_type="business",
        owner_name="Demo Business",
        ecocash_connected=True,
        kyc_verified=True,
        active=True,
    )

    receiver = Account(
        account_id="PER001",
        account_type="personal",
        owner_name="Demo Customer",
        ecocash_connected=True,
        kyc_verified=True,
        active=False,
    )

    assert accounts_can_transact(sender, receiver) is False


def test_business_to_personal_relationship():
    sender = Account(
        account_id="BUS001",
        account_type="business",
        owner_name="Demo Business",
        ecocash_connected=True,
        kyc_verified=True,
        active=True,
    )

    receiver = Account(
        account_id="PER001",
        account_type="personal",
        owner_name="Demo Customer",
        ecocash_connected=True,
        kyc_verified=True,
        active=True,
    )

    assert is_business_to_personal(sender, receiver) is True
