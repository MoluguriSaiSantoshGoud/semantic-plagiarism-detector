from typing import Dict


class ExplanationAgent:
    """Generate explanations for plagiarism matches."""
    
    def generate_explanation(self, match_data: Dict) -> str:
        """Generate a concise explanation for a match."""
        semantic_score = match_data.get("semantic_score", 0)
        lexical_score = match_data.get("lexical_score", 0)
        ngram_score = match_data.get("ngram_score", 0)
        exact_match_score = match_data.get("exact_match_score", 0)
        classification = match_data.get("classification", "unknown")
        
        if classification == "Exact copy":
            return "The submitted section is identical to the reference section. This indicates direct copying without any modifications."
        
        elif classification == "Near-exact copy":
            return "The submitted section is nearly identical to the reference with only minor changes such as punctuation or capitalization. This suggests light editing of copied content."
        
        elif classification == "Likely paraphrase":
            return f"The submitted section discusses the same concept as the reference but uses different wording. Semantic similarity is high ({semantic_score:.2f}) while lexical overlap is moderate ({lexical_score:.2f}), which is consistent with paraphrasing."
        
        elif classification == "Conceptually similar":
            return "The submitted section shares conceptual similarities with the reference but differs significantly in wording and structure. This may indicate shared ideas or common academic phrasing."
        
        elif classification == "Weak similarity":
            return "The submitted section shows some similarity to the reference, but the overlap is minimal. This could be due to common terminology or coincidental word choices."
        
        else:
            return f"This section was flagged based on a combined similarity score. Semantic: {semantic_score:.2f}, Lexical: {lexical_score:.2f}, N-gram: {ngram_score:.2f}. Human review is recommended."
    
    def classify_match(self, scores: Dict) -> str:
        """Classify a match based on similarity scores."""
        semantic = scores.get("semantic_score", 0)
        lexical = scores.get("lexical_score", 0)
        ngram = scores.get("ngram_score", 0)
        exact = scores.get("exact_match_score", 0)
        
        # Exact copy
        if exact > 0.95 or (lexical > 0.95 and semantic > 0.95):
            return "Exact copy"
        
        # Near-exact copy
        if exact > 0.8 or (lexical > 0.85 and semantic > 0.85):
            return "Near-exact copy"
        
        # Likely paraphrase
        if semantic > 0.75 and lexical < 0.6:
            return "Likely paraphrase"
        
        # High lexical with moderate semantic
        if lexical > 0.7 and semantic > 0.6:
            return "Likely paraphrase"
        
        # Conceptually similar
        if semantic > 0.5 and lexical < 0.4:
            return "Conceptually similar"
        
        # Weak similarity
        if semantic > 0.3 or lexical > 0.3:
            return "Weak similarity"
        
        return "Unrelated"
