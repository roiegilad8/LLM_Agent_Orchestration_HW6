from typing import Dict, Any, Optional

from llm_orchestration_hw6.evaluation.techniques.base import BaseEvaluator

class CoTEvaluator(BaseEvaluator):
    """
    Evaluator for the Chain-of-Thought (CoT) prompt engineering technique.
    """

    def evaluate(self, question: str, llm_client: Optional[Any] = None) -> Dict:
        """
        Evaluates a question using the Chain-of-Thought (CoT) prompt engineering technique.

        Args:
            question: The question to evaluate.
            llm_client: The LLM client to use for the evaluation.

        Returns:
            A dictionary containing the evaluation results.
        """
        prompt = f"""
Let's think step by step.
Question: {question}
Step 1: ...
Step 2: ...
Answer:"""
        
        if llm_client:
            response = llm_client.query(prompt)
        else:
            response = ""

        return {
            "prompt": prompt,
            "response": response,
        }
