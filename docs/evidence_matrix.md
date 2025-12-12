# Evidence Matrix

This matrix provides a comprehensive list of project claims and how each can be verified, demonstrating adherence to requirements and rubric criteria.

## 1. Project Setup & Installation

| Claim | Verification Command | Expected Output | Artifact/Location |
|---|---|---|---|
| Project is pip-installable | `pip install -e .` | Successfully installed `llm_orchestration_hw6` | Terminal output |
| All dependencies are listed in `requirements.txt` | `pip install -r requirements.txt` | All requirements satisfied or installed successfully | Terminal output |
| Virtual environment is used | `source .venv/bin/activate && which python` | Path to python executable inside `.venv` directory | Terminal output |

## 2. Code Quality & Structure

| Claim | Verification Command | Expected Output | Artifact/Location |
|---|---|---|---|
| Code adheres to PEP-8 standards | `flake8 llm_orchestration_hw6` | No errors or warnings | Terminal output |
| Code is type-hinted | `mypy llm_orchestration_hw6` | No type errors | Terminal output |
| Docstring coverage is sufficient | `interrogate -m llm_orchestration_hw6` | Report showing >=70% coverage | Terminal output |
| Modular repository structure | `ls -F llm_orchestration_hw6/` | Directories like `cli/`, `data/`, `evaluation/`, `llms/`, `prompts/` | Terminal output |
| Files generally less than 150 LOC | `find llm_orchestration_hw6 -name "*.py" -exec wc -l {} \; | awk '$1 > 150 {count++} END {print count " files exceed 150 LOC"}'` | "X files exceed 150 LOC" where X is small or 0 | Terminal output |

## 3. Testing & Reliability

| Claim | Verification Command | Expected Output | Artifact/Location |
|---|---|---|---|
| Unit tests are present and pass | `pytest tests/test_loader.py` | All tests passed | Terminal output |
| Test coverage is sufficient (e.g., >=70%) | `pytest --cov=llm_orchestration_hw6 --cov-report=term-missing` | Coverage report showing >=70% for `llm_orchestration_hw6` | Terminal output |
| Error handling for file operations | (e.g., Run `analyze-results` with non-existent dataset path) | Graceful error message (e.g., `FileNotFoundError`) | Terminal output |
| LLM API errors are handled gracefully | (Simulate LLM API error in `openai_client.py` and run evaluation) | "An error occurred: ..." message, no crash | Terminal output |

## 4. Functionality & Evaluation

| Claim | Verification Command | Expected Output | Artifact/Location |
|---|---|---|---|
| Dataset loads successfully | `python -m llm_orchestration_hw6.cli.main analyze-results --dataset-path ground_truth_dataset.csv --results-path results --llms GPT --techniques baseline` (check first few lines of output) | "Loaded 100 questions." | Terminal output |
| Prompts are generated for each technique | `python -m llm_orchestration_hw6.cli.main run-evaluation --dataset-path ground_truth_dataset.csv --results-path results --techniques baseline` | `results/prompts/baseline_prompts.txt` exists and contains prompts | File system |
| Accuracy is calculated correctly | (Run analysis command) | Printed accuracy values | Terminal output |
| Analysis report is generated | `python -m llm_orchestration_hw6.cli.main analyze-results --dataset-path ground_truth_dataset.csv --results-path results --llms GPT --techniques baseline` | `results/ANALYSIS_REPORT.md` exists and contains formatted results | File system |
| Plots are generated for visualization | `python -m llm_orchestration_hw6.cli.main generate-plot --results-path results` | `results/accuracy_comparison.png` exists | File system |

## 5. Documentation

| Claim | Verification Command | Expected Output | Artifact/Location |
|---|---|---|---|
| `README.md` is comprehensive | `cat README.md` | Contains sections on setup, usage, etc. | `README.md` |
| ADRs are present | `ls docs/adr` | List of ADR markdown files | File system |
| C4 Diagrams are present | `ls docs/c4` | List of PlantUML diagram files | File system |
| Extensibility Guide exists | `cat docs/extensibility/extensibility_guide.md` | Content describing extension points | `docs/extensibility/extensibility_guide.md` |
| Usability Analysis exists | `cat docs/usability/usability_analysis.md` | Content analyzing CLI usability | `docs/usability/usability_analysis.md` |

## 6. Configuration & Security

| Claim | Verification Command | Expected Output | Artifact/Location |
|---|---|---|---|
| `.env.example` is present | `ls .env.example` | File exists | File system |
| API keys are loaded securely | (Inspect `openai_client.py` for `os.environ.get`) | Code shows `os.environ.get` for API key | `llm_orchestration_hw6/llms/providers/openai_client.py` |
| `.gitignore` is comprehensive | `cat .gitignore` | Contains exclusions for `.venv/`, `__pycache__/`, `results/`, etc. | `.gitignore` |

## 7. Extensibility

| Claim | Verification Command | Expected Output | Artifact/Location |
|---|---|---|---|
| New technique can be added easily | (Follow steps in `extensibility_guide.md` to add a dummy technique) | New technique is recognized and generates prompts | `docs/extensibility/extensibility_guide.md` and terminal output |
| New LLM provider can be added easily | (Follow steps in `extensibility_guide.md` to add a dummy LLM provider) | New LLM provider is recognized and can be used | `docs/extensibility/extensibility_guide.md` and terminal output |
| New metric can be added easily | (Follow steps in `extensibility_guide.md` to add a dummy metric) | New metric is calculated and appears in report | `docs/extensibility/extensibility_guide.md` and terminal output |