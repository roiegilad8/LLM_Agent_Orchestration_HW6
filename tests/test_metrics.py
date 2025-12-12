from llm_orchestration_hw6.evaluation.metrics import calculate_accuracy

def test_calculate_accuracy():
    ground_truth = [
        {"ground_truth_answer": "4"},
        {"ground_truth_answer": "Paris"},
        {"ground_truth_answer": "56"},
    ]
    responses = ["4", "paris", "55"]

    accuracy = calculate_accuracy(ground_truth, responses)

    # The first two should be correct, the third one is incorrect
    assert accuracy == 2 / 3
