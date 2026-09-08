from rag.transaction_context import get_transaction_compliance_knowledge

from graph.bankguard_workflow import BankGuardWorkflowState


def run_rag_node(
    state: BankGuardWorkflowState,
) -> BankGuardWorkflowState:

    state.compliance_knowledge = get_transaction_compliance_knowledge(
        state.transaction,
        top_k=3,
    )

    return state