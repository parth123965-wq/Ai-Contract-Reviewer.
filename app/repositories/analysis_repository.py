from sqlalchemy.orm import Session

from app.models.contract import ContractAnalysis


class AnalysisRepository:

    def create_analysis(
        self,
        db: Session,
        analysis: ContractAnalysis
    ) -> ContractAnalysis:
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis