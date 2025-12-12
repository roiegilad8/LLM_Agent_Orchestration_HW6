from llm_orchestration_hw6.evaluation.techniques.baseline import BaselineEvaluator
from llm_orchestration_hw6.evaluation.techniques.few_shot import FewShotEvaluator
from llm_orchestration_hw6.evaluation.techniques.cot import CoTEvaluator
from llm_orchestration_hw6.evaluation.techniques.react import ReActEvaluator

def test_baseline_evaluator():
    evaluator = BaselineEvaluator()
    result = evaluator.evaluate("What is 2+2?")
    assert "Question: What is 2+2?" in result["prompt"]
    assert "Answer:" in result["prompt"]

def test_few_shot_evaluator():
    evaluator = FewShotEvaluator()
    result = evaluator.evaluate("What is 10 % 3 (modulo)?")
    assert "Examples:" in result["prompt"]
    assert "Q: What is 2+2?" in result["prompt"]
    assert "A: 4" in result["prompt"]
    assert "Question: What is 10 % 3 (modulo)?" in result["prompt"]
    assert "Answer:" in result["prompt"]

def test_cot_evaluator():
    evaluator = CoTEvaluator()
    result = evaluator.evaluate("What is 10 % 3 (modulo)?")
    assert "Let's think step by step." in result["prompt"]
    assert "Question: What is 10 % 3 (modulo)?" in result["prompt"]
    assert "Step 1: ..." in result["prompt"]
    assert "Answer:" in result["prompt"]

def test_react_evaluator():
    evaluator = ReActEvaluator()
    result = evaluator.evaluate("What is 10 % 3 (modulo)?")
    assert "You can:" in result["prompt"]
    assert "- Think: reason about the problem" in result["prompt"]
    assert "- Act: perform an action" in result["prompt"]
    assert "- Observe: see the result" in result["prompt"]
    assert "Question: What is 10 % 3 (modulo)?" in result["prompt"]
    assert "Think: ..." in result["prompt"]
    assert "Act: ..." in result["prompt"]
    assert "Observe: ..." in result["prompt"]
    assert "Answer:" in result["prompt"]
