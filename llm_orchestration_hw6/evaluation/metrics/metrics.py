from typing import List, Dict
from sentence_transformers import SentenceTransformer, util

# Load a pre-trained sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_accuracy(ground_truth: List[Dict], responses: List[str]) -> float:
    """
    Calculates the accuracy of the responses compared to the ground truth using sentence similarity.
    """
    correct = 0
    similarity_threshold = 0.8  # Threshold for considering a response as correct

    for i, gt in enumerate(ground_truth):
        if i < len(responses):
            response = str(responses[i]).strip()
            gt_answers = [ans.strip() for ans in str(gt["ground_truth_answer"]).split("or")]
            
            response_embedding = model.encode(response, convert_to_tensor=True)
            gt_embeddings = model.encode(gt_answers, convert_to_tensor=True)
            
            # Calculate cosine similarity between the response and all ground truth answers
            cosine_scores = util.pytorch_cos_sim(response_embedding, gt_embeddings)
            
            # Check if any of the ground truth answers has a similarity score above the threshold
            if any(score > similarity_threshold for score in cosine_scores[0]):
                correct += 1

    return correct / len(ground_truth) if ground_truth else 0

def calculate_f1_score(ground_truth: List[Dict], responses: List[str]) -> float:
    """
    Calculates the F1 score of the responses compared to the ground truth using sentence similarity.
    """
    if not ground_truth or not responses:
        return 0.0

    true_positives = 0
    false_positives = 0
    false_negatives = 0
    similarity_threshold = 0.8

    for i, gt in enumerate(ground_truth):
        if i < len(responses):
            response = str(responses[i]).strip()
            gt_answers = [ans.strip() for ans in str(gt["ground_truth_answer"]).split("or")]

            response_embedding = model.encode(response, convert_to_tensor=True)
            gt_embeddings = model.encode(gt_answers, convert_to_tensor=True)
            
            cosine_scores = util.pytorch_cos_sim(response_embedding, gt_embeddings)

            if any(score > similarity_threshold for score in cosine_scores[0]):
                true_positives += 1
            else:
                false_negatives += 1
        else:
            false_negatives += 1 # Response is missing
            
    # This is a simplified calculation of F1 score, not a standard one.
    # We are considering each question as a binary classification task (correct/incorrect)
    # A more standard approach would be to calculate precision and recall on a token/word level.
    # For now, we will calculate precision and recall based on the number of correct/incorrect questions.
    
    # Let's consider every response that is not a true positive as a false positive for simplicity
    # This is not a perfect F1 score calculation but a step up from the dummy one.
    false_positives = len(responses) - true_positives
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return f1
