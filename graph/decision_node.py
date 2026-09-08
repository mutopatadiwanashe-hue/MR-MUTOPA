from agents.decision_agent import (
    DecisionResult,
    calculate_final_risk,
    determine_final_decision,
)

from graph.bankguard_workflow import BankGuardWorkflowState


def run_decision_node(
    state: BankGuardWorkflowState,
) -> BankGuardWorkflowState:

    fraud_result = state.fraud_result
    kyc_result = state.kyc_result
    aml_result = state.aml_result

    if fraud_result is None or kyc_result is None or aml_result is None:
        raise ValueError(
            "Fraud, KYC and AML results are required before running the decision node."
        )

    final_risk_level = calculate_final_risk(
        fraud_result.risk_level,
        kyc_result.risk_level,
        aml_result.risk_level,
    )

    final_decision = determine_final_decision(
        final_risk_level
    )

    reasons = [
        f"Fraud Agent: {fraud_result.reason}",
        f"KYC Agent: {kyc_result.reason}",
        f"AML Agent: {aml_result.reason}",
    ]

    state.decision_result = DecisionResult(
        final_risk_level=final_risk_level,
        final_decision=final_decision,
        fraud_risk=fraud_result.risk_level,
        kyc_risk=kyc_result.risk_level,
        aml_risk=aml_result.risk_level,
        reasons=reasons,
    )

    return state