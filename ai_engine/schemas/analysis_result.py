from pydantic import BaseModel


class AnalysisResult(BaseModel):
    summary: str
    risk_score: int
    suggestions: list[str]
    error: str | None
