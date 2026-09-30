from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MatchResponse(BaseModel):
    id: int
    reference_chunk_id: int
    submitted_chunk_id: int
    semantic_score: float
    lexical_score: float
    ngram_score: float
    exact_match_score: float
    combined_score: float
    classification: str
    explanation: str
    
    class Config:
        from_attributes = True


class ComparisonCreate(BaseModel):
    reference_text: str
    submitted_text: str
    reference_filename: Optional[str] = "reference.txt"
    submitted_filename: Optional[str] = "submitted.txt"


class ComparisonResponse(BaseModel):
    id: int
    overall_similarity: float
    weighted_similarity: float
    processing_time: float
    created_at: datetime
    matches: List[MatchResponse] = []
    
    class Config:
        from_attributes = True


class ComparisonDetailedResponse(BaseModel):
    id: int
    overall_similarity: float
    weighted_similarity: float
    processing_time: float
    created_at: datetime
    reference_document: dict
    submitted_document: dict
    matches: List[MatchResponse]
    statistics: dict
    
    class Config:
        from_attributes = True
