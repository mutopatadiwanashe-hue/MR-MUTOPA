from security.admin_auth import authorize_admin


def test_admin_authorized_by_password():
    result = authorize_admin(
        password_valid=True,
        biometric_valid=False,
    )

    assert result.authorized is True
    assert result.method == "PASSWORD"


def test_admin_authorized_by_password_and_biometric():
    result = authorize_admin(
        password_valid=True,
        biometric_valid=True,
    )

    assert result.authorized is True
    assert result.method == "PASSWORD_AND_BIOMETRIC"


def test_admin_authorization_failed():
    result = authorize_admin(
        password_valid=False,
        biometric_valid=False,
    )

    assert result.authorized is False
    assert result.method == "NONE"
