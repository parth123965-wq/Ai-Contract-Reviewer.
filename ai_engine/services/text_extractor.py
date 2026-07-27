from pathlib import Path
import fitz
from typing import Any 

class TextExtractor:
    
    def _validate_file(
        self,
        file_path: str
    ):
        file_exists = Path(file_path)
        if not file_exists.exists():
            raise FileNotFoundError("File is not found.")
        
    def _open_pdf(
        self,
        file_path: str
    ):
        pdf_path = Path(file_path)
        doc = fitz.open(pdf_path)
        return doc
    
    def _extract_text(
        self,
        doc: Any
    ) -> list[str]:
        text_list = []
        for page_number,page in enumerate(doc,start=1):
            text = page.get_text()
            text_list.append(text)
        return text_list
    
    def _combine_text(
        self,
        text_list: list
    ) -> str:
        return " ".join(text_list)
    
    def _text_process(
        self,
        text: str
    ):
        if not text or not text.strip():
            raise ValueError("No Meaningful text found.")
    
    def extract_text(
        self,
        file_path: str
    ) -> str:
        self._validate_file(file_path=file_path)
        page = self._open_pdf(file_path=file_path)
        text_list = self._extract_text(doc=page)
        single_string = self._combine_text(text_list=text_list)
        self._text_process(text=single_string)
        return single_string
        