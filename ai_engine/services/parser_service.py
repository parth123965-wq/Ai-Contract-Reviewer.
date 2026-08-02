from ai_engine.schemas.analysis_result import AnalysisResult

class ParserService:
    
    def process_json(self,jsons: str) -> AnalysisResult:
        try:
            data = AnalysisResult.model_validate_json(json_data=jsons)
            return data
        except Exception as exc:
            raise ValueError("Invalid LLM response format") from exc