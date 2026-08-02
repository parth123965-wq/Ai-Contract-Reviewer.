from pydantic import BaseModel


class AnalysisResult(BaseModel):
    summary: str
    risk_score: int
    risk: str
    suggestions: list[str]
    error: str | None
    prompt: str
    llm_response: str
    analysis_result: AnalysisResult | None
    confidence: float