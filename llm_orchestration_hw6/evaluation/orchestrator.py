import os
import re
import concurrent.futures

from llm_orchestration_hw6.data.loader import load_dataset
from llm_orchestration_hw6.evaluation.metrics import calculate_accuracy, calculate_f1_score # Added calculate_f1_score
from llm_orchestration_hw6.evaluation.techniques.baseline import BaselineEvaluator
from llm_orchestration_hw6.evaluation.techniques.few_shot import FewShotEvaluator
from llm_orchestration_hw6.evaluation.techniques.cot import CoTEvaluator
from llm_orchestration_hw6.evaluation.techniques.react import ReActEvaluator
from llm_orchestration_hw6.llms.providers.openai_client import OpenAIClient
from llm_orchestration_hw6.llms.providers.gemini_client import GeminiClient


def clean_response(response: str) -> str:
    # remove the question number and dot from the beginning of the string
    response = re.sub(r"^\d+\.\s*", "", response, flags=re.MULTILINE).strip()
    # remove "Answer:" prefix, case-insensitive
    response = re.sub(r"^(answer:)\s*", "", response, flags=re.IGNORECASE | re.MULTILINE).strip()
    return response

def _analyze_single_llm_technique(llm_name, technique, questions, results_path):
    responses = []
    # response_file_path is different for perplexity
    if llm_name == "peplexity":
        if technique == "few_shot":
            response_file_path = os.path.join(results_path, llm_name, f"{technique}_prompts_perplexity.txt")
        else:
            response_file_path = os.path.join(results_path, llm_name, f"{technique}_prompts_perplexity.txt")
    elif llm_name == "Grok":
        response_file_path = os.path.join(results_path, llm_name, f"{technique}_prompts_grok.txt")
    else:
        response_file_path = os.path.join(results_path, llm_name, f"{technique}_prompts_{llm_name}.txt")

    
    if os.path.exists(response_file_path):
        with open(response_file_path, "r") as f:
            lines = f.read().splitlines()
            if technique == "cot" and llm_name == "GPT":
                # Special parsing for the single-line format in cot_prompts_GPT.txt
                full_text = " ".join(lines)
                # This regex will find all occurrences of a number followed by a dot and then the answer
                matches = re.findall(r'\d+\.\s*([^\d]+)', full_text)
                responses = [match.strip() for match in matches]
            elif technique == "react":
                for line in lines:
                    if line.lower().startswith("answer:"):
                        responses.append(line[len("answer:"):].strip())
                    elif re.match(r"A\d+:", line):
                        responses.append(line.split(":", 1)[1].strip())
            else:
                if lines and "Answers to 100 Questions" in lines[0]:
                    lines = lines[1:]
                responses = [clean_response(line) for line in lines if line.strip() != ""]
        
        accuracy = calculate_accuracy(questions, responses)
        f1_score = calculate_f1_score(questions, responses)
        return {
            "llm": llm_name,
            "technique": technique,
            "accuracy": accuracy,
            "f1_score": f1_score,
        }
    else:
        return {
            "llm": llm_name,
            "technique": technique,
            "accuracy": "Not found",
            "f1_score": "Not found",
        }

def analyze(dataset_path: str, results_path: str, llms: str, techniques: str) -> dict:
    """
    Analyze the manual evaluation results.
    """
    results = {}
    questions = load_dataset(os.path.abspath(dataset_path))

    llm_list = llms.split(',')
    technique_list = techniques.split(',')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for llm_name in llm_list:
            results[llm_name] = {}
            for technique in technique_list:
                futures.append(executor.submit(_analyze_single_llm_technique, llm_name, technique, questions, results_path))
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results[result["llm"]][result["technique"]] = {
                "accuracy": result["accuracy"],
                "f1_score": result["f1_score"],
            }
            accuracy_str = f"{result['accuracy']:.2f}" if isinstance(result['accuracy'], float) else str(result['accuracy'])
            f1_score_str = f"{result['f1_score']:.2f}" if isinstance(result['f1_score'], float) else str(result['f1_score'])
            print(f"  - {result['llm']} - {result['technique']}: Accuracy={accuracy_str}, F1-score={f1_score_str}")

    return results

def _generate_single_technique_prompts(technique, questions, prompts_dir, evaluator_map):
    print(f"  - Generating prompts for {technique}...")
    evaluator = evaluator_map.get(technique)
    if not evaluator:
        print(f"    - Technique '{technique}' not implemented yet.")
        return

    prompt_file_path = os.path.join(prompts_dir, f"{technique}_prompts.txt")
    with open(prompt_file_path, "w") as f:
        for i, question in enumerate(questions):
            # We pass a dummy llm_client since it's not used in this scenario
            result = evaluator.evaluate(question["question"], None)
            f.write(f"----- Prompt for Question {i+1} -----\n")
            f.write(result['prompt'])
            f.write("\n\n")

def generate_prompts(dataset_path: str, results_path: str, techniques: str):
    """
    Generate prompts for manual evaluation.
    """
    print(f"Generating prompts with the following settings:")
    print(f"  - Dataset: {dataset_path}")
    print(f"  - Results path: {results_path}")
    print(f"  - Techniques: {techniques}")

    # 1. Load the dataset
    print("\nLoading dataset...")
    questions = load_dataset(dataset_path)
    print(f"Loaded {len(questions)} questions.")

    # 2. Create prompts directory
    prompts_dir = os.path.join(results_path, "prompts")
    os.makedirs(prompts_dir, exist_ok=True)
    print(f"Prompts will be saved in: {prompts_dir}")

    # 3. Generate prompts for each technique
    print("\nGenerating prompts for each technique...")
    technique_list = techniques.split(',')
    evaluator_map = {
        "baseline": BaselineEvaluator(),
        "few_shot": FewShotEvaluator(),
        "cot": CoTEvaluator(),
        "react": ReActEvaluator(),
    }

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(_generate_single_technique_prompts, technique, questions, prompts_dir, evaluator_map) for technique in technique_list]
        for future in concurrent.futures.as_completed(futures):
            future.result() # Wait for all futures to complete

    print("\nPrompt generation complete.")