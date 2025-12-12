import typer
from typing_extensions import Annotated
import os
import re

from llm_orchestration_hw6.data.loader import load_dataset
from llm_orchestration_hw6.evaluation.metrics import calculate_accuracy

app = typer.Typer(help="LLM Agent Orchestration evaluation orchestrator.")

def clean_response(response: str) -> str:
    # remove the question number and dot from the beginning of the string
    return re.sub(r"^\d+\.\s*", "", response).strip()

@app.command()
def analyze_results(
    dataset_path: Annotated[str, typer.Option(help="Path to the ground truth dataset.")] = "ground_truth_dataset.csv",
    results_path: Annotated[str, typer.Option(help="Path to the evaluation results.")] = "results",
    llms: Annotated[str, typer.Option(help="Comma-separated list of LLMs to analyze.")] = "GPT,Grok,peplexity",
    techniques: Annotated[str, typer.Option(help="Comma-separated list of techniques to analyze.")] = "baseline,few_shot,cot,react",
):
    """
    Analyze the manual evaluation results.
    """
    print(f"Analyzing results with the following settings:")
    print(f"  - Dataset: {dataset_path}")
    print(f"  - Results path: {results_path}")
    print(f"  - LLMs: {llms}")
    print(f"  - Techniques: {techniques}")

    # 1. Load the dataset
    print("\nLoading dataset...")
    questions = load_dataset(dataset_path)
    print(f"Loaded {len(questions)} questions.")

    # 2. Analyze the results for each LLM and each technique
    print("\nAnalyzing results...")
    results = {}
    for llm in llms.split(','):
        results[llm] = {}
        for technique in techniques.split(','):
            responses = []
            # response_file_path is different for perplexity
            if llm == "peplexity":
                if technique == "few_shot":
                    response_file_path = os.path.join(results_path, llm, f"{technique}_prompts_preplexity.txt")
                else:
                    response_file_path = os.path.join(results_path, llm, f"{technique}_prompts_perplexity.txt")
            elif llm == "Grok":
                response_file_path = os.path.join(results_path, llm, f"{technique}_prompts_grok.txt")
            else:
                response_file_path = os.path.join(results_path, llm, f"{technique}_prompts_{llm}.txt")

            
            if os.path.exists(response_file_path):
                with open(response_file_path, "r") as f:
                    # Skip the first line which is a header
                    lines = f.read().splitlines()
                    if lines and "Answers to 100 Questions" in lines[0]:
                        lines = lines[1:]
                    responses = [clean_response(line) for line in lines if line.strip() != ""]
                
                accuracy = calculate_accuracy(questions, responses)
                results[llm][technique] = accuracy
                print(f"  - {llm} - {technique}: {accuracy:.2f}")
            else:
                print(f"  - {llm} - {technique}: Not found")

    # 3. Generate analysis report
    print("\nGenerating analysis report...")
    report_path = os.path.join(results_path, "ANALYSIS_REPORT.md")
    with open(report_path, "w") as f:
        f.write("# Analysis Report\n\n")
        f.write("## Accuracy by LLM and Technique\n\n")
        f.write("| LLM | Baseline | Few-shot | CoT | ReAct |\n")
        f.write("|---|---|---|---|---|\n")
        for llm in results:
            f.write(f"| {llm} |")
            for technique in techniques.split(','):
                if technique in results[llm]:
                    f.write(f" {results[llm][technique]:.2f} |")
                else:
                    f.write(" N/A |")
            f.write("\n")

    print(f"\nAnalysis report generated at: {report_path}")


if __name__ == "__main__":
    app()
