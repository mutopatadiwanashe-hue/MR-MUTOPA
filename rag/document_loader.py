from dataclasses import dataclass
from pathlib import Path


@dataclass
class ComplianceDocument:
    source: str
    content: str


def load_compliance_documents(
    knowledge_base_path: str = "rag/knowledge_base",
) -> list[ComplianceDocument]:

    knowledge_base = Path(knowledge_base_path)

    if not knowledge_base.exists():
        return []

    documents = []

    for file_path in knowledge_base.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        documents.append(
            ComplianceDocument(
                source=str(file_path),
                content=content,
            )
        )

    return documents