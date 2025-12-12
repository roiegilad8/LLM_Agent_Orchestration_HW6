from typing import Dict, Any, Optional

from llm_orchestration_hw6.evaluation.techniques.base import BaseEvaluator

class ReActEvaluator(BaseEvaluator):
    """
    Evaluator for the ReAct prompt engineering technique.
    """

    def evaluate(self, question: str, llm_client: Optional[Any] = None) -> Dict:
        """
        Evaluates a question using the ReAct prompt engineering technique.

        Args:
            question: The question to evaluate.
            llm_client: The LLM client to use for the evaluation.

        Returns:
            A dictionary containing the evaluation results.
        """
        prompt = f"""
You can:
- Think: reason about the problem
- Act: perform an action
- Observe: see the result

Question: {question}

Think: ...
Act: ...
Observe: ...
Answer:"""
        
        if llm_client:
            response = llm_client.query(prompt)
        else:
            response = ""

        return {
            "prompt": prompt,
            "response": response,
        }
