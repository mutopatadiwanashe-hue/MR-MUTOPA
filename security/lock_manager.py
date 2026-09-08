from dataclasses import dataclass


@dataclass
class SecurityLock:
    locked: bool
    reason: str
    requires_admin: bool


def create_lock(reason: str) -> SecurityLock:
    return SecurityLock(
        locked=True,
        reason=reason,
        requires_admin=True,
    )


def unlock_system(lock: SecurityLock, admin_authorized: bool) -> SecurityLock:
    if not admin_authorized:
        return lock

    return SecurityLock(
        locked=False,
        reason="System unlocked by authorized administrator.",
        requires_admin=False,
    )