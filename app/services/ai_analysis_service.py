from sqlalchemy.orm import Session

from app.models.contract import ContractAnalysis
from app.repositories.analysis_repository import AnalysisRepository

from ai_engine.schemas.analysis_result import AnalysisResult 


class AnalysisService:

    def __init__(self):
        self.analysis_repository = AnalysisRepository()

    def save_analysis(
        self,
        db: Session,
        contract_id: int,
        result: AnalysisResult,
        model_name: str,
        processing_time: float
    ):
        version = self.analysis_repository.get_next_analysis_version(
            db=db,
            contract_id=contract_id
        )

        analysis = ContractAnalysis(
            contract_id=contract_id,
            version=version,
            summary=result.summary,
            score=result.risk_score,
            risk=result.risk,
            risk_suggestion="\n".join(result.suggestions),
            model_name=model_name,
            process_time=processing_time,
        )

        return self.analysis_repository.create_analysis(
            db=db,
            analysis=analysis
        )
        
        
def aianalysisservice() -> AnalysisService:
    return AnalysisService()