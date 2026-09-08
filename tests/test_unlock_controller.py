from security.admin_auth import authorize_admin
from security.lock_manager import create_lock
from security.unlock_controller import attempt_system_unlock


def test_wrong_admin_authorization_keeps_system_locked():
    lock = create_lock("High-risk transaction detected.")

    authorization = authorize_admin(
        password_valid=False,
        biometric_valid=False,
    )

    result = attempt_system_unlock(lock, authorization)

    assert result.unlocked is False
    assert result.lock.locked is True
    assert result.authorization.authorized is False


def test_password_authorization_unlocks_system():
    lock = create_lock("High-risk transaction detected.")

    authorization = authorize_admin(
        password_valid=True,
        biometric_valid=False,
    )

    result = attempt_system_unlock(lock, authorization)

    assert result.unlocked is True
    assert result.lock.locked is False
    assert result.authorization.authorized is True


def test_password_and_biometric_unlocks_system():
    lock = create_lock("High-risk transaction detected.")

    authorization = authorize_admin(
        password_valid=True,
        biometric_valid=True,
    )

    result = attempt_system_unlock(lock, authorization)

    assert result.unlocked is True
    assert result.lock.locked is False
    assert result.authorization.authorized is True


def test_already_unlocked_system_remains_unlocked():
    lock = create_lock("High-risk transaction detected.")

    authorization = authorize_admin(
        password_valid=True,
        biometric_valid=False,
    )

    unlocked = attempt_system_unlock(lock, authorization)

    result = attempt_system_unlock(
        unlocked.lock,
        authorization,
    )

    assert result.unlocked is True
    assert result.lock.locked is False
