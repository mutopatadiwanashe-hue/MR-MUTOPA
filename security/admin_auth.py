from dataclasses import dataclass

from security.password_auth import verify_password


@dataclass
class AdminAuthorization:
    authorized: bool
    method: str
    message: str


def authorize_admin(
    password_valid: bool = False,
    biometric_valid: bool = False,
) -> AdminAuthorization:

    if biometric_valid:
        return AdminAuthorization(
            authorized=True,
            method="FACE",
            message="Administrator successfully authorized by face verification.",
        )

    if password_valid:
        return AdminAuthorization(
            authorized=True,
            method="PASSWORD",
            message="Administrator successfully authorized by password.",
        )

    return AdminAuthorization(
        authorized=False,
        method="NONE",
        message="Administrator authorization failed.",
    )


def authorize_admin_with_password(
    password: str,
) -> AdminAuthorization:

    password_valid = verify_password(password)

    return authorize_admin(
        password_valid=password_valid,
    )


def authorize_admin_with_face(
    face_valid: bool,
) -> AdminAuthorization:

    return authorize_admin(
        biometric_valid=face_valid,
    )
