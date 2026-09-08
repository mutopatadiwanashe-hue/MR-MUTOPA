from rag.knowledge_service import get_compliance_knowledge
from rag.retriever import retrieve_compliance_rules


def test_kyc_query_returns_kyc_rule():
    results = retrieve_compliance_rules(
        "customer KYC verification",
        top_k=2,
    )

    assert len(results) >= 1
    assert "RULE 1" in results[0].content
    assert "KYC" in results[0].content


def test_large_transaction_query_returns_large_transaction_rule():
    results = retrieve_compliance_rules(
        "large transaction monitoring money laundering",
        top_k=3,
    )

    assert len(results) >= 1
    assert "RULE 2" in results[0].content
    assert "LARGE TRANSACTIONS" in results[0].content


def test_knowledge_service_returns_result():
    result = get_compliance_knowledge(
        "international transaction",
        top_k=2,
    )

    assert result.query == "international transaction"
    assert len(result.rules) >= 1


def test_unknown_query_returns_empty_results():
    results = retrieve_compliance_rules(
        "banana spaceship weather",
        top_k=3,
    )

    assert results == []