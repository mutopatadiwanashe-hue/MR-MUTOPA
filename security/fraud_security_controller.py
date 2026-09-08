from dataclasses import dataclass

from agents.fraud_agent import analyze_transaction
from security.alert_engine import SecurityAlert, generate_security_alert
from security.lock_manager import SecurityLock, create_lock


@dataclass
class FraudSecurityResponse:
    fraud_result: object
    alert: SecurityAlert | None
    security_lock: SecurityLock | None


def create_fraud_security_response(transaction: dict) -> FraudSecurityResponse:
    fraud_result = analyze_transaction(transaction)

    decision = fraud_result.recommended_action

    alert = generate_security_alert(
        fraud_result.risk_level,
        decision,
    )

    security_lock = None

    if alert is not None and alert.requires_lock:
        security_lock = create_lock(
            reason="Fraudulent transaction detected by BankGuard AI."
        )

    return FraudSecurityResponse(
        fraud_result=fraud_result,
        alert=alert,
        security_lock=security_lock,
    )


if __name__ == "__main__":
    transaction = {
        "transaction_id": "TX_SECURITY_TEST",
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

    response = create_fraud_security_response(transaction)

    print("BANKGUARD AI FRAUD SECURITY CONTROLLER")
    print("--------------------------------------")
    print(f"Fraud Risk: {response.fraud_result.risk_level}")
    print(f"Fraud Probability: {response.fraud_result.fraud_probability:.2%}")
    print(f"Decision: {response.fraud_result.recommended_action}")

    if response.alert:
        print(f"Alert Level: {response.alert.level}")
        print(f"Alert Type: {response.alert.alert_type}")
        print(f"System Lock Required: {response.alert.requires_lock}")
        print(f"Admin Required: {response.alert.requires_admin}")
    else:
        print("Alert Level: NONE")
        print("Alert Type: NONE")

    print(f"System Locked: {response.security_lock is not None}")
