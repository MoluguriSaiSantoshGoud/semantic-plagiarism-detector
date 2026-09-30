from app.services.document_processor import DocumentProcessor
from app.services.embeddings import EmbeddingService
from app.services.similarity import SimilarityEngine
from app.services.plagiarism import PlagiarismDetector
from app.services.report_generator import ReportGenerator
from app.services.explanation_agent import ExplanationAgent

__all__ = [
    "DocumentProcessor",
    "EmbeddingService",
    "SimilarityEngine",
    "PlagiarismDetector",
    "ReportGenerator",
    "ExplanationAgent"
]
