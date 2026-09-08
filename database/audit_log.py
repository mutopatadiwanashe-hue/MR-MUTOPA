from dataclasses import dataclass
from datetime import datetime


@dataclass
class AuditLog:
    transaction_id: str
    timestamp: datetime
    risk_level: str
    decision: str
    reason: str
    flags: list[str]


def create_audit_log(
    transaction_id: str,
    risk_level: str,
    decision: str,
    reason: str,
    flags: list[str],
) -> AuditLog:
    return AuditLog(
        transaction_id=transaction_id,
        timestamp=datetime.now(),
        risk_level=risk_level,
        decision=decision,
        reason=reason,
        flags=flags.copy(),
    )
