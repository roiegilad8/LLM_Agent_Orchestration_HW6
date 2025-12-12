from typing import Dict, Any, Optional

from llm_orchestration_hw6.evaluation.techniques.base import BaseEvaluator

class FewShotEvaluator(BaseEvaluator):
    """
    Evaluator for the few-shot prompt engineering technique.
    """

    def evaluate(self, question: str, llm_client: Optional[Any] = None) -> Dict:
        """
        Evaluates a question using the few-shot prompt engineering technique.

        Args:
            question: The question to evaluate.
            llm_client: The LLM client to use for the evaluation.

        Returns:
            A dictionary containing the evaluation results.
        """
        prompt = f"""
Examples:
Q: What is 2+2?
A: 4

Q: What is capital of France?
A: Paris

Question: {question}
Answer:"""
        
        if llm_client:
            response = llm_client.query(prompt)
        else:
            response = ""

        return {
            "prompt": prompt,
            "response": response,
        }
