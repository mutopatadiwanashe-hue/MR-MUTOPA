from dataclasses import dataclass
from datetime import datetime


@dataclass
class SecurityEvent:
    transaction_id: str
    timestamp: datetime
    event_type: str
    severity: str
    message: str
    action_taken: str


def create_security_event(
    transaction_id: str,
    event_type: str,
    severity: str,
    message: str,
    action_taken: str,
) -> SecurityEvent:

    return SecurityEvent(
        transaction_id=transaction_id,
        timestamp=datetime.now(),
        event_type=event_type,
        severity=severity,
        message=message,
        action_taken=action_taken,
    )
