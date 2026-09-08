from agents.aml_agent import (
    detect_aml_flags,
    calculate_aml_risk_score,
    classify_aml_risk,
    determine_aml_action,
    explain_aml_result,
    analyze_aml,
)


def suspicious_transaction():
    return {
        "transaction_id": "TX_AML_TEST",
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
        "transaction_id": "TX_CLEAN_TEST",
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


def test_suspicious_transaction_has_flags():
    flags = detect_aml_flags(suspicious_transaction())

    assert "HIGH_VALUE_TRANSACTION" in flags
    assert "HIGH_TRANSACTION_FREQUENCY" in flags
    assert "INTERNATIONAL_TRANSACTION" in flags
    assert "BUSINESS_TO_PERSONAL_TRANSFER" in flags
    assert "SENDER_KYC_NOT_VERIFIED" in flags
    assert "ECOCASH_NOT_CONNECTED" in flags


def test_clean_transaction_has_no_flags():
    flags = detect_aml_flags(clean_transaction())

    assert flags == []


def test_risk_score_counts_flags():
    flags = ["FLAG_1", "FLAG_2", "FLAG_3"]

    assert calculate_aml_risk_score(flags) == 3


def test_low_aml_risk():
    assert classify_aml_risk(0) == "LOW"


def test_medium_aml_risk():
    assert classify_aml_risk(2) == "MEDIUM"


def test_high_aml_risk():
    assert classify_aml_risk(4) == "HIGH"


def test_low_aml_action():
    assert determine_aml_action("LOW") == "ALLOW"


def test_medium_aml_action():
    assert determine_aml_action("MEDIUM") == "REVIEW"


def test_high_aml_action():
    assert determine_aml_action("HIGH") == "BLOCK"


def test_suspicious_transaction_analysis():
    result = analyze_aml(suspicious_transaction())

    assert result.risk_level == "HIGH"
    assert result.risk_score == 6
    assert result.recommended_action == "BLOCK"
    assert len(result.flags) == 6
    assert isinstance(result.reason, str)


def test_clean_transaction_analysis():
    result = analyze_aml(clean_transaction())

    assert result.risk_level == "LOW"
    assert result.risk_score == 0
    assert result.recommended_action == "ALLOW"
    assert result.flags == []


def test_high_risk_explanation():
    result = explain_aml_result(
        "HIGH",
        5,
        ["HIGH_VALUE_TRANSACTION"],
    )

    assert "High AML risk" in result
    assert "blocking" in result


def test_medium_risk_explanation():
    result = explain_aml_result(
        "MEDIUM",
        2,
        ["HIGH_VALUE_TRANSACTION", "INTERNATIONAL_TRANSACTION"],
    )

    assert "Medium AML risk" in result
    assert "review" in result


def test_low_risk_explanation():
    result = explain_aml_result(
        "LOW",
        0,
        [],
    )

    assert "Low AML risk" in result
