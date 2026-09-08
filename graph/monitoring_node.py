from security.transaction_monitor import monitor_transaction

from graph.bankguard_workflow import BankGuardWorkflowState


def run_monitoring_node(
    state: BankGuardWorkflowState,
) -> BankGuardWorkflowState:

    state.transaction_monitor_result = monitor_transaction(
        amount=state.transaction.get("amount", 0),
        sender_type=state.transaction.get("sender_type", ""),
        receiver_type=state.transaction.get("receiver_type", ""),
    )

    return state