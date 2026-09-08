from graph.workflow_runner import run_bankguard_workflow


def test_workflow_reliability():
    transaction = {
        "transaction_id": "RELIABILITY_TEST_001",
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

    results = []

    for _ in range(10):
        state = run_bankguard_workflow(transaction)

        results.append(
            (
                state.decision_result.final_risk_level,
                state.decision_result.final_decision,
                state.transaction_monitor_result.flagged,
                state.security_response["security_lock"] is not None,
            )
        )

    expected = ("HIGH", "BLOCK", True, True)

    assert len(results) == 10
    assert all(result == expected for result in results)

    print(f"Successful workflow executions: {len(results)}")
    print(f"Consistent results: {all(result == expected for result in results)}")