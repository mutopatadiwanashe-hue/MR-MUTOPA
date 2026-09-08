from security.alert_engine import SecurityAlert, generate_security_alert


def test_low_risk_produces_no_alert():
    alert = generate_security_alert("LOW", "ALLOW")

    assert alert is None


def test_medium_risk_produces_warning():
    alert = generate_security_alert("MEDIUM", "REVIEW")

    assert isinstance(alert, SecurityAlert)
    assert alert.level == "WARNING"
    assert alert.alert_type == "COMPLIANCE_REVIEW"
    assert alert.requires_lock is False
    assert alert.requires_admin is False


def test_high_risk_produces_critical_alert():
    alert = generate_security_alert("HIGH", "BLOCK")

    assert isinstance(alert, SecurityAlert)
    assert alert.level == "CRITICAL"
    assert alert.alert_type == "HIGH_RISK_TRANSACTION"
    assert alert.requires_lock is True
    assert alert.requires_admin is True


def test_unexpected_decision_requires_admin():
    alert = generate_security_alert("HIGH", "REVIEW")

    assert isinstance(alert, SecurityAlert)
    assert alert.level == "WARNING"
    assert alert.alert_type == "UNEXPECTED_DECISION"
    assert alert.requires_admin is True