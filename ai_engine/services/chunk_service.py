from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkService:
    
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.CHUNK_SIZE,
            chunk_overlap = self.CHUNK_OVERLAP,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )
    
    def _validate_text(
        self,
        text: str
    ) -> None:
        if not text or not text.strip():
            raise ValueError("Text is empty.")
        
    def chunk_text(
        self,
        text: str
    ) -> list[str]:
        self._validate_text(text=text)
        chunks = self.splitter.split_text(text=text)
        return chunks