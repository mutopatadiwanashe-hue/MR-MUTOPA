from datetime import datetime

from database.audit_log import AuditLog
from database.transaction_schema import Transaction
from rules.compliance_processor import process_transaction


def test_process_low_risk_transaction():
    transaction = Transaction(
        transaction_id="TX013",
        sender_account="BUS013",
        receiver_account="BUS014",
        amount=5000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    log = process_transaction(transaction)

    assert isinstance(log, AuditLog)
    assert log.transaction_id == "TX013"
    assert log.risk_level == "LOW"
    assert log.decision == "ALLOW"
    assert log.flags == []


def test_process_medium_risk_transaction():
    transaction = Transaction(
        transaction_id="TX014",
        sender_account="BUS014",
        receiver_account="BUS015",
        amount=15000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    log = process_transaction(transaction)

    assert log.transaction_id == "TX014"
    assert log.risk_level == "MEDIUM"
    assert log.decision == "REVIEW"
    assert log.flags == ["MEDIUM_RISK_TRANSACTION"]


def test_process_high_risk_transaction():
    transaction = Transaction(
        transaction_id="TX015",
        sender_account="BUS015",
        receiver_account="PER015",
        amount=20000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=False,
        receiver_kyc_verified=False,
    )

    log = process_transaction(transaction)

    assert log.transaction_id == "TX015"
    assert log.risk_level == "HIGH"
    assert log.decision == "BLOCK"
    assert log.flags == ["HIGH_RISK_TRANSACTION"]