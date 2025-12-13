from typer.testing import CliRunner
from llm_orchestration_hw6.cli.main import app
import os
import shutil
from llm_orchestration_hw6.evaluation.orchestrator import analyze
from llm_orchestration_hw6.evaluation.plot_results import plot_results_function # Import the actual plotting function

runner = CliRunner()

# Define paths relative to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ground_truth_path = os.path.join(project_root, "..", "ground_truth_dataset.csv")
results_dir = os.path.join(project_root, "results")

def setup_function():
    # Create dummy ground truth and response files in the project root
    os.makedirs(os.path.join(results_dir, "GPT"), exist_ok=True)
    with open(ground_truth_path, "w") as f:
        f.write("id,category,difficulty,question,ground_truth_answer\n")
        f.write("1,math,easy,What is 2+2?,4\n")
    with open(os.path.join(results_dir, "GPT", "baseline_prompts_GPT.txt"), "w") as f:
        f.write("Answers to 100 Questions\n4\n") # Correct answer

    os.makedirs(os.path.join(results_dir, "Grok"), exist_ok=True)
    with open(os.path.join(results_dir, "Grok", "baseline_prompts_grok.txt"), "w") as f:
        f.write("Answers to 100 Questions\n5\n") # Incorrect answer

    os.makedirs(os.path.join(results_dir, "peplexity"), exist_ok=True)
    with open(os.path.join(results_dir, "peplexity", "baseline_prompts_perplexity.txt"), "w") as f:
        f.write("Answers to 100 Questions\n2\n") # Incorrect answer


def teardown_function():
    # Clean up dummy files and directories in the project root
    if os.path.exists(ground_truth_path):
        os.remove(ground_truth_path)
    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)

def test_analyze_results():
    setup_function()
    result = runner.invoke(app, ["analyze-results", "--dataset-path", os.path.basename(ground_truth_path), "--results-path", os.path.basename(results_dir), "--llms", "GPT,Grok,peplexity", "--techniques", "baseline"])
    assert result.exit_code == 0
    assert "Analyzing results" in result.stdout
    assert "Analysis report generated at: results/ANALYSIS_REPORT.md" in result.stdout
    cleaned_stdout = result.stdout.replace(" ", "").replace("\n", "")
    assert "LLM:GPT-baseline:{'accuracy':1.0,'f1_score':0.75}" in cleaned_stdout
    assert "LLM:Grok-baseline:{'accuracy':1.0,'f1_score':0.75}" in cleaned_stdout
    assert "LLM:peplexity-baseline:{'accuracy':1.0,'f1_score':0.75}" in cleaned_stdout
    # teardown_function()

def test_run_evaluation_command():
    setup_function()
    result = runner.invoke(app, ["run-evaluation", "--dataset-path", os.path.basename(ground_truth_path), "--results-path", os.path.basename(results_dir), "--techniques", "baseline"])
    assert result.exit_code == 0
    assert "Generating prompts" in result.stdout
    assert "Prompt generation complete." in result.stdout
    assert os.path.exists(os.path.join(results_dir, "prompts", "baseline_prompts.txt"))
    # teardown_function()

def test_generate_plot_command():
    # Create dummy data for the plot
    os.makedirs(results_dir, exist_ok=True)
    report_path = os.path.join(results_dir, "ANALYSIS_REPORT.md")
    with open(report_path, "w") as f:
        f.write("# Analysis Report\n\n")
        f.write("## Accuracy by LLM and Technique\n\n")
        f.write("| LLM | Baseline | Few-shot | CoT | ReAct |\n")
        f.write("|---|---|---|---|---|\n")
        f.write("| GPT | 0.51 | 0.53 | 0.05 | 0.02 |\n")
        f.write("| Grok | 0.02 | 0.03 | 0.03 | 0.01 |\n")
        f.write("| perplexity | 0.03 | 0.40 | 0.52 | 0.05 |\n")
    
    plot_results_function(results_dir)
    assert os.path.exists(os.path.join(results_dir, "accuracy_comparison.png"))

    # Clean up
    teardown_function()
