from security.security_event import create_security_event


def test_create_security_event():
    event = create_security_event(
        transaction_id="TX001",
        event_type="HIGH_RISK_TRANSACTION",
        severity="CRITICAL",
        message="High-risk transaction detected.",
        action_taken="TRANSACTION_BLOCKED_AND_SYSTEM_LOCKED",
    )

    assert event.transaction_id == "TX001"
    assert event.event_type == "HIGH_RISK_TRANSACTION"
    assert event.severity == "CRITICAL"
    assert event.message == "High-risk transaction detected."
    assert event.action_taken == "TRANSACTION_BLOCKED_AND_SYSTEM_LOCKED"
    assert event.timestamp is not None


def test_security_event_timestamp_is_datetime():
    from datetime import datetime

    event = create_security_event(
        transaction_id="TX002",
        event_type="COMPLIANCE_REVIEW",
        severity="WARNING",
        message="Transaction requires review.",
        action_taken="TRANSACTION_SENT_FOR_REVIEW",
    )

    assert isinstance(event.timestamp, datetime)
