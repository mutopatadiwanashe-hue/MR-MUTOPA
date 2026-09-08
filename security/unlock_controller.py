from dataclasses import dataclass

from security.admin_auth import (
    AdminAuthorization,
    authorize_admin_with_password,
)
from security.lock_manager import SecurityLock, unlock_system


@dataclass
class UnlockResult:
    unlocked: bool
    lock: SecurityLock
    authorization: AdminAuthorization


def attempt_system_unlock(
    lock: SecurityLock,
    authorization: AdminAuthorization,
) -> UnlockResult:

    if not lock.locked:
        return UnlockResult(
            unlocked=True,
            lock=lock,
            authorization=authorization,
        )

    updated_lock = unlock_system(
        lock,
        authorization.authorized,
    )

    return UnlockResult(
        unlocked=not updated_lock.locked,
        lock=updated_lock,
        authorization=authorization,
    )


def attempt_system_unlock_with_password(
    lock: SecurityLock,
    password: str,
) -> UnlockResult:

    authorization = authorize_admin_with_password(
        password=password,
    )

    return attempt_system_unlock(
        lock=lock,
        authorization=authorization,
    )