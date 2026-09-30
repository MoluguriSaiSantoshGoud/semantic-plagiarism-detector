from typing import List, Tuple
import numpy as np
from collections import Counter
from app.config import settings

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class SimilarityEngine:
    """Hybrid similarity engine combining semantic, lexical, and n-gram similarities."""
    
    def __init__(self):
        self.semantic_weight = settings.semantic_weight
        self.lexical_weight = settings.lexical_weight
        self.ngram_weight = settings.ngram_weight
    
    def calculate_lexical_similarity(self, text_a: str, text_b: str) -> float:
        """Calculate TF-IDF based lexical similarity."""
        if not text_a or not text_b or not text_a.strip() or not text_b.strip():
            return 0.0
        
        if SKLEARN_AVAILABLE:
            try:
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                return float(similarity)
            except:
                return self._simple_word_overlap(text_a, text_b)
        else:
            return self._simple_word_overlap(text_a, text_b)
    
    def _simple_word_overlap(self, text_a: str, text_b: str) -> float:
        """Simple word overlap similarity as fallback."""
        words_a = set(text_a.lower().split())
        words_b = set(text_b.lower().split())
        
        if not words_a or not words_b:
            return 0.0
        
        intersection = len(words_a & words_b)
        union = len(words_a | words_b)
        
        return intersection / union if union > 0 else 0.0
    
    def calculate_ngram_similarity(self, text_a: str, text_b: str, n: int = 3) -> float:
        """Calculate n-gram overlap similarity using Jaccard index."""
        if not text_a or not text_b or not text_a.strip() or not text_b.strip():
            return 0.0
        
        def get_ngrams(text: str, n: int) -> set:
            words = text.lower().split()
            ngrams = set()
            for i in range(len(words) - n + 1):
                ngram = tuple(words[i:i+n])
                ngrams.add(ngram)
            return ngrams
        
        ngrams_a = get_ngrams(text_a, n)
        ngrams_b = get_ngrams(text_b, n)
        
        if not ngrams_a or not ngrams_b:
            return 0.0
        
        # Jaccard similarity
        intersection = len(ngrams_a & ngrams_b)
        union = len(ngrams_a | ngrams_b)
        
        return intersection / union if union > 0 else 0.0
    
    def calculate_exact_match_similarity(self, text_a: str, text_b: str) -> float:
        """Calculate exact phrase match similarity."""
        if not text_a or not text_b or not text_a.strip() or not text_b.strip():
            return 0.0
        
        # Normalize texts
        normalized_a = " ".join(text_a.lower().split())
        normalized_b = " ".join(text_b.lower().split())
        
        if normalized_a == normalized_b:
            return 1.0
        
        # Check for sentence-level exact matches
        sentences_a = [s.strip() for s in normalized_a.split('.') if s.strip()]
        sentences_b = [s.strip() for s in normalized_b.split('.') if s.strip()]
        
        if not sentences_a or not sentences_b:
            return 0.0
        
        matches = 0
        for sent_a in sentences_a:
            for sent_b in sentences_b:
                if sent_a == sent_b:
                    matches += 1
                    break
        
        return matches / max(len(sentences_a), len(sentences_b))
    
    def calculate_combined_score(
        self,
        semantic_score: float,
        lexical_score: float,
        ngram_score: float,
        exact_match_score: float
    ) -> float:
        """Calculate weighted combined similarity score."""
        combined = (
            self.semantic_weight * semantic_score +
            self.lexical_weight * lexical_score +
            self.ngram_weight * ngram_score
        )
        
        # Boost if exact match is high
        if exact_match_score > 0.8:
            combined = min(1.0, combined + (exact_match_score * 0.1))
        
        return max(0.0, min(1.0, combined))
    
    def calculate_all_similarities(self, text_a: str, text_b: str) -> dict:
        """Calculate all similarity metrics between two texts."""
        return {
            "semantic_score": 0.0,  # Will be calculated by embedding service
            "lexical_score": self.calculate_lexical_similarity(text_a, text_b),
            "ngram_score": self.calculate_ngram_similarity(text_a, text_b),
            "exact_match_score": self.calculate_exact_match_similarity(text_a, text_b)
        }
