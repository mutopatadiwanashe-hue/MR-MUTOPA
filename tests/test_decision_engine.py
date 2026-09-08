from datetime import datetime

from database.transaction_schema import Transaction
from rules.decision_engine import make_risk_decision


def test_low_risk_decision_is_allow():
    transaction = Transaction(
        transaction_id="TX008",
        sender_account="BUS008",
        receiver_account="BUS009",
        amount=5000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    decision = make_risk_decision(transaction)

    assert decision.transaction_id == "TX008"
    assert decision.risk_level == "LOW"
    assert decision.decision == "ALLOW"


def test_medium_risk_decision_is_review():
    transaction = Transaction(
        transaction_id="TX009",
        sender_account="BUS009",
        receiver_account="BUS010",
        amount=15000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    decision = make_risk_decision(transaction)

    assert decision.transaction_id == "TX009"
    assert decision.risk_level == "MEDIUM"
    assert decision.decision == "REVIEW"
    assert decision.reason == "Transaction requires compliance review."


def test_high_risk_decision_is_block():
    transaction = Transaction(
        transaction_id="TX010",
        sender_account="BUS010",
        receiver_account="PER010",
        amount=20000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=False,
        receiver_kyc_verified=False,
    )

    decision = make_risk_decision(transaction)

    assert decision.transaction_id == "TX010"
    assert decision.risk_level == "HIGH"
    assert decision.decision == "BLOCK"
    assert decision.reason == "Transaction triggered multiple high-risk indicators."