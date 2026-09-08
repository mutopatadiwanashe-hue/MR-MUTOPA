from security.account_control import check_business_to_personal_control
from security.transaction_monitor import monitor_transaction


def test_business_to_personal():
    result = check_business_to_personal_control(
        sender_type="business",
        receiver_type="personal",
    )

    assert result.allowed is False
    assert result.requires_admin is True


def test_personal_to_personal():
    result = check_business_to_personal_control(
        sender_type="personal",
        receiver_type="personal",
    )

    assert result.allowed is True
    assert result.requires_admin is False


def test_business_to_business():
    result = check_business_to_personal_control(
        sender_type="business",
        receiver_type="business",
    )

    assert result.allowed is True
    assert result.requires_admin is False


def test_large_transaction():
    result = monitor_transaction(
        amount=15000,
        sender_type="personal",
        receiver_type="personal",
    )

    assert result.flagged is True
    assert result.requires_review is True


def test_normal_transaction():
    result = monitor_transaction(
        amount=500,
        sender_type="personal",
        receiver_type="personal",
    )

    assert result.flagged is False
    assert result.requires_review is False


if __name__ == "__main__":
    test_business_to_personal()
    test_personal_to_personal()
    test_business_to_business()
    test_large_transaction()
    test_normal_transaction()

    print("BANKGUARD AI ACCOUNT CONTROL TESTS")
    print("----------------------------------")
    print("All 5 tests passed.")
