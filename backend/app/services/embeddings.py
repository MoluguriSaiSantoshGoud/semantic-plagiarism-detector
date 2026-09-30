from typing import List
import numpy as np
from collections import Counter

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class EmbeddingService:
    """Service for generating text embeddings using Sentence Transformers."""
    
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._model is None and SENTENCE_TRANSFORMERS_AVAILABLE:
            self._model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts."""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            return np.zeros((len(texts), 384))
        return self._model.encode(texts, show_progress_bar=False)
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for a single text."""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            return np.zeros(384)
        return self._model.encode(text, show_progress_bar=False)
    
    def calculate_similarity_matrix(self, chunks_a: List[str], chunks_b: List[str]) -> np.ndarray:
        """Calculate similarity matrix between two sets of chunks."""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            # Use simple word overlap as fallback
            return self._calculate_word_overlap_matrix(chunks_a, chunks_b)
        
        embeddings_a = self.get_embeddings(chunks_a)
        embeddings_b = self.get_embeddings(chunks_b)
        
        if len(embeddings_a) == 0 or len(embeddings_b) == 0:
            return np.array([])
        
        # Cosine similarity matrix
        similarity_matrix = np.dot(embeddings_a, embeddings_b.T)
        
        return similarity_matrix
    
    def _calculate_word_overlap_matrix(self, chunks_a: List[str], chunks_b: List[str]) -> np.ndarray:
        """Calculate simple word overlap similarity matrix as fallback."""
        matrix = np.zeros((len(chunks_a), len(chunks_b)))
        
        for i, text_a in enumerate(chunks_a):
            words_a = set(text_a.lower().split())
            for j, text_b in enumerate(chunks_b):
                words_b = set(text_b.lower().split())
                
                if not words_a or not words_b:
                    matrix[i, j] = 0.0
                else:
                    intersection = len(words_a & words_b)
                    union = len(words_a | words_b)
                    matrix[i, j] = intersection / union if union > 0 else 0.0
        
        return matrix
