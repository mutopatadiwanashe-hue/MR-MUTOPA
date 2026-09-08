from dataclasses import dataclass

from rag.document_loader import load_compliance_documents


@dataclass
class ComplianceChunk:
    source: str
    content: str


def split_into_chunks(content: str) -> list[str]:
    sections = content.split("\n\n")

    return [
        section.strip()
        for section in sections
        if section.strip()
    ]


def load_compliance_chunks() -> list[ComplianceChunk]:
    documents = load_compliance_documents()

    chunks = []

    for document in documents:
        for section in split_into_chunks(document.content):
            chunks.append(
                ComplianceChunk(
                    source=document.source,
                    content=section,
                )
            )

    return chunks


def normalize_query(query: str) -> set[str]:
    query = query.lower()

    replacements = {
        "verification": "verify",
        "verified": "verify",
        "transactions": "transaction",
        "transfers": "transfer",
        "international": "international",
        "money laundering": "laundering",
    }

    for old, new in replacements.items():
        query = query.replace(old, new)

    return set(query.split())


def calculate_score(query_words: set[str], content: str) -> int:
    content_lower = content.lower()
    content_words = set(content_lower.split())

    score = len(query_words.intersection(content_words))

    keyword_groups = {
        "kyc": ["kyc", "customer", "identity", "verify"],
        "large": ["large", "value", "amount"],
        "transaction": ["transaction", "monitoring"],
        "international": ["international", "cross-border"],
        "business": ["business", "personal"],
        "risk": ["risk", "high-risk"],
        "review": ["review", "compliance"],
        "audit": ["audit", "trail"],
        "human": ["human", "compliance", "review"],
        "security": ["security", "fraud", "aml"],
    }

    for query_word, keywords in keyword_groups.items():
        if query_word in query_words:
            score += sum(
                2 for keyword in keywords
                if keyword in content_lower
            )

    return score


def retrieve_compliance_rules(
    query: str,
    top_k: int = 3,
) -> list[ComplianceChunk]:

    chunks = load_compliance_chunks()

    query_words = normalize_query(query)

    scored_chunks = []

    for chunk in chunks:
        score = calculate_score(
            query_words,
            chunk.content,
        )

        if score > 0:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        chunk
        for score, chunk in scored_chunks[:top_k]
    ]