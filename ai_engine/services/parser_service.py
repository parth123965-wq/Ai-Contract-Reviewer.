import re
from ai_engine.schemas.analysis_result import AnalysisResult

class ParserService:
    
    def process_json(self, jsons: str) -> AnalysisResult:
        try:
            cleaned = jsons.strip()
            if cleaned.startswith("```"):
                cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
                cleaned = re.sub(r"\s*```$", "", cleaned)
            data = AnalysisResult.model_validate_json(json_data=cleaned)
            return data
        except Exception as exc:
            raise ValueError("Invalid LLM response format") from exc