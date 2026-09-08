from datetime import datetime

from database.audit_log import AuditLog, create_audit_log


def test_create_audit_log():
    log = create_audit_log(
        transaction_id="TX011",
        risk_level="HIGH",
        decision="BLOCK",
        reason="Transaction triggered multiple high-risk indicators.",
        flags=[
            "HIGH_VALUE_TRANSACTION",
            "BUSINESS_TO_PERSONAL_TRANSFER",
            "SENDER_KYC_NOT_VERIFIED",
        ],
    )

    assert isinstance(log, AuditLog)
    assert log.transaction_id == "TX011"
    assert log.risk_level == "HIGH"
    assert log.decision == "BLOCK"
    assert log.reason == "Transaction triggered multiple high-risk indicators."
    assert len(log.flags) == 3
    assert "HIGH_VALUE_TRANSACTION" in log.flags
    assert isinstance(log.timestamp, datetime)


def test_audit_log_copies_flags():
    flags = ["HIGH_VALUE_TRANSACTION"]

    log = create_audit_log(
        transaction_id="TX012",
        risk_level="MEDIUM",
        decision="REVIEW",
        reason="Transaction requires compliance review.",
        flags=flags,
    )

    flags.append("NEW_FLAG")

    assert log.flags == ["HIGH_VALUE_TRANSACTION"]