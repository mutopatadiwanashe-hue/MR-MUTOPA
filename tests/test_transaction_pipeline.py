from datetime import datetime

from rules.transaction_pipeline import process_transaction_pipeline
from database.transaction_schema import Transaction


def test_valid_transaction_goes_through_pipeline():
    transaction = Transaction(
        transaction_id="TX016",
        sender_account="BUS016",
        receiver_account="BUS017",
        amount=5000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    result = process_transaction_pipeline(transaction)

    assert result.transaction_id == "TX016"
    assert result.valid is True
    assert result.validation_errors == []
    assert result.audit_log is not None
    assert result.audit_log.decision == "ALLOW"


def test_invalid_transaction_stops_pipeline():
    transaction = Transaction(
        transaction_id="TX017",
        sender_account="BUS017",
        receiver_account="BUS018",
        amount=-500.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    result = process_transaction_pipeline(transaction)

    assert result.transaction_id == "TX017"
    assert result.valid is False
    assert result.audit_log is None
    assert "Transaction amount must be greater than zero." in result.validation_errors


def test_high_risk_transaction_reaches_block_decision():
    transaction = Transaction(
        transaction_id="TX018",
        sender_account="BUS018",
        receiver_account="PER018",
        amount=20000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=False,
        receiver_kyc_verified=False,
    )

    result = process_transaction_pipeline(transaction)

    assert result.valid is True
    assert result.audit_log is not None
    assert result.audit_log.risk_level == "HIGH"
    assert result.audit_log.decision == "BLOCK"