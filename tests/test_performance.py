import time

from graph.workflow_runner import run_bankguard_workflow


def test_workflow_performance():
    transaction = {
        "transaction_id": "PERF_TEST_001",
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

    start_time = time.perf_counter()

    state = run_bankguard_workflow(transaction)

    elapsed_time = time.perf_counter() - start_time

    assert state.decision_result is not None
    assert elapsed_time > 0

    print(f"Workflow execution time: {elapsed_time:.4f} seconds")