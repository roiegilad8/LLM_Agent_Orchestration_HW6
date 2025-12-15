# Architecture Documentation

## Overview

This project implements a **Prompt Engineering Benchmark Framework** that compares the effectiveness of four prompt engineering techniques (Baseline, Few-Shot, Chain-of-Thought, and ReAct) across three LLM models (GPT-4o, Grok-2, and Perplexity).

The architecture follows a modular, extensible design that separates concerns and enables easy addition of new models, techniques, and evaluation metrics.

---

## System Context (C4 Level 1)

```
┌─────────────────────────────────────────────────────────────────┐
│                     External Systems                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   OpenAI     │  │     xAI      │  │  Perplexity  │           │
│  │  (GPT-4o)    │  │  (Grok-2)    │  │  (Sonar)     │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│         ▲                  ▲                  ▲                  │
│         └──────────────────┼──────────────────┘                  │
│                            │                                     │
│                    HTTP/REST API Calls                           │
│                            │                                     │
└─────────────────────────────┼──────────────────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │  LLM Orchestration │
                    │    Framework       │
                    └────────────────────┘
                              │
                    ┌─────────▼──────────────────┐
                    │  Prompt Engineering       │
                    │  Benchmark System         │
                    │  (Python 3.12)            │
                    └──────────────────────────┘
                              │
                    ┌─────────▼──────────────────┐
                    │   Data Storage            │
                    │  (CSV, JSON, Images)      │
                    └──────────────────────────┘
```

---

## Container Architecture (C4 Level 2)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Prompt Engineering Benchmark                         │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                    Data Layer                                   │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────────┐     │  │
│  │  │ Questions  │  │  Responses │  │  Ground Truth Data   │     │  │
│  │  │ (CSV)      │  │  (CSV)     │  │  (JSON/CSV)          │     │  │
│  │  └────────────┘  └────────────┘  └──────────────────────┘     │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                    ▲                                    │
│                                    │                                    │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │               Processing Layer (Python Core)                    │  │
│  │                                                                  │  │
│  │  ┌──────────────────┐  ┌──────────────────┐                   │  │
│  │  │ Prompt Builder   │  │ API Orchestrator │                   │  │
│  │  │  - Baseline      │  │  - GPT-4o        │                   │  │
│  │  │  - Few-Shot      │  │  - Grok-2        │                   │  │
│  │  │  - CoT           │  │  - Perplexity    │                   │  │
│  │  │  - ReAct         │  └──────────────────┘                   │  │
│  │  └──────────────────┘                                          │  │
│  │                                                                  │  │
│  │  ┌──────────────────┐  ┌──────────────────┐                   │  │
│  │  │ Grading Engine   │  │ Analysis Module  │                   │  │
│  │  │  - Accuracy      │  │  - Metrics Calc  │                   │  │
│  │  │  - Fuzzy Match   │  │  - Aggregation   │                   │  │
│  │  │  - Validation    │  │  - Visualization │                   │  │
│  │  └──────────────────┘  └──────────────────┘                   │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                    ▲                                    │
│                                    │                                    │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                    Output Layer                                 │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────────┐     │  │
│  │  │  CSV       │  │  PNG/JPEG  │  │  Markdown Reports    │     │  │
│  │  │  Reports   │  │  Charts &  │  │  Documentation       │     │  │
│  │  │            │  │  Visuals   │  │                      │     │  │
│  │  └────────────┘  └────────────┘  └──────────────────────┘     │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture (C4 Level 3)

### Core Modules

#### 1. **Data Preparation** (`data_prep_FINAL.py`)
Loads raw responses from 12 files (4 techniques × 3 models) and creates standardized CSV datasets.

```
Input Files (12 TXT files)
      ↓
  Parse responses
      ↓
  Normalize format
      ↓
  results.csv (100 questions × 12 columns)
  ground_truth.csv (100 answers)
```

**Key Functions:**
- `load_responses(filepath)` - Reads from TXT/CSV/JSON
- `combine_datasets()` - Merges 12 files
- Handles variable row counts (pads/trims to 100)

---

#### 2. **Grading Engine** (`compare_results_FIXED.py`)
Evaluates LLM responses against ground truth answers using fuzzy matching.

```
results.csv + ground_truth.csv
         ↓
  Comparison loop (100 questions)
         ↓
  Fuzzy match algorithm (similarity score)
         ↓
  Accuracy calculation (strict match)
         ↓
  graded_scores.csv
```

**Key Functions:**
- `fuzzy_match(response, expected)` - Uses difflib.SequenceMatcher
- `calculate_accuracy()` - Counts exact matches
- `grade_all_responses()` - Main grading loop

---

#### 3. **Analysis Module** (`compare_results_FIXED.py`)
Generates metrics, aggregations, and visualizations.

```
graded_scores.csv
         ↓
  Calculate metrics per combination
         ↓
  Aggregate by technique & model
         ↓
  Generate 4 visualizations (PNG)
  Generate 2 reports (CSV)
         ↓
  outputs/ (6 files)
```

**Key Functions:**
- `calculate_metrics()` - Mean accuracy, std dev per combo
- `generate_charts()` - Matplotlib visualizations
- `aggregate_results()` - Group by technique/model

---

#### 4. **Visualization Layer**
Creates 4 publication-ready charts:

| Chart | Purpose | X-axis | Y-axis |
|-------|---------|--------|--------|
| `accuracy_by_technique.png` | Compare prompt techniques | Technique | Accuracy (%) |
| `accuracy_by_model.png` | Compare LLM models | Model | Accuracy (%) |
| `model_technique_heatmap.png` | 2D comparison grid | Model × Technique | Accuracy |
| `all_combinations.png` | All 12 combos ranked | Combination | Accuracy (%) |

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     Data Processing Pipeline                   │
└─────────────────────────────────────────────────────────────────┘

PHASE 1: Data Preparation
┌──────────────────┐
│ 12 TXT Files     │
│ (responses)      │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────┐
│ data_prep_FINAL.py           │
│ - Load from results/GPT/      │
│ - Load from results/Grok/     │
│ - Load from results/Perplexity│
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ results.csv (100 × 14)       │
│ ground_truth.csv (100 × 5)   │
└────────┬─────────────────────┘

PHASE 2: Grading
┌──────────────────┐
│ Comparison Loop  │
│ 100 iterations   │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────┐
│ compare_results_FIXED.py      │
│ - Fuzzy match each response   │
│ - Calculate accuracy          │
│ - Grade all 12 combinations   │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ graded_scores.csv            │
│ (100 rows × 14 columns)      │
└────────┬─────────────────────┘

PHASE 3: Analysis & Output
┌──────────────────┐
│ Analysis Module  │
│ - Metrics calc   │
│ - Aggregation    │
│ - Visualization  │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────┐
│ outputs/ (6 files)           │
│ - 4 PNG charts               │
│ - 2 CSV reports              │
└──────────────────────────────┘
```

---

## Directory Structure

```
LLM_Agent_Orchestration_HW6/
│
├── 📄 README.md                          # Project overview
├── 📄 CONTRIBUTING.md                    # Development guide
├── 📄 ARCHITECTURE.md                    # This file
├── 📄 PROMPTS_LOG.md                     # Prompt documentation
├── 📄 COST_ANALYSIS.md                   # Cost breakdown
│
├── 🐍 compare_results_FIXED.py          # Main analysis pipeline
├── 🐍 data_prep_FINAL.py                # Data preparation script
│
├── 🔧 pyproject.toml                     # Linting & formatting config
├── 🔧 .pre-commit-config.yaml            # Pre-commit hooks
├── 🔧 requirements.txt                   # Runtime dependencies
├── 🔧 requirements-dev.txt               # Dev dependencies
├── 🔧 .env.example                       # Environment template
│
├── 📁 .github/
│   └── workflows/
│       └── ci-cd.yml                     # CI/CD pipeline
│
├── 📁 results/
│   ├── GPT/                              # GPT-4o responses (12 files)
│   ├── Grok/                             # Grok-2 responses (12 files)
│   ├── Perplexity/                       # Perplexity responses (12 files)
│   ├── RESULTS.md                        # Summary document
│   └── prompts_log/
│       └── PROMPTS_LOG.md                # Prompt templates & examples
│
├── 📁 outputs/
│   ├── graded_scores.csv                 # All 100 questions graded
│   ├── detailed_metrics.csv              # Accuracy per combination
│   ├── accuracy_by_technique.png         # Bar chart: techniques
│   ├── accuracy_by_model.png             # Bar chart: models
│   ├── model_technique_heatmap.png       # 2D heatmap
│   └── all_combinations.png              # Ranked bar chart (12 combos)
│
└── 📁 docs/ (optional, for screenshots/diagrams)
    └── screenshots/                      # Visual documentation
```

---

## Module Dependencies

```
data_prep_FINAL.py
    │
    └── pandas
    └── os
    └── json

compare_results_FIXED.py
    │
    ├── pandas                    # CSV/JSON handling
    ├── difflib                   # Fuzzy matching
    ├── matplotlib                # Chart generation
    └── numpy                     # Array operations

External APIs (via HTTP)
    │
    ├── OpenAI API (GPT-4o)
    ├── xAI API (Grok-2)
    └── Perplexity API (Sonar)

Quality Standards
    │
    ├── Black                     # Code formatting
    ├── Ruff                      # Linting
    ├── isort                     # Import sorting
    ├── pytest                    # Testing
    └── mypy                      # Type checking
```

---

## Key Design Decisions (ADRs)

### ADR-1: Fuzzy Matching for Grading
**Decision:** Use Python's `difflib.SequenceMatcher` for similarity scoring.

**Rationale:**
- Handles typos and formatting variations
- Better than strict string equality
- No external library dependency
- Fast for 100 questions

**Trade-off:** May give partial credit to wrong answers. Mitigated by using both fuzzy score and exact match.

---

### ADR-2: CSV as Primary Storage
**Decision:** Use CSV for results and outputs instead of JSON.

**Rationale:**
- Human-readable in Excel/spreadsheets
- Easy to filter, sort, and analyze
- Standard for academic reporting
- Reduces data pipeline complexity

**Trade-off:** Less hierarchical than JSON. Mitigated by careful schema design.

---

### ADR-3: Modular Script Architecture
**Decision:** Two separate scripts (`data_prep_FINAL.py` and `compare_results_FIXED.py`) instead of single monolithic script.

**Rationale:**
- Separation of concerns (prepare vs. analyze)
- Easier to test and debug
- Can re-run analysis without re-fetching from APIs
- Clear data dependencies

**Trade-off:** Requires running two scripts in sequence. Mitigated by clear documentation.

---

### ADR-4: Matplotlib for Visualizations
**Decision:** Use Matplotlib instead of Plotly or Seaborn.

**Rationale:**
- Lightweight, no JavaScript required
- Publication-ready static images (PNG)
- Works in CI/CD pipelines
- Wide compatibility

**Trade-off:** Less interactive than Plotly. Acceptable for academic use.

---

## Extensibility Points

### Adding a New Prompt Technique

1. Create responses with new technique (e.g., `chain_of_verification.txt`)
2. Place in `results/GPT/chain_of_verification_GPT.txt`, etc.
3. Update `data_prep_FINAL.py` to include in file list:
   ```python
   'ChainOfVerification': 'results/GPT/chain_of_verification_GPT.txt'
   ```
4. Re-run: `python data_prep_FINAL.py && python compare_results_FIXED.py`

### Adding a New Model

1. Create response files for all 4 techniques
2. Place in new folder: `results/NewModel/`
3. Update file lists in `data_prep_FINAL.py`
4. Charts automatically update

### Adding a New Metric

1. Add calculation function in `compare_results_FIXED.py`:
   ```python
   def calculate_f1_score(graded_df):
       # Implementation
       return f1_scores
   ```
2. Add to output CSV generation
3. Visualize in charts

---

## Performance Characteristics

| Operation | Time | Resources |
|-----------|------|-----------|
| Data Preparation (12 files, 100 Qs) | ~2 sec | 50 MB RAM |
| Grading (Fuzzy match, 100 Qs × 12 combos) | ~5 sec | 100 MB RAM |
| Analysis & Visualization (4 charts, 2 CSVs) | ~3 sec | 150 MB RAM |
| **Total Pipeline** | **~10 sec** | **~200 MB RAM** |

---

## Testing Strategy

### Unit Tests (Using pytest)
- `test_grading.py` - Fuzzy match accuracy, exact match calculation
- `test_analysis.py` - Metrics aggregation, chart generation
- `test_data_prep.py` - File loading, data normalization

### Integration Tests
- Full pipeline: data_prep → compare_results
- CSV schema validation
- Chart PNG generation

### Quality Standards
- **Code Coverage:** Target ≥80%
- **Linting:** Ruff + Black pass without errors
- **Type Checking:** mypy with strict settings
- **Pre-commit:** All hooks pass before commit

### CI/CD Pipeline
- Runs on every push to `main` or `develop`
- Linting → Testing → Coverage → Build check
- Fails if coverage < 70%

---

## Future Improvements

1. **Parallel API Calls:** Currently sequential. Use `asyncio` for parallel requests.
2. **Caching:** Cache API responses to avoid re-calling during development.
3. **Web Dashboard:** Interactive visualization via Flask/Streamlit.
4. **Database:** Store results in PostgreSQL instead of CSV for querying.
5. **Prompt Versioning:** Track prompt iterations and their impact on accuracy.
6. **Cost Optimization:** Implement token counting to predict costs before running.

---

## References

- **C4 Model:** https://c4model.com/
- **Prompt Engineering:** https://platform.openai.com/docs/guides/prompt-engineering
- **Fuzzy Matching:** Python `difflib` documentation
- **CI/CD:** GitHub Actions documentation
- **Code Quality:** Black, Ruff, pytest documentation

---

**Last Updated:** December 15, 2025  
**Author:** LLM Orchestration HW6 Team
