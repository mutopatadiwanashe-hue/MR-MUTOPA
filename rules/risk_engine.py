from dataclasses import dataclass

from database.transaction_schema import Transaction
from rules.transaction_rules import (
    check_high_value_transaction,
    check_business_to_personal_transfer,
    check_kyc_verification,
)


@dataclass
class RiskAssessment:
    transaction_id: str
    risk_level: str
    flags: list[str]
    flag_count: int
    recommended_action: str


def assess_transaction_risk(transaction: Transaction) -> list[str]:
    flags = []

    high_value_flag = check_high_value_transaction(transaction)
    if high_value_flag:
        flags.append(high_value_flag)

    business_personal_flag = check_business_to_personal_transfer(transaction)
    if business_personal_flag:
        flags.append(business_personal_flag)

    kyc_flag = check_kyc_verification(transaction)
    if kyc_flag:
        flags.append(kyc_flag)

    return flags


def classify_risk_severity(flags: list[str]) -> str:
    if len(flags) == 0:
        return "LOW"

    if len(flags) == 1:
        return "MEDIUM"

    return "HIGH"


def determine_recommended_action(risk_level: str) -> str:
    if risk_level == "LOW":
        return "ALLOW"

    if risk_level == "MEDIUM":
        return "REVIEW"

    return "BLOCK"


def generate_risk_assessment(transaction: Transaction) -> RiskAssessment:
    flags = assess_transaction_risk(transaction)
    risk_level = classify_risk_severity(flags)
    recommended_action = determine_recommended_action(risk_level)

    return RiskAssessment(
        transaction_id=transaction.transaction_id,
        risk_level=risk_level,
        flags=flags,
        flag_count=len(flags),
        recommended_action=recommended_action,
    )