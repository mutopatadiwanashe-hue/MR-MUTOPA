from dataclasses import dataclass

from rag.retriever import ComplianceChunk, retrieve_compliance_rules


@dataclass
class ComplianceKnowledgeResult:
    query: str
    rules: list[ComplianceChunk]


def get_compliance_knowledge(
    query: str,
    top_k: int = 3,
) -> ComplianceKnowledgeResult:

    rules = retrieve_compliance_rules(
        query=query,
        top_k=top_k,
    )

    return ComplianceKnowledgeResult(
        query=query,
        rules=rules,
    )