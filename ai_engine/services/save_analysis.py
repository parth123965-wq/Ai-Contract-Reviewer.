from sqlalchemy.orm import Session
from ai_engine.schemas.analysis_result import AnalysisResult
from app.models.contract import ContractAnalysis
from app.repositories.analysis_repository import AnalysisRepository

class AnalysisService:

    def __init__(self):
        self.analysis_repository = AnalysisRepository()

    def save_analysis(
        self,
        db: Session,
        contract_id: int,
        result: AnalysisResult,
        model_name: str,
        processing_time_ms: int,
        analysis_version: int = 1
    ) -> ContractAnalysis:
        analysis = ContractAnalysis(
            contract_id=contract_id,
            summary=result.summary,
            risk_score=result.risk_score,
            risk_level=result.risk,
            recommendations="\n".join(result.suggestions),
            high_risk_clause=None,
            model_name=model_name,
            confidence_score=result.confidence,
            processing_time_ms=processing_time_ms,
            analysis_version=analysis_version
        )

        return self.analysis_repository.create_analysis(
            db=db,
            analysis=analysis
        )