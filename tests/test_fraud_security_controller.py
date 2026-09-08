from security.fraud_security_controller import create_fraud_security_response


def high_risk_transaction():
    return {
        "transaction_id": "TX_HIGH_TEST",
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


def test_high_risk_creates_critical_alert():
    response = create_fraud_security_response(high_risk_transaction())

    assert response.fraud_result.risk_level == "HIGH"
    assert response.fraud_result.recommended_action == "BLOCK"
    assert response.alert is not None
    assert response.alert.level == "CRITICAL"
    assert response.alert.alert_type == "HIGH_RISK_TRANSACTION"


def test_high_risk_requires_admin():
    response = create_fraud_security_response(high_risk_transaction())

    assert response.alert.requires_admin is True


def test_high_risk_locks_system():
    response = create_fraud_security_response(high_risk_transaction())

    assert response.alert.requires_lock is True
    assert response.security_lock is not None
    assert response.security_lock.locked is True


def test_fraud_probability_is_valid():
    response = create_fraud_security_response(high_risk_transaction())

    assert 0.0 <= response.fraud_result.fraud_probability <= 1.0
