from security.admin_auth import authorize_admin
from security.admin_unlock_service import process_admin_unlock
from security.lock_manager import create_lock


def test_authorized_admin_can_unlock():
    lock = create_lock("High-risk transaction detected.")

    authorization = authorize_admin(
        password_valid=True,
        biometric_valid=True,
    )

    result = process_admin_unlock(lock, authorization)

    assert authorization.authorized is True
    assert result.unlocked is True
    assert result.lock.locked is False


def test_invalid_admin_cannot_unlock():
    lock = create_lock("High-risk transaction detected.")

    authorization = authorize_admin(
        password_valid=False,
        biometric_valid=False,
    )

    result = process_admin_unlock(lock, authorization)

    assert authorization.authorized is False
    assert result.unlocked is False
    assert result.lock.locked is True


def test_password_only_admin_can_unlock():
    lock = create_lock("High-risk transaction detected.")

    authorization = authorize_admin(
        password_valid=True,
        biometric_valid=False,
    )

    result = process_admin_unlock(lock, authorization)

    assert authorization.authorized is True
    assert result.unlocked is True
    assert result.lock.locked is False
