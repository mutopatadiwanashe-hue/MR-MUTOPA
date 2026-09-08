from dataclasses import dataclass


@dataclass
class AMLResult:
    risk_level: str
    risk_score: int
    flags: list[str]
    recommended_action: str
    reason: str


def detect_aml_flags(transaction: dict) -> list[str]:
    flags = []

    if transaction.get("amount", 0) > 10000:
        flags.append("HIGH_VALUE_TRANSACTION")

    if transaction.get("transaction_frequency", 0) > 20:
        flags.append("HIGH_TRANSACTION_FREQUENCY")

    if transaction.get("international", False):
        flags.append("INTERNATIONAL_TRANSACTION")

    if (
        transaction.get("sender_type") == "business"
        and transaction.get("receiver_type") == "personal"
    ):
        flags.append("BUSINESS_TO_PERSONAL_TRANSFER")

    if not transaction.get("sender_kyc_verified", False):
        flags.append("SENDER_KYC_NOT_VERIFIED")

    if not transaction.get("receiver_kyc_verified", False):
        flags.append("RECEIVER_KYC_NOT_VERIFIED")

    if not transaction.get("ecocash_connected", False):
        flags.append("ECOCASH_NOT_CONNECTED")

    return flags


def calculate_aml_risk_score(flags: list[str]) -> int:
    return len(flags)


def classify_aml_risk(risk_score: int) -> str:
    if risk_score >= 4:
        return "HIGH"

    if risk_score >= 2:
        return "MEDIUM"

    return "LOW"


def determine_aml_action(risk_level: str) -> str:
    if risk_level == "HIGH":
        return "BLOCK"

    if risk_level == "MEDIUM":
        return "REVIEW"

    return "ALLOW"


def explain_aml_result(
    risk_level: str,
    risk_score: int,
    flags: list[str],
) -> str:
    if risk_level == "HIGH":
        return (
            f"High AML risk detected with {risk_score} risk indicators. "
            f"Suspicious activity requires blocking and compliance investigation. "
            f"Flags: {', '.join(flags)}."
        )

    if risk_level == "MEDIUM":
        return (
            f"Medium AML risk detected with {risk_score} risk indicators. "
            f"Transaction requires compliance review. "
            f"Flags: {', '.join(flags)}."
        )

    return "Low AML risk detected. No significant suspicious activity indicators were identified."


def analyze_aml(transaction: dict) -> AMLResult:
    flags = detect_aml_flags(transaction)
    risk_score = calculate_aml_risk_score(flags)
    risk_level = classify_aml_risk(risk_score)
    recommended_action = determine_aml_action(risk_level)
    reason = explain_aml_result(
        risk_level,
        risk_score,
        flags,
    )

    return AMLResult(
        risk_level=risk_level,
        risk_score=risk_score,
        flags=flags,
        recommended_action=recommended_action,
        reason=reason,
    )


if __name__ == "__main__":
    example_transaction = {
        "transaction_id": "TX_AML_TEST",
        "amount": 18000.00,
        "sender_type": "business",
        "receiver_type": "personal",
        "transaction_type": "transfer",
        "sender_kyc_verified": False,
        "receiver_kyc_verified": True,
        "ecocash_connected": False,
        "transaction_frequency": 25,
        "international": True,
    }

    result = analyze_aml(example_transaction)

    print("BANKGUARD AI AML DETECTION AGENT")
    print("--------------------------------")
    print(f"AML Risk Level: {result.risk_level}")
    print(f"AML Risk Score: {result.risk_score}")
    print(f"Recommended Action: {result.recommended_action}")
    print(f"AML Flags: {', '.join(result.flags)}")
    print(f"Reason: {result.reason}")
