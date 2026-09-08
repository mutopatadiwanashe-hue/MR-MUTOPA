from datetime import datetime

from database.transaction_schema import Transaction
from rules.transaction_rules import (
    check_high_value_transaction,
    check_business_to_personal_transfer,
    check_kyc_verification,
)


def test_business_transaction_above_10000_is_flagged():
    transaction = Transaction(
        transaction_id="TX100",
        sender_account="BUS001",
        receiver_account="COMP001",
        amount=15000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    result = check_high_value_transaction(transaction)

    assert result == "HIGH_VALUE_TRANSACTION"


def test_business_transaction_below_10000_is_not_flagged():
    transaction = Transaction(
        transaction_id="TX101",
        sender_account="BUS001",
        receiver_account="COMP001",
        amount=8000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    result = check_high_value_transaction(transaction)

    assert result is None


def test_business_to_personal_transfer_is_flagged():
    transaction = Transaction(
        transaction_id="TX102",
        sender_account="BUS001",
        receiver_account="PER001",
        amount=5000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    result = check_business_to_personal_transfer(transaction)

    assert result == "BUSINESS_TO_PERSONAL_TRANSFER"


def test_business_to_business_transfer_is_not_flagged():
    transaction = Transaction(
        transaction_id="TX103",
        sender_account="BUS001",
        receiver_account="BUS002",
        amount=5000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    result = check_business_to_personal_transfer(transaction)

    assert result is None


def test_sender_kyc_not_verified_is_flagged():
    transaction = Transaction(
        transaction_id="TX104",
        sender_account="BUS001",
        receiver_account="PER001",
        amount=3000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=False,
        receiver_kyc_verified=True,
    )

    result = check_kyc_verification(transaction)

    assert result == "SENDER_KYC_NOT_VERIFIED"


def test_receiver_kyc_not_verified_is_flagged():
    transaction = Transaction(
        transaction_id="TX105",
        sender_account="BUS001",
        receiver_account="PER001",
        amount=3000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=True,
        receiver_kyc_verified=False,
    )

    result = check_kyc_verification(transaction)

    assert result == "RECEIVER_KYC_NOT_VERIFIED"


def test_both_kyc_verified_is_not_flagged():
    transaction = Transaction(
        transaction_id="TX106",
        sender_account="BUS001",
        receiver_account="PER001",
        amount=3000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    result = check_kyc_verification(transaction)

    assert result is None

def test_business_transaction_below_10000_is_not_flagged():
    transaction = Transaction(
        transaction_id="TX101",
        sender_account="BUS001",
        receiver_account="COMP001",
        amount=8000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    result = check_high_value_transaction(transaction)

    assert result is None


def test_business_to_personal_transfer_is_flagged():
    transaction = Transaction(
        transaction_id="TX102",
        sender_account="BUS001",
        receiver_account="PER001",
        amount=5000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    result = check_business_to_personal_transfer(transaction)

    assert result == "BUSINESS_TO_PERSONAL_TRANSFER"


def test_business_to_business_transfer_is_not_flagged():
    transaction = Transaction(
        transaction_id="TX103",
        sender_account="BUS001",
        receiver_account="BUS002",
        amount=5000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    result = check_business_to_personal_transfer(transaction)

    assert result is None