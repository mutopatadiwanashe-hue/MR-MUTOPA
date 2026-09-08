from agents.decision_agent import (
    calculate_final_risk,
    determine_final_decision,
    make_final_decision,
)


def test_highest_risk_wins():
    assert calculate_final_risk("LOW", "MEDIUM", "HIGH") == "HIGH"


def test_medium_risk_wins_over_low():
    assert calculate_final_risk("LOW", "MEDIUM", "LOW") == "MEDIUM"


def test_all_low_is_low():
    assert calculate_final_risk("LOW", "LOW", "LOW") == "LOW"


def test_high_risk_decision_is_block():
    assert determine_final_decision("HIGH") == "BLOCK"


def test_medium_risk_decision_is_review():
    assert determine_final_decision("MEDIUM") == "REVIEW"


def test_low_risk_decision_is_allow():
    assert determine_final_decision("LOW") == "ALLOW"


def suspicious_transaction():
    return {
        "transaction_id": "TX_DECISION_TEST",
        "amount": 18000.00,
        "sender_type": "business",
        "receiver_type": "personal",
        "transaction_type": "transfer",
        "sender_kyc_verified": False,
        "receiver_kyc_verified": True,
        "ecocash_connected": False,
        "transaction_frequency": 25,
        "international": True,
    }


def clean_transaction():
    return {
        "transaction_id": "TX_CLEAN_DECISION",
        "amount": 500.00,
        "sender_type": "personal",
        "receiver_type": "business",
        "transaction_type": "payment",
        "sender_kyc_verified": True,
        "receiver_kyc_verified": True,
        "ecocash_connected": True,
        "transaction_frequency": 2,
        "international": False,
    }


def test_suspicious_transaction_is_blocked():
    result = make_final_decision(suspicious_transaction())

    assert result.final_risk_level == "HIGH"
    assert result.final_decision == "BLOCK"
    assert result.fraud_risk == "HIGH"
    assert result.kyc_risk == "MEDIUM"
    assert result.aml_risk == "HIGH"


def test_clean_transaction_is_allowed():
    result = make_final_decision(clean_transaction())

    assert result.final_risk_level == "LOW"
    assert result.final_decision == "ALLOW"
    assert result.fraud_risk == "LOW"
    assert result.kyc_risk == "LOW"
    assert result.aml_risk == "LOW"


def test_decision_contains_reasons():
    result = make_final_decision(suspicious_transaction())

    assert len(result.reasons) == 3
    assert "Fraud Agent:" in result.reasons[0]
    assert "KYC Agent:" in result.reasons[1]
    assert "AML Agent:" in result.reasons[2]
