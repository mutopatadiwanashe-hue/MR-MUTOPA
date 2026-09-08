from dataclasses import dataclass
from pathlib import Path

import joblib
import pandas as pd


MODEL_FILE = Path("models/fraud_detection_model.pkl")


@dataclass
class FraudAgentResult:
    prediction: int
    fraud_probability: float
    risk_level: str
    recommended_action: str
    reason: str


def classify_fraud_risk(probability: float) -> str:
    if probability >= 0.80:
        return "HIGH"

    if probability >= 0.50:
        return "MEDIUM"

    return "LOW"


def determine_fraud_action(risk_level: str) -> str:
    if risk_level == "HIGH":
        return "BLOCK"

    if risk_level == "MEDIUM":
        return "REVIEW"

    return "ALLOW"


def explain_fraud_result(
    risk_level: str,
    probability: float,
) -> str:

    if risk_level == "HIGH":
        return (
            f"High probability of fraudulent activity "
            f"({probability:.2%}). Transaction should be blocked."
        )

    if risk_level == "MEDIUM":
        return (
            f"Moderate probability of fraudulent activity "
            f"({probability:.2%}). Transaction requires review."
        )

    return (
        f"Low probability of fraudulent activity "
        f"({probability:.2%}). Transaction can be allowed."
    )


def analyze_transaction(transaction: dict) -> FraudAgentResult:

    model = joblib.load(MODEL_FILE)

    transaction_data = pd.DataFrame([transaction])

    prediction = int(model.predict(transaction_data)[0])

    probability = float(
        model.predict_proba(transaction_data)[0][1]
    )

    risk_level = classify_fraud_risk(probability)

    recommended_action = determine_fraud_action(
        risk_level
    )

    reason = explain_fraud_result(
        risk_level,
        probability,
    )

    return FraudAgentResult(
        prediction=prediction,
        fraud_probability=probability,
        risk_level=risk_level,
        recommended_action=recommended_action,
        reason=reason,
    )


if __name__ == "__main__":

    example_transaction = {
        "transaction_id": "TX_AGENT_TEST",
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

    result = analyze_transaction(
        example_transaction
    )

    print("BANKGUARD AI FRAUD AGENT")
    print("-------------------------")
    print(f"Prediction: {result.prediction}")
    print(
        f"Fraud Probability: "
        f"{result.fraud_probability:.2%}"
    )
    print(f"Risk Level: {result.risk_level}")
    print(
        f"Recommended Action: "
        f"{result.recommended_action}"
    )
    print(f"Reason: {result.reason}")
