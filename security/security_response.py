from dataclasses import dataclass

from security.alert_engine import SecurityAlert
from security.lock_manager import SecurityLock, create_lock


@dataclass
class SecurityResponse:
    alert: SecurityAlert | None
    lock: SecurityLock | None


def respond_to_alert(alert: SecurityAlert | None) -> SecurityResponse:
    if alert is None:
        return SecurityResponse(
            alert=None,
            lock=None,
        )

    if alert.requires_lock:
        lock = create_lock(alert.message)

        return SecurityResponse(
            alert=alert,
            lock=lock,
        )

    return SecurityResponse(
        alert=alert,
        lock=None,
    )