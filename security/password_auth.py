import hashlib
import hmac
import json
import secrets
from getpass import getpass
from pathlib import Path


PASSWORD_FILE = Path("security/admin_password.json")
ITERATIONS = 600000


def hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS,
    )

    return salt.hex(), password_hash.hex()


def save_password_hash(password: str) -> None:
    salt, password_hash = hash_password(password)

    PASSWORD_FILE.parent.mkdir(parents=True, exist_ok=True)

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


def verify_password(password: str) -> bool:
    if not PASSWORD_FILE.exists():
        return False

    try:
        data = json.loads(
            PASSWORD_FILE.read_text(encoding="utf-8")
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


def setup_admin_password() -> None:
    password = getpass("Enter new BankGuard administrator password: ")
    confirmation = getpass("Confirm administrator password: ")

    if not password:
        print("Password cannot be empty.")
        return

    if password != confirmation:
        print("Passwords do not match.")
        return

    save_password_hash(password)
    print("Administrator password configured successfully.")


if __name__ == "__main__":
    setup_admin_password()