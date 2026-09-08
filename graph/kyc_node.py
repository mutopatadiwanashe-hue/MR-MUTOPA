from agents.kyc_agent import analyze_kyc

from graph.bankguard_workflow import BankGuardWorkflowState


def run_kyc_node(
    state: BankGuardWorkflowState,
) -> BankGuardWorkflowState:

    state.kyc_result = analyze_kyc(
        state.transaction.get(
            "sender_kyc_verified",
            False,
        ),
        state.transaction.get(
            "receiver_kyc_verified",
            False,
        ),
    )

    return state