from dataclasses import dataclass

from database.transaction_schema import Transaction
from rules.risk_engine import generate_risk_assessment, RiskAssessment


@dataclass
class RiskDecision:
    transaction_id: str
    risk_level: str
    decision: str
    reason: str


def make_risk_decision(transaction: Transaction) -> RiskDecision:
    assessment: RiskAssessment = generate_risk_assessment(transaction)

    if assessment.risk_level == "LOW":
        decision = "ALLOW"
        reason = "Transaction passed all current risk checks."

    elif assessment.risk_level == "MEDIUM":
        decision = "REVIEW"
        reason = "Transaction requires compliance review."

    else:
        decision = "BLOCK"
        reason = "Transaction triggered multiple high-risk indicators."

    return RiskDecision(
        transaction_id=assessment.transaction_id,
        risk_level=assessment.risk_level,
        decision=decision,
        reason=reason,
    )