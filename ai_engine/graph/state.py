from typing import TypedDict

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