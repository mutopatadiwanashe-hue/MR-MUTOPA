from graph.workflow_runner import run_bankguard_workflow


def test_evaluation_low_risk_transaction():
    transaction = {
        "transaction_id": "EVAL_LOW_001",
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

    assert state.decision_result.final_risk_level == "LOW"
    assert state.decision_result.final_decision == "ALLOW"


def test_evaluation_medium_risk_transaction():
    transaction = {
        "transaction_id": "EVAL_MEDIUM_001",
        "transaction_type": "transfer",
        "amount": 5000,
        "sender_type": "personal",
        "receiver_type": "personal",
        "sender_kyc_verified": False,
        "receiver_kyc_verified": True,
        "ecocash_connected": True,
        "transaction_frequency": 2,
        "international": False,
    }

    state = run_bankguard_workflow(transaction)

    assert state.decision_result.final_risk_level == "MEDIUM"
    assert state.decision_result.final_decision == "REVIEW"


def test_evaluation_high_risk_transaction():
    transaction = {
        "transaction_id": "EVAL_HIGH_001",
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

    state = run_bankguard_workflow(transaction)

    assert state.decision_result.final_risk_level == "HIGH"
    assert state.decision_result.final_decision == "BLOCK"