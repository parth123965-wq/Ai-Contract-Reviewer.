from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from app.core.config import settings
load_dotenv()

class LLMService:
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model=settings.AI_MODEL_NAME)
    
    def generate(self,prompt: str):
        response = self.llm.invoke(prompt)
        return response.content