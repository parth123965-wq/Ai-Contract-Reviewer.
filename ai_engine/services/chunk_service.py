from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkService:
    
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200,
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
        chunk = self.splitter.split_text(text=text)
        return chunk