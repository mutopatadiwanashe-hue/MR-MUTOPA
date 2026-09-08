from agents.fraud_agent import analyze_transaction

from graph.bankguard_workflow import BankGuardWorkflowState


def run_fraud_node(
    state: BankGuardWorkflowState,
) -> BankGuardWorkflowState:

    state.fraud_result = analyze_transaction(
        state.transaction
    )

    return state