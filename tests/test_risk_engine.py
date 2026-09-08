from datetime import datetime

from database.transaction_schema import Transaction
from rules.risk_engine import (
    assess_transaction_risk,
    classify_risk_severity,
)


def test_risk_engine_detects_multiple_flags():
    transaction = Transaction(
        transaction_id="TX200",
        sender_account="BUS001",
        receiver_account="PER001",
        amount=15000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=False,
        receiver_kyc_verified=True,
    )

    flags = assess_transaction_risk(transaction)

    assert "HIGH_VALUE_TRANSACTION" in flags
    assert "BUSINESS_TO_PERSONAL_TRANSFER" in flags
    assert "SENDER_KYC_NOT_VERIFIED" in flags
    assert len(flags) == 3


from datetime import datetime

from database.transaction_schema import Transaction
from rules.risk_engine import (
    assess_transaction_risk,
    classify_risk_severity,
    generate_risk_assessment,
)


def test_detects_multiple_risk_flags():
    transaction = Transaction(
        transaction_id="TX003",
        sender_account="BUS003",
        receiver_account="PER003",
        amount=15000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=False,
        receiver_kyc_verified=True,
    )

    flags = assess_transaction_risk(transaction)

    assert "HIGH_VALUE_TRANSACTION" in flags
    assert "BUSINESS_TO_PERSONAL_TRANSFER" in flags
    assert "SENDER_KYC_NOT_VERIFIED" in flags


def test_low_risk_transaction():
    transaction = Transaction(
        transaction_id="TX004",
        sender_account="BUS004",
        receiver_account="BUS005",
        amount=5000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    flags = assess_transaction_risk(transaction)

    assert flags == []
    assert classify_risk_severity(flags) == "LOW"


def test_zero_flags_are_low_risk():
    assert classify_risk_severity([]) == "LOW"


def test_one_flag_is_medium_risk():
    assert classify_risk_severity(["HIGH_VALUE_TRANSACTION"]) == "MEDIUM"


def test_multiple_flags_are_high_risk():
    assert classify_risk_severity(
        ["HIGH_VALUE_TRANSACTION", "BUSINESS_TO_PERSONAL_TRANSFER"]
    ) == "HIGH"


def test_low_risk_structured_assessment():
    transaction = Transaction(
        transaction_id="TX005",
        sender_account="BUS005",
        receiver_account="BUS006",
        amount=5000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    assessment = generate_risk_assessment(transaction)

    assert assessment.transaction_id == "TX005"
    assert assessment.risk_level == "LOW"
    assert assessment.flags == []
    assert assessment.flag_count == 0
    assert assessment.recommended_action == "ALLOW"


def test_medium_risk_structured_assessment():
    transaction = Transaction(
        transaction_id="TX006",
        sender_account="BUS006",
        receiver_account="BUS007",
        amount=15000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="business",
        sender_kyc_verified=True,
        receiver_kyc_verified=True,
    )

    assessment = generate_risk_assessment(transaction)

    assert assessment.transaction_id == "TX006"
    assert assessment.risk_level == "MEDIUM"
    assert assessment.flag_count == 1
    assert "HIGH_VALUE_TRANSACTION" in assessment.flags
    assert assessment.recommended_action == "REVIEW"


def test_high_risk_structured_assessment():
    transaction = Transaction(
        transaction_id="TX007",
        sender_account="BUS007",
        receiver_account="PER007",
        amount=20000.00,
        currency="USD",
        transaction_type="transfer",
        timestamp=datetime.now(),
        sender_account_type="business",
        receiver_account_type="personal",
        sender_kyc_verified=False,
        receiver_kyc_verified=False,
    )

    assessment = generate_risk_assessment(transaction)

    assert assessment.transaction_id == "TX007"
    assert assessment.risk_level == "HIGH"
    assert assessment.flag_count == 3
    assert "HIGH_VALUE_TRANSACTION" in assessment.flags
    assert "BUSINESS_TO_PERSONAL_TRANSFER" in assessment.flags
    assert "SENDER_KYC_NOT_VERIFIED" in assessment.flags
    assert assessment.recommended_action == "BLOCK"