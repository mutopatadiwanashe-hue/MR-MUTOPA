from security.unified_security_controller import process_transaction_security


def create_high_risk_transaction():
    return {
        "transaction_id": "TX_RAG_INTEGRATION_TEST",
        "amount": 18000,
        "sender_type": "business",
        "receiver_type": "personal",
        "transaction_type": "transfer",
        "sender_kyc_verified": False,
        "receiver_kyc_verified": True,
        "ecocash_connected": False,
        "transaction_frequency": 25,
        "international": True,
    }


def test_security_controller_returns_compliance_knowledge():
    transaction = create_high_risk_transaction()

    response = process_transaction_security(transaction)

    assert response.compliance_knowledge is not None
    assert len(response.compliance_knowledge.rules) > 0


def test_rag_integration_does_not_change_high_risk_decision():
    transaction = create_high_risk_transaction()

    response = process_transaction_security(transaction)

    assert response.decision_result.final_risk_level == "HIGH"
    assert response.decision_result.final_decision == "BLOCK"


def test_rag_returns_relevant_compliance_rules():
    transaction = create_high_risk_transaction()

    response = process_transaction_security(transaction)

    rule_text = " ".join(
        rule.content
        for rule in response.compliance_knowledge.rules
    )

    assert "KYC" in rule_text
    assert "INTERNATIONAL" in rule_text or "international" in rule_text
    assert "LARGE" in rule_text