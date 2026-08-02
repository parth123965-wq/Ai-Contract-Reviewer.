from typing import TypedDict
from sqlalchemy.orm import Session

class ContractState(TypedDict):
    contract_id: int
    user_id: int
    file_path: str
    extracted_text: str
    chunks: list[str]
    embeddings: list[list[float]]
    retrieved_chunks: list[str]
    summary: str
    risk_score: int
    suggestions: list[str]
    analysis_version: int
    status: str
    error: str | None
    query_embedding: list[float]
    db: Session