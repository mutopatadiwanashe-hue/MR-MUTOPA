from security.unified_security_controller import process_transaction_security


def suspicious_transaction():
    return {
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


def clean_transaction():
    return {
        "transaction_id": "TX_CLEAN_SECURITY",
        "amount": 500.00,
        "sender_type": "personal",
        "receiver_type": "business",
        "transaction_type": "payment",
        "sender_kyc_verified": True,
        "receiver_kyc_verified": True,
        "ecocash_connected": True,
        "transaction_frequency": 2,
        "international": False,
    }


def test_suspicious_transaction_is_blocked_and_locked():
    response = process_transaction_security(suspicious_transaction())

    assert response.decision_result.final_risk_level == "HIGH"
    assert response.decision_result.final_decision == "BLOCK"
    assert response.alert is not None
    assert response.alert.level == "CRITICAL"
    assert response.alert.requires_lock is True
    assert response.alert.requires_admin is True
    assert response.security_lock is not None
    assert response.security_lock.locked is True


def test_clean_transaction_is_allowed_and_not_locked():
    response = process_transaction_security(clean_transaction())

    assert response.decision_result.final_risk_level == "LOW"
    assert response.decision_result.final_decision == "ALLOW"
    assert response.alert is None
    assert response.security_lock is None
