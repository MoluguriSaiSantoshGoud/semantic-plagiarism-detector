from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DocumentChunkResponse(BaseModel):
    id: int
    chunk_index: int
    paragraph_index: int
    page_number: int
    text: str
    word_count: int
    
    class Config:
        from_attributes = True


class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    extracted_text: str
    page_count: int
    word_count: int
    uploaded_at: datetime
    chunks: List[DocumentChunkResponse] = []
    
    class Config:
        from_attributes = True
