from agents.aml_agent import analyze_aml

from graph.bankguard_workflow import BankGuardWorkflowState


def run_aml_node(
    state: BankGuardWorkflowState,
) -> BankGuardWorkflowState:

    state.aml_result = analyze_aml(
        state.transaction
    )

    return state