from rag.transaction_context import (
    build_compliance_query,
    get_transaction_compliance_knowledge,
)


def test_high_risk_transaction_builds_compliance_query():
    transaction = {
        "amount": 18000,
        "sender_type": "business",
        "receiver_type": "personal",
        "transaction_frequency": 25,
        "international": True,
        "sender_kyc_verified": False,
        "receiver_kyc_verified": True,
    }

    query = build_compliance_query(transaction)

    assert "large transaction monitoring" in query
    assert "high transaction frequency" in query
    assert "international transaction" in query
    assert "business to personal transfer" in query
    assert "customer KYC verification" in query


def test_normal_transaction_builds_general_compliance_query():
    transaction = {
        "amount": 1000,
        "sender_type": "personal",
        "receiver_type": "personal",
        "transaction_frequency": 2,
        "international": False,
        "sender_kyc_verified": True,
        "receiver_kyc_verified": True,
    }

    query = build_compliance_query(transaction)

    assert "general banking security compliance" in query


def test_transaction_compliance_knowledge_returns_rules():
    transaction = {
        "amount": 18000,
        "sender_type": "business",
        "receiver_type": "personal",
        "transaction_frequency": 25,
        "international": True,
        "sender_kyc_verified": False,
        "receiver_kyc_verified": True,
    }

    result = get_transaction_compliance_knowledge(
        transaction,
        top_k=3,
    )

    assert len(result.rules) >= 1
    assert "RULE" in result.rules[0].content