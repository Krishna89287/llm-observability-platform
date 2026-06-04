"""
LLM Response Quality Scorer
Automated quality evaluation for production LLM responses
"""
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class QualityScorer:
    """
    Automated quality scoring for LLM responses.
    Evaluates coherence, completeness, and safety.
    """

    def score_coherence(self, response: str) -> float:
        """Score response coherence based on sentence structure."""
        sentences = [s.strip() for s in response.split('.') if s.strip()]
        if not sentences:
            return 0.0
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
        if 5 <= avg_length <= 25:
            return 1.0
        elif 3 <= avg_length <= 35:
            return 0.7
        return 0.4

    def score_completeness(self, question: str, response: str) -> float:
        """Score how completely the response answers the question."""
        q_words = set(question.lower().split())
        r_words = set(response.lower().split())
        coverage = len(q_words & r_words) / max(len(q_words), 1)
        length_bonus = min(len(response.split()) / 50, 0.3)
        return min(coverage + length_bonus, 1.0)

    def score_safety(self, response: str) -> float:
        """Basic safety check for harmful content."""
        harmful_patterns = ["harm", "kill", "illegal", "dangerous"]
        response_lower = response.lower()
        if any(p in response_lower for p in harmful_patterns):
            return 0.0
        return 1.0

    def score_response(self, question: str, response: str) -> Dict:
        """Full quality assessment."""
        coherence = self.score_coherence(response)
        completeness = self.score_completeness(question, response)
        safety = self.score_safety(response)
        overall = (coherence * 0.3 + completeness * 0.5 + safety * 0.2)
        return {
            "overall": round(overall, 2),
            "coherence": round(coherence, 2),
            "completeness": round(completeness, 2),
            "safety": round(safety, 2),
            "passed": overall >= 0.7
        }


if __name__ == "__main__":
    scorer = QualityScorer()
    result = scorer.score_response(
        question="What is vLLM and why is it fast?",
        response="vLLM is a fast LLM inference engine that uses PagedAttention to achieve high throughput and low latency. It can serve multiple requests efficiently."
    )
    print(f"Quality scores: {result}")
