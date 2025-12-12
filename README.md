# LLM Agent Orchestration - HW6

## Executive Summary
This project focuses on **LLM Agent Orchestration**, comparing the performance of **4 prompt engineering techniques**: Baseline, Few-shot, Chain-of-Thought (CoT), and ReAct. The primary goal is to evaluate these techniques on a diverse dataset and analyze their effectiveness.

## Project Objectives:
1.  **Compare 4 Prompt Engineering Techniques** - baseline, few-shot, CoT, ReAct.
2.  **Evaluate on 100 Questions** - using a diverse dataset covering multiple domains.
3.  **Statistical Analysis** - to compare performance across techniques.
4.  **Modular and Reusable Code** - designed for clarity and future expansion.

## Repository Structure

```
LLM_Agent_Orchestration_HW6/
├── llm_orchestration_hw6/
│   ├── cli/
│   │   └── main.py (CLI entry point)
│   ├── config/
│   │   └── settings.yaml
│   ├── data/
│   │   ├── __init__.py
│   │   └── loader.py (Dataset loading)
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── metrics/
│   │   │   ├── __init__.py
│   │   │   └── metrics.py (Accuracy calculation)
│   │   ├── orchestrator.py (Main orchestration for analysis)
│   │   └── techniques/
│   │       ├── __init__.py
│   │       ├── base.py (BaseEvaluator abstract class)
│   │       ├── baseline.py (Baseline technique)
│   │       ├── cot.py (Chain-of-Thought)
│   │       ├── few_shot.py (Few-shot technique)
│   │       └── react.py (ReAct)
│   ├── llms/
│   │   ├── __init__.py
│   │   └── providers/
│   │       ├── __init__.py
│   │       └── openai_client.py (OpenAI API client - currently mocked for prompt generation)
│   └── prompts/
│       └── __init__.py
├── results/
│   ├── prompts/
│   │   ├── baseline_prompts.txt
│   │   ├── cot_prompts.txt
│   │   ├── few_shot_prompts.txt
│   │   └── react_prompts.txt
│   └── ANALYSIS_REPORT.md
├── ground_truth_dataset.csv
├── requirements.txt
├── README.md
├── .gitignore
└── setup.py
```

## Setup

1.  **Navigate to the project directory:**
    ```bash
    cd LLM_Agent_Orchestration_HW6
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

This project supports two main workflows: **Generating Prompts for Manual Testing** and **Analyzing Manual Evaluation Results**.

### 1. Generating Prompts for Manual Testing

To generate the prompts for each technique that you can then manually input into LLM chat interfaces (like OpenAI Playground, Claude, Perplexity, etc.):

```bash
cd LLM_Agent_Orchestration_HW6
source .venv/bin/activate
python llm_orchestration_hw6/evaluation/orchestrator.py \
  --dataset-path ground_truth_dataset.csv \
  --results-path results
```

The generated prompt files (e.g., `baseline_prompts.txt`, `few_shot_prompts.txt`) will be saved in the `results/prompts` directory.

### 2. Providing Manual Evaluation Results

After you have manually run the prompts in your chosen LLMs, you need to provide the responses in a structured format for analysis.

For each LLM (e.g., GPT, Grok, Perplexity) and each technique, create a separate text file within the `results/<LLM_NAME>/` directory. For example:

*   `results/GPT/baseline_prompts_GPT.txt`
*   `results/GPT/few_shot_prompts_GPT.txt`
*   `results/GPT/cot_prompts_GPT.txt`
*   `results/GPT/react_prompts_GPT.txt`
*   (and similarly for Grok and Perplexity)

Each file should contain the responses from the LLM, one response per line, in the same order as the questions appeared in the generated prompt files. Ensure to remove any question numbers or headers from the responses.

### 3. Analyzing Manual Evaluation Results

Once you have placed your response files in the correct directories, you can run the analysis to calculate accuracy for each technique and LLM:

```bash
cd LLM_Agent_Orchestration_HW6
source .venv/bin/activate
python llm_orchestration_hw6/evaluation/orchestrator.py \
  --dataset-path ground_truth_dataset.csv \
  --results-path results \
  --llms "GPT,Grok,peplexity" \
  --techniques "baseline,few_shot,cot,react" analyze-results
```

This command will:
*   Load the ground truth dataset.
*   Read your provided response files.
*   Calculate the accuracy for each combination of LLM and technique.
*   Print the results to the console.
*   Generate a detailed `ANALYSIS_REPORT.md` in the `results/` directory summarizing the accuracies.

## Analysis Report

A markdown file named `ANALYSIS_REPORT.md` will be generated in the `results/` directory, providing a summary of the accuracy for each LLM and technique.

## Learning Outcomes (from original instructions)

*   **Prompt Engineering** - Understanding 4 different techniques.
*   **Evaluation Frameworks** - How to measure LLM performance.
*   **Statistical Analysis** - Comparing techniques.
*   **Clean Code** - Modular, reusable code.
*   **LLM APIs** - Working with different providers.
*   **Project Management** - From planning to execution.

---
Date: December 12, 2025
Status: Project Ready for Evaluation and Analysis
