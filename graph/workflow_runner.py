from graph.bankguard_workflow import (
    BankGuardWorkflowState,
    create_workflow_state,
)
from graph.fraud_node import run_fraud_node
from graph.kyc_node import run_kyc_node
from graph.aml_node import run_aml_node
from graph.monitoring_node import run_monitoring_node
from graph.rag_node import run_rag_node
from graph.decision_node import run_decision_node
from graph.security_response_node import run_security_response_node


def run_bankguard_workflow(
    transaction: dict,
) -> BankGuardWorkflowState:

    state = create_workflow_state(transaction)

    state = run_fraud_node(state)
    state = run_kyc_node(state)
    state = run_aml_node(state)
    state = run_monitoring_node(state)
    state = run_rag_node(state)
    state = run_decision_node(state)
    state = run_security_response_node(state)

    return state