from database.audit_repository import load_audit_logs
from database.audit_log import create_audit_log
from security.unified_security_controller import process_transaction_security


def test_high_risk_transaction_audit_data():
    transaction = {
        "transaction_id": "TX_AUDIT_HIGH_TEST",
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

    assert response.decision_result.final_risk_level == "HIGH"
    assert response.decision_result.final_decision == "BLOCK"
    assert response.audit_log is not None
    assert response.audit_log.transaction_id == "TX_AUDIT_HIGH_TEST"
    assert response.audit_log.risk_level == "HIGH"
    assert response.audit_log.decision == "BLOCK"


def test_audit_log_structure():
    log = create_audit_log(
        transaction_id="TX_AUDIT_STRUCTURE_TEST",
        risk_level="MEDIUM",
        decision="REVIEW",
        reason="Transaction requires compliance review.",
        flags=["KYC_NOT_VERIFIED"],
    )

    assert log.transaction_id == "TX_AUDIT_STRUCTURE_TEST"
    assert log.risk_level == "MEDIUM"
    assert log.decision == "REVIEW"
    assert log.reason == "Transaction requires compliance review."
    assert log.flags == ["KYC_NOT_VERIFIED"]
    assert log.timestamp is not None


def test_controller_transaction_is_persisted():
    transaction_id = "TX_AUDIT_PERSISTENCE_TEST"

    transaction = {
        "transaction_id": transaction_id,
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

    process_transaction_security(transaction)

    logs = load_audit_logs()

    matching_logs = [
        log for log in logs
        if log.get("transaction_id") == transaction_id
    ]

    assert matching_logs

    latest = matching_logs[-1]

    assert latest["transaction_id"] == transaction_id
    assert latest["risk_level"] == "HIGH"
    assert latest["decision"] == "BLOCK"
    assert "timestamp" in latest
    assert "reason" in latest
    assert "flags" in latest


if __name__ == "__main__":
    test_high_risk_transaction_audit_data()
    test_audit_log_structure()
    test_controller_transaction_is_persisted()
    print("All audit integration tests passed.")
