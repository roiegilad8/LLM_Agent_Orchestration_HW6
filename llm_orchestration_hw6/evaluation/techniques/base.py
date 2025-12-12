from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseEvaluator(ABC):
    """
    Abstract base class for all evaluators.
    """

    @abstractmethod
    def evaluate(self, question: str, llm_client: Optional[Any] = None) -> Dict:
        """
        Evaluates a question using a specific prompt engineering technique.

        Args:
            question: The question to evaluate.
            llm_client: The LLM client to use for the evaluation.

        Returns:
            A dictionary containing the evaluation results.
        """
        pass
