from security.lock_manager import SecurityLock, create_lock, unlock_system


def test_create_lock():
    lock = create_lock("High-risk transaction detected.")

    assert isinstance(lock, SecurityLock)
    assert lock.locked is True
    assert lock.reason == "High-risk transaction detected."
    assert lock.requires_admin is True


def test_unauthorized_user_cannot_unlock():
    lock = create_lock("Security violation detected.")

    unlocked = unlock_system(lock, admin_authorized=False)

    assert unlocked.locked is True
    assert unlocked.requires_admin is True
    assert unlocked.reason == "Security violation detected."


def test_authorized_admin_can_unlock():
    lock = create_lock("High-risk transaction detected.")

    unlocked = unlock_system(lock, admin_authorized=True)

    assert unlocked.locked is False
    assert unlocked.requires_admin is False
    assert unlocked.reason == "System unlocked by authorized administrator."