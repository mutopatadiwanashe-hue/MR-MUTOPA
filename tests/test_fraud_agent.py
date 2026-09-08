from agents.fraud_agent import (
    classify_fraud_risk,
    determine_fraud_action,
    explain_fraud_result,
)


def test_high_risk_classification():
    assert classify_fraud_risk(0.90) == "HIGH"


def test_medium_risk_classification():
    assert classify_fraud_risk(0.60) == "MEDIUM"


def test_low_risk_classification():
    assert classify_fraud_risk(0.20) == "LOW"


def test_high_risk_action():
    assert determine_fraud_action("HIGH") == "BLOCK"


def test_medium_risk_action():
    assert determine_fraud_action("MEDIUM") == "REVIEW"


def test_low_risk_action():
    assert determine_fraud_action("LOW") == "ALLOW"


def test_high_risk_explanation():
    result = explain_fraud_result("HIGH", 0.90)

    assert "High probability" in result
    assert "blocked" in result


def test_medium_risk_explanation():
    result = explain_fraud_result("MEDIUM", 0.60)

    assert "Moderate probability" in result
    assert "review" in result


def test_low_risk_explanation():
    result = explain_fraud_result("LOW", 0.20)

    assert "Low probability" in result
    assert "allowed" in result
