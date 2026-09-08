from rag.knowledge_service import ComplianceKnowledgeResult, get_compliance_knowledge


def build_compliance_query(transaction: dict) -> str:
    query_parts = []

    amount = transaction.get("amount", 0)

    if amount >= 10000:
        query_parts.append("large transaction monitoring")

    if transaction.get("transaction_frequency", 0) > 20:
        query_parts.append("high transaction frequency unusual activity")

    if transaction.get("international", False):
        query_parts.append("international transaction money laundering")

    if (
        transaction.get("sender_type") == "business"
        and transaction.get("receiver_type") == "personal"
    ):
        query_parts.append("business to personal transfer")

    if not transaction.get("sender_kyc_verified", False):
        query_parts.append("customer KYC verification")

    if not transaction.get("receiver_kyc_verified", False):
        query_parts.append("customer KYC verification")

    if not query_parts:
        query_parts.append("general banking security compliance")

    return " ".join(query_parts)


def get_transaction_compliance_knowledge(
    transaction: dict,
    top_k: int = 3,
) -> ComplianceKnowledgeResult:

    query = build_compliance_query(transaction)

    return get_compliance_knowledge(
        query=query,
        top_k=top_k,
    )