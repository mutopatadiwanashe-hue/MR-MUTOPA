from datetime import datetime

from database.transaction_schema import Transaction
from security.security_controller import process_security_transaction


def test_low_risk_transaction():
    transaction = Transaction(
        transaction_id="TX_LOW",
        sender_account="BUS001",
        receiver_account="BUS002",
        amount=5000,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    result = process_security_transaction(transaction)

    assert result.valid is True
    assert result.alert is None
    assert result.response is not None
    assert result.response.alert is None
    assert result.response.lock is None


def test_medium_risk_transaction():
    transaction = Transaction(
        transaction_id="TX_MEDIUM",
        sender_account="BUS001",
        receiver_account="PER001",
        amount=5000,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    result = process_security_transaction(transaction)

    assert result.valid is True
    assert result.alert is not None
    assert result.alert.level == "WARNING"
    assert result.response is not None
    assert result.response.lock is None


def test_high_risk_transaction():
    transaction = Transaction(
        transaction_id="TX_HIGH",
        sender_account="BUS001",
        receiver_account="PER001",
        amount=15000,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    result = process_security_transaction(transaction)

    assert result.valid is True
    assert result.alert is not None
    assert result.alert.level == "CRITICAL"
    assert result.response is not None
    assert result.response.lock is not None
    assert result.response.lock.locked is True


def test_invalid_transaction():
    transaction = Transaction(
        transaction_id="TX_INVALID",
        sender_account="BUS001",
        receiver_account="PER001",
        amount=-100,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    result = process_security_transaction(transaction)

    assert result.valid is False
    assert result.alert is None
    assert result.response is None