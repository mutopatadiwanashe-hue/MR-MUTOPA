from dataclasses import dataclass

from agents.decision_agent import make_final_decision
from security.account_control import check_business_to_personal_control
from security.transaction_monitor import monitor_transaction
from security.alert_engine import SecurityAlert, generate_security_alert
from security.lock_manager import SecurityLock, create_lock


@dataclass
class UnifiedSecurityResponse:
    decision_result: object
    alert: SecurityAlert | None
    security_lock: SecurityLock | None
    account_control: object
    transaction_monitor: object


def process_transaction_security(transaction: dict) -> UnifiedSecurityResponse:

    # Stage 10: Account-control rules
    account_control = check_business_to_personal_control(
        transaction.get("sender_type", ""),
        transaction.get("receiver_type", ""),
    )

    # Stage 10: Transaction monitoring
    transaction_monitor = monitor_transaction(
        amount=transaction.get("amount", 0),
        sender_type=transaction.get("sender_type", ""),
        receiver_type=transaction.get("receiver_type", ""),
    )

    # Existing BankGuard AI decision engine
    decision_result = make_final_decision(transaction)

    # Existing security alert engine
    alert = generate_security_alert(
        decision_result.final_risk_level,
        decision_result.final_decision,
    )

    security_lock = None

    # Lock high-risk AI decisions
    if alert is not None and alert.requires_lock:
        security_lock = create_lock(
            reason="High-risk transaction blocked by BankGuard AI.",
        )

    # Account-control violations also require administrator review
    if account_control.requires_admin:
        if security_lock is None:
            security_lock = create_lock(
                reason=account_control.warning,
            )

    return UnifiedSecurityResponse(
        decision_result=decision_result,
        alert=alert,
        security_lock=security_lock,
        account_control=account_control,
        transaction_monitor=transaction_monitor,
    )


if __name__ == "__main__":
    transaction = {
        "transaction_id": "TX_UNIFIED_SECURITY_TEST",
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

    response = process_transaction_security(transaction)

    print("BANKGUARD AI UNIFIED SECURITY CONTROLLER")
    print("----------------------------------------")

    print(f"Account Control Allowed: {response.account_control.allowed}")
    print(f"Admin Required: {response.account_control.requires_admin}")
    print(f"Account Warning: {response.account_control.warning}")

    print(f"Transaction Flagged: {response.transaction_monitor.flagged}")
    print(f"Monitoring Reasons: {response.transaction_monitor.reasons}")
    print(f"Review Required: {response.transaction_monitor.requires_review}")

    print(f"Fraud Risk: {response.decision_result.fraud_risk}")
    print(f"KYC Risk: {response.decision_result.kyc_risk}")
    print(f"AML Risk: {response.decision_result.aml_risk}")
    print(f"Final Risk: {response.decision_result.final_risk_level}")
    print(f"Final Decision: {response.decision_result.final_decision}")

    if response.alert:
        print(f"Alert Level: {response.alert.level}")
        print(f"Alert Type: {response.alert.alert_type}")
        print(f"System Lock Required: {response.alert.requires_lock}")
        print(f"Alert Admin Required: {response.alert.requires_admin}")
    else:
        print("Alert Level: NONE")

    print(f"System Locked: {response.security_lock is not None}")
