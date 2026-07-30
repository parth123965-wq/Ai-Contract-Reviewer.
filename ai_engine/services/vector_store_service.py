from app.core.config import settings
import chromadb

class VectorStoreService:
    
    
    def __init__(self):
        self.vector_store = chromadb.PersistentClient()
        
    def store_embeddings(
        self,
        contract_id: int,
        user_id: int,
        chunks: list[str],
        embeddings: list[list[float]]
    ) -> None:
        pass
    
    def search(
        self,
        query_embedding: list[float],
        contract_id: int,
        user_id: int,
        top_k: int = 5
    ) -> list[str]:
        pass
    
    