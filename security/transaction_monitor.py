from dataclasses import dataclass


@dataclass
class TransactionMonitorResult:
    flagged: bool
    reasons: list[str]
    requires_review: bool


def monitor_transaction(
    amount: float,
    sender_type: str,
    receiver_type: str,
) -> TransactionMonitorResult:

    reasons = []

    # Large transaction control
    if amount >= 10000:
        reasons.append("Large transaction requires monitoring.")

    # Business-to-personal control
    if sender_type == "business" and receiver_type == "personal":
        reasons.append(
            "Business-to-personal transfer requires administrator authorization."
        )

    return TransactionMonitorResult(
        flagged=len(reasons) > 0,
        reasons=reasons,
        requires_review=len(reasons) > 0,
    )


if __name__ == "__main__":
    result = monitor_transaction(
        amount=15000,
        sender_type="business",
        receiver_type="personal",
    )

    print("BANKGUARD AI TRANSACTION MONITOR")
    print("--------------------------------")
    print(f"Flagged: {result.flagged}")
    print(f"Reasons: {result.reasons}")
    print(f"Review Required: {result.requires_review}")
