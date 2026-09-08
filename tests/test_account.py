from database.account_schema import Account
from database.account_validator import validate_account


def test_valid_business_account():
    account = Account(
        account_id="BUS001",
        account_type="business",
        owner_name="Demo Business",
        ecocash_connected=True,
        kyc_verified=True,
        active=True,
    )

    errors = validate_account(account)

    assert errors == []


def test_valid_personal_account():
    account = Account(
        account_id="PER001",
        account_type="personal",
        owner_name="Demo Customer",
        ecocash_connected=True,
        kyc_verified=True,
        active=True,
    )

    errors = validate_account(account)

    assert errors == []


def test_invalid_account_type():
    account = Account(
        account_id="ACC001",
        account_type="invalid",
        owner_name="Demo User",
        ecocash_connected=False,
        kyc_verified=True,
        active=True,
    )

    errors = validate_account(account)

    assert "Invalid account type." in errors


def test_missing_account_id():
    account = Account(
        account_id="",
        account_type="business",
        owner_name="Demo Business",
        ecocash_connected=True,
        kyc_verified=True,
        active=True,
    )

    errors = validate_account(account)

    assert "Account ID is required." in errors
