from sqlalchemy.orm import Session

from app.models.contract import ContractAnalysis
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.contract_repository import ContractRepository

from ai_engine.schemas.analysis_result import AnalysisResult


class AnalysisService:

    def __init__(self):
        self.contract_repository = ContractRepository()
        self.analysis_repository = AnalysisRepository()

    def analyze_contract(
        self,
        db: Session,
        contract_id: int
    ) -> None:
        # Placeholder for the contract analysis workflow.
        # Implement the analysis execution using the AI engine here.
        return None

    def save_analysis(
        self,
        db: Session,
        contract_id: int,
        result: AnalysisResult,
        model_name: str,
        processing_time: float
    ):
        version = self.contract_repository.get_next_analysis_version(
            db=db,
            contract_id=contract_id
        )

        analysis = ContractAnalysis(
            contract_id=contract_id,
            analysis_version=version,
            summary=result.summary,
            risk_score=result.risk_score,
            risk_level=result.risk,
            recommendations="\n".join(result.suggestions),
            model_name=model_name,
            confidence_score=result.confidence,
            processing_time_ms=int(processing_time),
        )

        return self.analysis_repository.create_analysis(
            db=db,
            analysis=analysis
        )
        
        
def aianalysisservice() -> AnalysisService:
    return AnalysisService()