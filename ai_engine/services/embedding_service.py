from sentence_transformers import SentenceTransformer
from app.core.config import settings

class EmbeddingService:
    
    def __init__(self):
        self.model = SentenceTransformer(settings.MODEL_NAME)
        
    def _validate_chunks(
        self,
        chunks: list[str]
    ) -> None:
        if any(
            not isinstance(chunk, str) or not chunk.strip()
            for chunk in chunks
        ):
            raise ValueError("All chunks must contain valid text.")
        cleaned = [item for item in chunks if isinstance(item,str) and item.strip()]
        if not cleaned:
            raise ValueError("Chunk is not contain valid text.")        
        
    def create_embeddings(
        self,
        chunks: list[str]
    ) -> list[list[float]]:
        self._validate_chunks(chunks=chunks)
        try:
            embeddings = self.model.encode(inputs=chunks)
            return embeddings.tolist()
        except Exception as exc:
            raise RuntimeError("Fail to generate embeddings") from exc