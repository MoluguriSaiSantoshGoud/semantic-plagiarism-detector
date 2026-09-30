from typing import List, Dict, Tuple
import numpy as np
import time
from app.services.embeddings import EmbeddingService
from app.services.similarity import SimilarityEngine
from app.services.explanation_agent import ExplanationAgent


class PlagiarismDetector:
    """Main plagiarism detection engine."""
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.similarity_engine = SimilarityEngine()
        self.explanation_agent = ExplanationAgent()
    
    def compare_documents(
        self,
        reference_chunks: List[Dict],
        submitted_chunks: List[Dict]
    ) -> Dict:
        """Compare two documents and return plagiarism analysis."""
        start_time = time.time()
        
        if not reference_chunks or not submitted_chunks:
            return {
                "error": "No chunks to compare",
                "overall_similarity": 0.0,
                "weighted_similarity": 0.0,
                "matches": [],
                "statistics": {}
            }
        
        # Extract chunk texts
        ref_texts = [chunk["text"] for chunk in reference_chunks]
        sub_texts = [chunk["text"] for chunk in submitted_chunks]
        
        # Calculate semantic similarity matrix
        semantic_matrix = self.embedding_service.calculate_similarity_matrix(ref_texts, sub_texts)
        
        # Find matches
        matches = self._find_matches(
            reference_chunks,
            submitted_chunks,
            semantic_matrix,
            ref_texts,
            sub_texts
        )
        
        # Calculate overall similarity
        overall_stats = self._calculate_overall_similarity(submitted_chunks, matches)
        
        processing_time = time.time() - start_time
        
        return {
            "overall_similarity": overall_stats["overall_similarity"],
            "weighted_similarity": overall_stats["weighted_similarity"],
            "matches": matches,
            "statistics": overall_stats,
            "processing_time": processing_time
        }
    
    def _find_matches(
        self,
        reference_chunks: List[Dict],
        submitted_chunks: List[Dict],
        semantic_matrix: np.ndarray,
        ref_texts: List[str],
        sub_texts: List[str]
    ) -> List[Dict]:
        """Find and classify matches between chunks."""
        matches = []
        threshold = 0.45  # Minimum similarity threshold
        
        for sub_idx, sub_chunk in enumerate(submitted_chunks):
            sub_text = sub_texts[sub_idx]
            best_match = None
            best_score = 0.0
            
            for ref_idx, ref_chunk in enumerate(reference_chunks):
                ref_text = ref_texts[ref_idx]
                
                # Get semantic score from matrix
                semantic_score = float(semantic_matrix[ref_idx, sub_idx])
                
                if semantic_score < threshold:
                    continue
                
                # Calculate other similarity scores
                other_scores = self.similarity_engine.calculate_all_similarities(ref_text, sub_text)
                other_scores["semantic_score"] = semantic_score
                
                # Calculate combined score
                combined_score = self.similarity_engine.calculate_combined_score(
                    semantic_score,
                    other_scores["lexical_score"],
                    other_scores["ngram_score"],
                    other_scores["exact_match_score"]
                )
                
                if combined_score > best_score:
                    best_score = combined_score
                    best_match = {
                        "reference_chunk_id": ref_idx,
                        "submitted_chunk_id": sub_idx,
                        "reference_chunk": ref_chunk,
                        "submitted_chunk": sub_chunk,
                        "semantic_score": semantic_score,
                        "lexical_score": other_scores["lexical_score"],
                        "ngram_score": other_scores["ngram_score"],
                        "exact_match_score": other_scores["exact_match_score"],
                        "combined_score": combined_score
                    }
            
            if best_match and best_match["combined_score"] >= threshold:
                # Classify the match
                classification = self.explanation_agent.classify_match(best_match)
                best_match["classification"] = classification
                
                # Generate explanation
                explanation = self.explanation_agent.generate_explanation(best_match)
                best_match["explanation"] = explanation
                
                matches.append(best_match)
        
        # Sort matches by combined score
        matches.sort(key=lambda x: x["combined_score"], reverse=True)
        
        return matches
    
    def _calculate_overall_similarity(
        self,
        submitted_chunks: List[Dict],
        matches: List[Dict]
    ) -> Dict:
        """Calculate overall document similarity statistics."""
        if not submitted_chunks:
            return {
                "overall_similarity": 0.0,
                "weighted_similarity": 0.0,
                "percentage_of_text_with_matches": 0.0,
                "total_submitted_chunks": 0,
                "matching_chunk_count": 0,
                "very_high_similarity_chunk_count": 0,
                "high_similarity_chunk_count": 0,
                "moderate_similarity_chunk_count": 0,
                "low_similarity_chunk_count": 0
            }
        
        total_words = sum(chunk["word_count"] for chunk in submitted_chunks)
        
        if total_words == 0:
            return {
                "overall_similarity": 0.0,
                "weighted_similarity": 0.0,
                "percentage_of_text_with_matches": 0.0,
                "total_submitted_chunks": len(submitted_chunks),
                "matching_chunk_count": 0,
                "very_high_similarity_chunk_count": 0,
                "high_similarity_chunk_count": 0,
                "moderate_similarity_chunk_count": 0,
                "low_similarity_chunk_count": 0
            }
        
        # Calculate weighted similarity
        weighted_sum = 0.0
        matched_words = 0
        
        # Track chunk counts by similarity level
        very_high = 0
        high = 0
        moderate = 0
        low = 0
        
        matched_chunk_indices = set()
        
        for match in matches:
            sub_idx = match["submitted_chunk_id"]
            sub_chunk = submitted_chunks[sub_idx]
            word_count = sub_chunk["word_count"]
            
            weighted_sum += match["combined_score"] * word_count
            matched_words += word_count
            matched_chunk_indices.add(sub_idx)
            
            # Classify by score
            score = match["combined_score"]
            if score >= 0.80:
                very_high += 1
            elif score >= 0.65:
                high += 1
            elif score >= 0.45:
                moderate += 1
            else:
                low += 1
        
        weighted_similarity = weighted_sum / total_words if total_words > 0 else 0.0
        percentage_with_matches = (matched_words / total_words) * 100 if total_words > 0 else 0.0
        
        return {
            "overall_similarity": weighted_similarity,
            "weighted_similarity": weighted_similarity,
            "percentage_of_text_with_matches": percentage_with_matches,
            "total_submitted_chunks": len(submitted_chunks),
            "matching_chunk_count": len(matched_chunk_indices),
            "very_high_similarity_chunk_count": very_high,
            "high_similarity_chunk_count": high,
            "moderate_similarity_chunk_count": moderate,
            "low_similarity_chunk_count": low
        }
    
    def get_similarity_label(self, score: float) -> str:
        """Get label for similarity score."""
        if score >= 0.80:
            return "Very high similarity"
        elif score >= 0.65:
            return "High similarity"
        elif score >= 0.45:
            return "Moderate similarity"
        else:
            return "Low similarity"
