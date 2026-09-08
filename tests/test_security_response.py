from security.alert_engine import SecurityAlert
from security.security_response import SecurityResponse, respond_to_alert


def test_no_alert_creates_no_lock():
    response = respond_to_alert(None)

    assert isinstance(response, SecurityResponse)
    assert response.alert is None
    assert response.lock is None


def test_warning_alert_does_not_lock():
    alert = SecurityAlert(
        level="WARNING",
        alert_type="COMPLIANCE_REVIEW",
        message="Transaction requires compliance review.",
        requires_lock=False,
        requires_admin=False,
    )

    response = respond_to_alert(alert)

    assert response.alert == alert
    assert response.lock is None


def test_critical_alert_creates_lock():
    alert = SecurityAlert(
        level="CRITICAL",
        alert_type="HIGH_RISK_TRANSACTION",
        message="High-risk transaction blocked by BankGuard AI.",
        requires_lock=True,
        requires_admin=True,
    )

    response = respond_to_alert(alert)

    assert response.alert == alert
    assert response.lock is not None
    assert response.lock.locked is True
    assert response.lock.requires_admin is True
    assert response.lock.reason == alert.message