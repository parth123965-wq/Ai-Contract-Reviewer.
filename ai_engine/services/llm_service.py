import json
import os
from dotenv import load_dotenv
from app.core.config import settings
load_dotenv()

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

class LLMService:
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.model_name = settings.AI_MODEL_NAME
        self.use_stub = False
        if self.api_key and ChatGoogleGenerativeAI is not None:
            self.llm = ChatGoogleGenerativeAI(
                model=self.model_name,
                api_key=self.api_key
            )
        else:
            self.llm = None
            self.use_stub = True
    
    def generate(self,prompt: str):
        if self.use_stub:
            return json.dumps({
                "summary": "Stub summary due to missing API key.",
                "risk_score": 0,
                "risk": "LOW",
                "suggestions": ["AI model is unavailable, using stub analysis."],
                "error": None,
                "prompt": prompt,
                "llm_response": "",
                "confidence": 0.0
            })

        response = self.llm.invoke(prompt)
        return response.content