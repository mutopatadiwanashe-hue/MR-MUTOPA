from dataclasses import dataclass


@dataclass
class KYCResult:
    kyc_status: str
    risk_level: str
    recommended_action: str
    reason: str


def assess_kyc_status(
    sender_kyc_verified: bool,
    receiver_kyc_verified: bool,
) -> str:
    if sender_kyc_verified and receiver_kyc_verified:
        return "VERIFIED"

    if not sender_kyc_verified and not receiver_kyc_verified:
        return "BOTH_NOT_VERIFIED"

    if not sender_kyc_verified:
        return "SENDER_NOT_VERIFIED"

    return "RECEIVER_NOT_VERIFIED"


def classify_kyc_risk(kyc_status: str) -> str:
    if kyc_status == "VERIFIED":
        return "LOW"

    if kyc_status in {"SENDER_NOT_VERIFIED", "RECEIVER_NOT_VERIFIED"}:
        return "MEDIUM"

    return "HIGH"


def determine_kyc_action(risk_level: str) -> str:
    if risk_level == "LOW":
        return "ALLOW"

    if risk_level == "MEDIUM":
        return "REVIEW"

    return "BLOCK"


def explain_kyc_result(kyc_status: str, risk_level: str) -> str:
    if kyc_status == "VERIFIED":
        return "Both sender and receiver have verified KYC information."

    if kyc_status == "SENDER_NOT_VERIFIED":
        return "Sender KYC verification is missing. Transaction requires review."

    if kyc_status == "RECEIVER_NOT_VERIFIED":
        return "Receiver KYC verification is missing. Transaction requires review."

    return "Both sender and receiver have unverified KYC information. Transaction should be blocked."


def analyze_kyc(
    sender_kyc_verified: bool,
    receiver_kyc_verified: bool,
) -> KYCResult:
    kyc_status = assess_kyc_status(
        sender_kyc_verified,
        receiver_kyc_verified,
    )

    risk_level = classify_kyc_risk(kyc_status)
    recommended_action = determine_kyc_action(risk_level)
    reason = explain_kyc_result(
        kyc_status,
        risk_level,
    )

    return KYCResult(
        kyc_status=kyc_status,
        risk_level=risk_level,
        recommended_action=recommended_action,
        reason=reason,
    )


if __name__ == "__main__":
    result = analyze_kyc(
        sender_kyc_verified=False,
        receiver_kyc_verified=True,
    )

    print("BANKGUARD AI KYC COMPLIANCE AGENT")
    print("---------------------------------")
    print(f"KYC Status: {result.kyc_status}")
    print(f"Risk Level: {result.risk_level}")
    print(f"Recommended Action: {result.recommended_action}")
    print(f"Reason: {result.reason}")
