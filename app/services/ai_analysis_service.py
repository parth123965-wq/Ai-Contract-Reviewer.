from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.contract import ContractAnalysis, ContractStatus
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.contract_repository import ContractRepository

from ai_engine.schemas.analysis_result import AnalysisResult
from ai_engine.graph.graph import ContractGraph


class AnalysisService:

    def __init__(self):
        self.contract_repository = ContractRepository()
        self.analysis_repository = AnalysisRepository()

    def analyze_contract(
        self,
        contract_id: int
    ) -> None:
        db = SessionLocal()
        contract = None
        try:
            contract = self.contract_repository.get_contract_by_id(
                db=db,
                contract_id=contract_id
            )
            if contract is None or contract.is_deleted:
                return

            contract.status = ContractStatus.PROCESSING
            db.commit()
            db.refresh(contract)

            version = self.contract_repository.get_next_analysis_version(
                db=db,
                contract_id=contract.id
            )

            graph = ContractGraph()
            compiled_graph = graph.compile_graph()
            compiled_graph.invoke(
                input={
                    "contract_id": contract.id,
                    "user_id": contract.user_id,
                    "file_path": contract.file_path,
                    "db": db,
                    "analysis_version": version,
                    "status": contract.status,
                    "error": None,
                    "extracted_text": "",
                    "chunks": [],
                    "embeddings": [],
                    "retrieved_chunks": [],
                    "summary": "",
                    "risk_score": 0,
                    "suggestions": [],
                    "query_embedding": [],
                }
            )

            contract.status = ContractStatus.COMPLETED
            db.commit()
        except Exception as exc:
            db.rollback()
            if contract is not None:
                try:
                    contract.status = ContractStatus.FAILED
                    contract.last_error = str(exc)
                    db.add(contract)
                    db.commit()
                except Exception:
                    pass
        finally:
            db.close()

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