import typer
from typing_extensions import Annotated
import os
import logging.config
import yaml

# Load logging configuration from file
config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'logging.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)
logging.config.dictConfig(config)

from llm_orchestration_hw6.__version__ import __version__
from llm_orchestration_hw6.evaluation.orchestrator import analyze, generate_prompts
from llm_orchestration_hw6.evaluation.plot_results import plot_results_function

app = typer.Typer(help="LLM Agent Orchestration CLI for evaluating prompt engineering techniques.")

def version_callback(value: bool):
    if value:
        print(f"LLM Agent Orchestration HW6 Version: {__version__}")
        raise typer.Exit()

@app.callback()
def enable_check(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
):
    """
    Assistant for Software Development.
    """
    pass

@app.command()
def analyze_results(
    dataset_path: Annotated[str, typer.Option(help="Path to the ground truth dataset.")] = "ground_truth_dataset.csv",
    results_path: Annotated[str, typer.Option(help="Path to the evaluation results.")] = "results",
    llms: Annotated[str, typer.Option(help="Comma-separated list of LLMs to analyze.")] = "GPT,Grok,peplexity",
    techniques: Annotated[str, typer.Option(help="Comma-separated list of techniques to analyze.")] = "baseline,few_shot,cot,react",
):
    """
    Analyze the manual evaluation results and generate a report.
    """
    print(f"Analyzing results with the following settings:")
    print(f"  - Dataset: {dataset_path}")
    print(f"  - Results path: {results_path}")
    print(f"  - LLMs: {llms}")
    print(f"  - Techniques: {techniques}")

    results = analyze(dataset_path, results_path, llms, techniques)

    print("\nResults:")
    for llm, llm_results in results.items():
        print(f"\nLLM: {llm}")
        for technique, accuracy in llm_results.items():
            print(f"  - {technique}: {accuracy}")

    # 3. Generate analysis report
    print("\nGenerating analysis report...")
    report_path = os.path.join(results_path, "ANALYSIS_REPORT.md")
    with open(report_path, "w") as f:
        f.write("# Analysis Report\n\n")
        f.write("## Accuracy and F1 Score by LLM and Technique\n\n")
        f.write("| LLM | Metric | Baseline | Few-shot | CoT | ReAct |\n")
        f.write("|---|---|---|---|---|---|\n")
        for llm, llm_results in results.items():
            f.write(f"| {llm} | Accuracy |")
            for technique in techniques.split(','):
                if technique in llm_results and isinstance(llm_results[technique], dict):
                    accuracy_val = llm_results[technique]['accuracy']
                    accuracy_str = f"{accuracy_val:.2f}" if isinstance(accuracy_val, float) else str(accuracy_val)
                    f.write(f" {accuracy_str} |")
                else:
                    f.write(" N/A |")
            f.write("\n")
            f.write(f"| {llm} | F1-Score |")
            for technique in techniques.split(','):
                if technique in llm_results and isinstance(llm_results[technique], dict):
                    f1_score_val = llm_results[technique]['f1_score']
                    f1_score_str = f"{f1_score_val:.2f}" if isinstance(f1_score_val, float) else str(f1_score_val)
                    f.write(f" {f1_score_str} |")
                else:
                    f.write(" N/A |")
            f.write("\n")

    print(f"\nAnalysis report generated at: {report_path}")

@app.command()
def run_evaluation(
    dataset_path: Annotated[str, typer.Option(help="Path to the ground truth dataset.")] = "ground_truth_dataset.csv",
    results_path: Annotated[str, typer.Option(help="Path to save the evaluation results.")] = "results",
    techniques: Annotated[str, typer.Option(help="Comma-separated list of techniques to evaluate.")] = "baseline,few_shot,cot,react",
):
    """
    Generate prompts for manual evaluation.
    """
    generate_prompts(dataset_path, results_path, techniques)

@app.command()
def generate_plot(
    results_path: Annotated[str, typer.Option(help="Path to the evaluation results.")] = "results",
):
    """
    Generate a plot from the analysis results.
    """
    plot_results_function(results_path)
    
if __name__ == "__main__":
    app()
