from datetime import datetime

from database.transaction_schema import Transaction
from database.validator import validate_transaction


def test_valid_transaction():
    transaction = Transaction(
        transaction_id="TX001",
        sender_account="BUS001",
        receiver_account="PER001",
        amount=15000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    errors = validate_transaction(transaction)

    assert errors == []


def test_invalid_amount():
    transaction = Transaction(
        transaction_id="TX002",
        sender_account="BUS002",
        receiver_account="PER002",
        amount=-100,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    errors = validate_transaction(transaction)

    assert "Transaction amount must be greater than zero." in errors