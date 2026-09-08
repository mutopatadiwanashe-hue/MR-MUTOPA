from graph.workflow_runner import run_bankguard_workflow


def high_risk_transaction():
    return {
        "transaction_id": "TX_WORKFLOW_TEST",
        "transaction_type": "transfer",
        "amount": 18000,
        "sender_type": "business",
        "receiver_type": "personal",
        "sender_kyc_verified": False,
        "receiver_kyc_verified": True,
        "ecocash_connected": False,
        "transaction_frequency": 25,
        "international": True,
    }


def test_full_workflow_high_risk_transaction():
    state = run_bankguard_workflow(high_risk_transaction())

    assert state.fraud_result is not None
    assert state.kyc_result is not None
    assert state.aml_result is not None
    assert state.transaction_monitor_result is not None
    assert state.compliance_knowledge is not None
    assert state.decision_result is not None
    assert state.security_response is not None

    assert state.decision_result.final_risk_level == "HIGH"
    assert state.decision_result.final_decision == "BLOCK"

    assert state.transaction_monitor_result.flagged is True

    assert len(state.compliance_knowledge.rules) == 3

    assert state.security_response["security_lock"] is not None
    assert state.security_response["security_lock"].locked is True


def test_full_workflow_normal_transaction():
    transaction = {
        "transaction_id": "TX_NORMAL_WORKFLOW_TEST",
        "transaction_type": "transfer",
        "amount": 500,
        "sender_type": "personal",
        "receiver_type": "personal",
        "sender_kyc_verified": True,
        "receiver_kyc_verified": True,
        "ecocash_connected": True,
        "transaction_frequency": 2,
        "international": False,
    }

    state = run_bankguard_workflow(transaction)

    assert state.decision_result is not None
    assert state.decision_result.final_risk_level == "LOW"
    assert state.decision_result.final_decision == "ALLOW"

    assert state.transaction_monitor_result.flagged is False

    assert state.security_response is not None
    assert state.security_response["security_lock"] is None