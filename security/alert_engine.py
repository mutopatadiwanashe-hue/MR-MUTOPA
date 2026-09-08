from dataclasses import dataclass


@dataclass
class SecurityAlert:
    level: str
    alert_type: str
    message: str
    requires_lock: bool
    requires_admin: bool


def generate_security_alert(
    risk_level: str,
    decision: str,
) -> SecurityAlert | None:

    if risk_level == "LOW" and decision == "ALLOW":
        return None

    if risk_level == "MEDIUM" and decision == "REVIEW":
        return SecurityAlert(
            level="WARNING",
            alert_type="COMPLIANCE_REVIEW",
            message="Transaction requires compliance review.",
            requires_lock=False,
            requires_admin=False,
        )

    if risk_level == "HIGH" and decision == "BLOCK":
        return SecurityAlert(
            level="CRITICAL",
            alert_type="HIGH_RISK_TRANSACTION",
            message="High-risk transaction blocked by BankGuard AI.",
            requires_lock=True,
            requires_admin=True,
        )

    return SecurityAlert(
        level="WARNING",
        alert_type="UNEXPECTED_DECISION",
        message="Transaction produced an unexpected risk decision.",
        requires_lock=False,
        requires_admin=True,
    )