# Extensibility Guide

This document outlines how to extend the LLM Agent Orchestration Framework by adding new prompt engineering techniques, LLM providers, and evaluation metrics.

## 1. Adding a New Prompt Engineering Technique

To add a new prompt engineering technique, you need to create a new evaluator class that inherits from `BaseEvaluator` and implements the `evaluate` method. For example, if you want to add a "SuperPrompt" technique, you would create a file like `super_prompt.py` in `llm_orchestration_hw6/evaluation/techniques/` with the following structure:

```python
# llm_orchestration_hw6/evaluation/techniques/super_prompt.py
from typing import Dict, Any, Optional

from llm_orchestration_hw6.evaluation.techniques.base import BaseEvaluator

class SuperPromptEvaluator(BaseEvaluator):
    def evaluate(self, question: str, llm_client: Optional[Any] = None) -> Dict:
        # Implement your SuperPrompt logic here
        pass
```

Then, you would add a new `elif` condition in the `generate_prompts` function within `orchestrator.py` to instantiate `SuperPromptEvaluator` when the "super_prompt" technique is requested.

## 2. Adding a New LLM Provider

To add support for a new LLM provider (e.g., Google Gemini, Anthropic Claude), you need to create a new client class that implements a `query` method similar to `OpenAIClient`. For example, if you want to add a "GoogleGeminiClient", you would create a file like `gemini_client.py` in `llm_orchestration_hw6/llms/providers/` with the following structure:

```python
import os
# import your gemini library here (e.g., google.generativeai as genai)

class GoogleGeminiClient:
    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.environ.get("GEMINI_API_KEY")
        if api_key is None:
            raise ValueError("Google Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
        
        self.api_key = api_key
        # Initialize your Google Gemini client here
        # self.model = genai.GenerativeModel('gemini-pro')

    def query(self, prompt: str) -> str:
        # Implement your LLM API call here
        # response = self.model.generate_content(prompt)
        # return response.text
        return "This is a dummy response from the Google Gemini API."
```

## 3. Adding a New Evaluation Metric

To add a new evaluation metric, you need to extend the `metrics.py` module. For example, if you want to add an "F1 Score" metric, you would:

1.  **Add a new function** to `llm_orchestration_hw6/evaluation/metrics/metrics.py` (e.g., `calculate_f1_score`) that takes the ground truth answers and LLM responses as input and returns the calculated metric.

    ```python
    # llm_orchestration_hw6/evaluation/metrics/metrics.py
    # ...
    def calculate_f1_score(ground_truth: List[Dict], responses: List[str]) -> float:
        # Implement your F1 score calculation here
        return 0.75 # Dummy value
    ```

2.  **Update `llm_orchestration_hw6/evaluation/orchestrator.py`:**
    *   Import your new metric function.
    *   Modify the `analyze` function to calculate and include your new metric in the results dictionary.
    *   Update the `ANALYSIS_REPORT.md` generation to include the new metric.

This modular design allows for flexible expansion of the framework's capabilities without altering existing, tested components.