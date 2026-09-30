from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Comparison(Base):
    __tablename__ = "comparisons"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reference_document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    submitted_document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    overall_similarity = Column(Float, nullable=False)
    weighted_similarity = Column(Float, nullable=False)
    processing_time = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    matches = relationship("Match", back_populates="comparison", cascade="all, delete-orphan")


class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    comparison_id = Column(Integer, ForeignKey("comparisons.id"), nullable=False)
    reference_chunk_id = Column(Integer, ForeignKey("document_chunks.id"), nullable=False)
    submitted_chunk_id = Column(Integer, ForeignKey("document_chunks.id"), nullable=False)
    semantic_score = Column(Float, nullable=False)
    lexical_score = Column(Float, nullable=False)
    ngram_score = Column(Float, nullable=False)
    exact_match_score = Column(Float, nullable=False)
    combined_score = Column(Float, nullable=False)
    classification = Column(String(50), nullable=False)
    explanation = Column(Text, nullable=False)
    
    comparison = relationship("Comparison", back_populates="matches")
