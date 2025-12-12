from typing import List, Dict

def calculate_accuracy(ground_truth: List[Dict], responses: List[str]) -> float:
    """
    Calculates the accuracy of the responses compared to the ground truth.

    Args:
        ground_truth: A list of dictionaries, where each dictionary represents a question and its ground truth answer.
        responses: A list of strings, where each string is the response from the LLM.

    Returns:
        The accuracy of the responses, as a float between 0 and 1.
    """
    correct = 0
    for i, gt in enumerate(ground_truth):
        if i < len(responses):
            response = str(responses[i]).strip().lower()
            gt_answers = [ans.strip().lower() for ans in str(gt["ground_truth_answer"]).split("or")]
            
            for gt_answer in gt_answers:
                if gt_answer in response:
                    correct += 1
                    break

    return correct / len(ground_truth)
