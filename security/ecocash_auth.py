from dataclasses import dataclass
import hashlib
import hmac
import json
import secrets
from pathlib import Path


BUSINESS_ACCOUNT = "0789165857"
PASSWORD_FILE = Path("security/ecocash_transaction_password.json")
ITERATIONS = 600000


@dataclass
class EcoCashAuthorization:
    authorized: bool
    account_number: str
    message: str


def hash_password(
    password: str,
    salt: bytes | None = None,
) -> tuple[str, str]:

    if salt is None:
        salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS,
    )

    return salt.hex(), password_hash.hex()


def save_transaction_password(password: str) -> None:

    salt, password_hash = hash_password(password)

    PASSWORD_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = {
        "algorithm": "PBKDF2-HMAC-SHA256",
        "iterations": ITERATIONS,
        "salt": salt,
        "password_hash": password_hash,
    }

    PASSWORD_FILE.write_text(
        json.dumps(data, indent=4),
        encoding="utf-8",
    )


def verify_transaction_password(password: str) -> bool:

    if not PASSWORD_FILE.exists():
        return False

    try:
        data = json.loads(
            PASSWORD_FILE.read_text(
                encoding="utf-8"
            )
        )

        salt = bytes.fromhex(data["salt"])

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            int(data["iterations"]),
        ).hex()

        return hmac.compare_digest(
            password_hash,
            data["password_hash"],
        )

    except (KeyError, ValueError, json.JSONDecodeError):
        return False


def authorize_ecocash_transaction(
    account_number: str,
    password: str,
) -> EcoCashAuthorization:

    if account_number != BUSINESS_ACCOUNT:

        return EcoCashAuthorization(
            authorized=False,
            account_number=account_number,
            message="Invalid business EcoCash account.",
        )

    if not verify_transaction_password(password):

        return EcoCashAuthorization(
            authorized=False,
            account_number=account_number,
            message="Invalid transaction password.",
        )

    return EcoCashAuthorization(
        authorized=True,
        account_number=account_number,
        message="EcoCash transaction authorized successfully.",
    )
