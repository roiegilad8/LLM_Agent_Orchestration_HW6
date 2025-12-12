from typing import Dict, Any, Optional

from llm_orchestration_hw6.evaluation.techniques.base import BaseEvaluator

class BaselineEvaluator(BaseEvaluator):
    """
    Evaluator for the baseline prompt engineering technique.
    """

    def evaluate(self, question: str, llm_client: Optional[Any] = None) -> Dict:
        """
        Evaluates a question using the baseline prompt engineering technique.

        Args:
            question: The question to evaluate.
            llm_client: The LLM client to use for the evaluation.

        Returns:
            A dictionary containing the evaluation results.
        """
        prompt = f"Question: {question}\nAnswer:"
        
        if llm_client:
            response = llm_client.query(prompt)
        else:
            response = ""

        return {
            "prompt": prompt,
            "response": response,
        }

