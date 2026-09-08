from dataclasses import dataclass

from security.admin_auth import AdminAuthorization
from security.lock_manager import SecurityLock, unlock_system


@dataclass
class AdminUnlockResult:
    unlocked: bool
    message: str
    lock: SecurityLock


def process_admin_unlock(
    lock: SecurityLock,
    authorization: AdminAuthorization,
) -> AdminUnlockResult:

    if not authorization.authorized:
        return AdminUnlockResult(
            unlocked=False,
            message="Administrator authorization failed. System remains locked.",
            lock=lock,
        )

    updated_lock = unlock_system(
        lock,
        authorization.authorized,
    )

    if not updated_lock.locked:
        return AdminUnlockResult(
            unlocked=True,
            message="Administrator authorized. System unlocked successfully.",
            lock=updated_lock,
        )

    return AdminUnlockResult(
        unlocked=False,
        message="System could not be unlocked.",
        lock=updated_lock,
    )


if __name__ == "__main__":
    from security.admin_auth import authorize_admin
    from security.lock_manager import create_lock

    lock = create_lock(
        reason="High-risk transaction detected by BankGuard AI."
    )

    authorization = authorize_admin(
        password_valid=True,
        biometric_valid=True,
    )

    result = process_admin_unlock(
        lock,
        authorization,
    )

    print("BANKGUARD AI ADMIN UNLOCK SERVICE")
    print("---------------------------------")
    print(f"Authorization: {authorization.authorized}")
    print(f"Authorization Method: {authorization.method}")
    print(f"Unlocked: {result.unlocked}")
    print(f"Message: {result.message}")
    print(f"System Locked: {result.lock.locked}")
