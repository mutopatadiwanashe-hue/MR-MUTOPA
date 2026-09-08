from dataclasses import dataclass


@dataclass
class AccountControlResult:
    allowed: bool
    warning: str | None
    requires_admin: bool


def check_business_to_personal_control(
    sender_type: str,
    receiver_type: str,
) -> AccountControlResult:

    if sender_type == "business" and receiver_type == "personal":
        return AccountControlResult(
            allowed=False,
            warning="Business-to-personal transfer requires administrator authorization.",
            requires_admin=True,
        )

    return AccountControlResult(
        allowed=True,
        warning=None,
        requires_admin=False,
    )


if __name__ == "__main__":
    result = check_business_to_personal_control(
        sender_type="business",
        receiver_type="personal",
    )

    print("BANKGUARD AI ACCOUNT CONTROL")
    print("----------------------------")
    print(f"Allowed: {result.allowed}")
    print(f"Warning: {result.warning}")
    print(f"Admin Required: {result.requires_admin}")
