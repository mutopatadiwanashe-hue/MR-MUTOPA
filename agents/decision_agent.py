from dataclasses import dataclass

from agents.aml_agent import analyze_aml
from agents.fraud_agent import analyze_transaction
from agents.kyc_agent import analyze_kyc


@dataclass
class DecisionResult:
    final_risk_level: str
    final_decision: str
    fraud_risk: str
    kyc_risk: str
    aml_risk: str
    reasons: list[str]


def calculate_final_risk(
    fraud_risk: str,
    kyc_risk: str,
    aml_risk: str,
) -> str:
    risk_levels = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
    }

    highest_risk = max(
        fraud_risk,
        kyc_risk,
        aml_risk,
        key=lambda risk: risk_levels[risk],
    )

    return highest_risk


def determine_final_decision(risk_level: str) -> str:
    if risk_level == "HIGH":
        return "BLOCK"

    if risk_level == "MEDIUM":
        return "REVIEW"

    return "ALLOW"


def combine_reasons(
    fraud_result,
    kyc_result,
    aml_result,
) -> list[str]:
    reasons = [
        f"Fraud Agent: {fraud_result.reason}",
        f"KYC Agent: {kyc_result.reason}",
        f"AML Agent: {aml_result.reason}",
    ]

    return reasons


def make_final_decision(transaction: dict) -> DecisionResult:
    fraud_result = analyze_transaction(transaction)

    kyc_result = analyze_kyc(
        transaction.get("sender_kyc_verified", False),
        transaction.get("receiver_kyc_verified", False),
    )

    aml_result = analyze_aml(transaction)

    final_risk_level = calculate_final_risk(
        fraud_result.risk_level,
        kyc_result.risk_level,
        aml_result.risk_level,
    )

    final_decision = determine_final_decision(final_risk_level)

    reasons = combine_reasons(
        fraud_result,
        kyc_result,
        aml_result,
    )

    return DecisionResult(
        final_risk_level=final_risk_level,
        final_decision=final_decision,
        fraud_risk=fraud_result.risk_level,
        kyc_risk=kyc_result.risk_level,
        aml_risk=aml_result.risk_level,
        reasons=reasons,
    )


if __name__ == "__main__":
    example_transaction = {
        "transaction_id": "TX_DECISION_TEST",
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

    result = make_final_decision(example_transaction)

    print("BANKGUARD AI UNIFIED DECISION AGENT")
    print("-----------------------------------")
    print(f"Fraud Risk: {result.fraud_risk}")
    print(f"KYC Risk: {result.kyc_risk}")
    print(f"AML Risk: {result.aml_risk}")
    print(f"Final Risk Level: {result.final_risk_level}")
    print(f"Final Decision: {result.final_decision}")
    print("Reasons:")

    for reason in result.reasons:
        print(f"- {reason}")
