from agents.kyc_agent import (
    assess_kyc_status,
    classify_kyc_risk,
    determine_kyc_action,
    explain_kyc_result,
    analyze_kyc,
)


def test_both_kyc_verified():
    assert assess_kyc_status(True, True) == "VERIFIED"


def test_sender_not_verified():
    assert assess_kyc_status(False, True) == "SENDER_NOT_VERIFIED"


def test_receiver_not_verified():
    assert assess_kyc_status(True, False) == "RECEIVER_NOT_VERIFIED"


def test_both_kyc_not_verified():
    assert assess_kyc_status(False, False) == "BOTH_NOT_VERIFIED"


def test_low_kyc_risk():
    assert classify_kyc_risk("VERIFIED") == "LOW"


def test_medium_kyc_risk():
    assert classify_kyc_risk("SENDER_NOT_VERIFIED") == "MEDIUM"


def test_high_kyc_risk():
    assert classify_kyc_risk("BOTH_NOT_VERIFIED") == "HIGH"


def test_low_risk_action():
    assert determine_kyc_action("LOW") == "ALLOW"


def test_medium_risk_action():
    assert determine_kyc_action("MEDIUM") == "REVIEW"


def test_high_risk_action():
    assert determine_kyc_action("HIGH") == "BLOCK"


def test_kyc_analysis_returns_result():
    result = analyze_kyc(False, True)

    assert result.kyc_status == "SENDER_NOT_VERIFIED"
    assert result.risk_level == "MEDIUM"
    assert result.recommended_action == "REVIEW"
    assert isinstance(result.reason, str)


def test_verified_kyc_analysis():
    result = analyze_kyc(True, True)

    assert result.kyc_status == "VERIFIED"
    assert result.risk_level == "LOW"
    assert result.recommended_action == "ALLOW"


def test_unverified_kyc_explanation():
    result = explain_kyc_result(
        "SENDER_NOT_VERIFIED",
        "MEDIUM",
    )

    assert "Sender KYC verification is missing" in result
