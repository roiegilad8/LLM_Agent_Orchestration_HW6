# 📋 HW6 - LLM Agent Orchestration - Complete Instructions

## Executive Summary
This project covers **LLM Agent Orchestration** with **4 prompt engineering techniques** evaluated on **100 questions** for a total of **400 evaluations**. Goal: Compare performance across Baseline, Few-shot, Chain-of-Thought (CoT), and ReAct.

---

## 🎯 DGS (Design Goals & Success Criteria)

### Project Objectives:
1. **Compare 4 Prompt Engineering Techniques** - baseline, few-shot, CoT, ReAct
2. **Evaluate on 100 Questions** - diverse dataset covering multiple domains
3. **Run 400 Total Evaluations** - 100 questions × 4 techniques
4. **Statistical Analysis** - mean, std, confidence intervals
5. **Production-Ready Code** - modular, reusable, well-documented

### Grading Rubric (60% Academic / 40% Technical):

#### Academic (60%):
- ✅ Clear problem statement and motivation
- ✅ Literature review of prompt engineering techniques
- ✅ Hypothesis and expected outcomes
- ✅ Rigorous evaluation methodology
- ✅ Comprehensive analysis of results
- ✅ Insights and conclusions

#### Technical (40%):
- ✅ Code quality (modular, clean, documented)
- ✅ Proper error handling and logging
- ✅ Efficient execution
- ✅ Reproducibility (can run with requirements.txt)
- ✅ GitHub repository structure
- ✅ CI/CD pipeline

### Success Metrics:
- **Accuracy**: > 70% for best technique
- **Speed**: Evaluation completes < 30 min
- **Code Quality**: 0 warnings, PEP-8 compliant
- **Documentation**: All functions documented
- **Reproducibility**: Can re-run anytime

---

## 📁 GitHub Repository Structure

```
LLM_Agent_Orchestration_HW6/
├── src/prom_eng/
│   ├── evaluators/
│   │   ├── base.py (BaseEvaluator abstract class)
│   │   ├── baseline.py (Baseline technique)
│   │   ├── few_shot.py (Few-shot technique)
│   │   ├── cot.py (Chain-of-Thought)
│   │   └── react.py (ReAct)
│   ├── utils/
│   │   └── llm_clients.py (LLM API clients)
│   ├── data/
│   │   ├── loader.py (Dataset loading)
│   │   └── cache.py (Response caching)
│   └── analysis/
│       └── orchestrator.py (Main orchestration)
├── results/
│   ├── baseline_results.json
│   ├── few_shot_results.json
│   ├── cot_results.json
│   ├── react_results.json
│   ├── summary.json
│   └── ANALYSIS_REPORT.md
├── ground_truth_dataset.json
├── requirements.txt
├── README.md
├── LICENSE
├── setup.py
└── .gitignore
```

### What each folder contains:
- **src/prom_eng/evaluators/** - 4 implementations of prompt techniques
- **src/prom_eng/utils/** - LLM clients (ChatGPT, Claude, etc.)
- **src/prom_eng/data/** - Loading questions, caching results
- **src/prom_eng/analysis/** - Main orchestrator that runs everything
- **results/** - Output JSON files with scores
- **ground_truth_dataset.json** - 100 questions with correct answers

---

## 🔧 How to Use This Project

### Step 1: Setup
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/LLM_Agent_Orchestration_HW6.git
cd LLM_Agent_Orchestration_HW6

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Keys
```bash
# Copy example env file
cp env.example .env

# Edit .env with your API keys:
# OPENAI_API_KEY=sk-...
# CLAUDE_API_KEY=sk-ant-...
```

### Step 3: Run Evaluation
```bash
# Run full orchestration (400 evaluations)
python -m src.prom_eng.analysis.orchestrator

# Or run specific technique:
python -m src.prom_eng.evaluators.baseline

# Results saved to results/ folder
```

### Step 4: View Results
```bash
# See summary
cat results/summary.json

# See detailed analysis
cat results/ANALYSIS_REPORT.md

# Plot results (if matplotlib installed)
python visualize_results.py
```

---

## 🤖 How to Use KICKOFF Agent

### Purpose:
KICKOFF Agent helps **plan** new projects - generates PRD, missions, progress tracker.

### How to Use:

#### Option 1: Perplexity AI (Recommended)
```
1. Go to: perplexity.ai
2. Paste the kickoff_agent_core_v3.1.md content
3. Add your project description
4. Let it generate PRD + missions
```

#### Option 2: Claude / ChatGPT
```
1. Open Claude or ChatGPT
2. Paste: kickoff_agent_core_v3.1.md
3. Add: "Create a PRD for: [your project description]"
4. Get structured planning document
```

### Output (What You Get):
- ✅ **PRD** - 17 sections with requirements
- ✅ **Missions** - 30-42 concrete tasks
- ✅ **Progress Tracker** - Milestones and checkpoints
- ✅ **.claude files** - Custom configuration for Claude

### Example Usage:
```
System: [paste kickoff_agent_core_v3.1.md]

User: "I want to build an LLM evaluation framework 
that tests 4 prompt techniques on 100 questions"

Agent: [Generates full PRD + 42 missions + tracker]
```

---

## 🎓 How to Use GRADER Agent

### Purpose:
GRADER Agent **grades** projects according to 7 categories.

### How to Use:

#### Step 1: Prepare Your Submission
```
1. Upload your code to GitHub
2. Have README.md ready
3. Have results/outputs ready
```

#### Step 2: Call the Grader
```
1. Go to: Claude or Perplexity
2. Paste: grader_agent.md
3. Add: "Grade this project: [GitHub URL]"
4. Get detailed rubric score
```

#### Step 3: Read Rubric
```
Grader evaluates on:
1. Problem Statement & Motivation (10%)
2. Literature Review (10%)
3. Methodology (15%)
4. Implementation (20%)
5. Results & Analysis (20%)
6. Code Quality (15%)
7. Documentation & Reproducibility (10%)

Bonus: +10% for excellence
```

### Example Grading Output:
```
Score Breakdown:
✅ Problem Statement: 9/10
✅ Literature Review: 8/10
✅ Methodology: 9/10
✅ Implementation: 9/10
✅ Results: 8/10
✅ Code Quality: 9/10
✅ Documentation: 9/10
➕ Bonus: +5%
═══════════════════
TOTAL: 88/100 (B+)
```

---

## 📊 GROUND TRUTH Dataset

### What is it?
A dataset of **100 questions** with **correct answers** (ground truth).

### Format:
```json
{
  "question_id": 1,
  "question": "What is 2+2?",
  "ground_truth": "4",
  "domain": "arithmetic",
  "difficulty": "easy"
}
```

### How to Use:
```python
from src.prom_eng.data.loader import load_dataset

# Load dataset
questions = load_dataset("ground_truth_dataset.json")

# Loop through questions
for q in questions:
    question = q["question"]
    expected = q["ground_truth"]
    
    # Run evaluator
    response = evaluator.evaluate(question)
    
    # Check if correct
    is_correct = response == expected
```

### Key Details:
- **100 questions** - diverse domains (math, logic, text)
- **4 difficulty levels** - easy, medium, hard, expert
- **Domain tags** - arithmetic, logic, reasoning, etc.
- **Curated answers** - validated by humans

---

## 🎯 Key Emphasis Points (IMPORTANT!)

### 1. **Modular Architecture**
- ✅ Each evaluator is independent
- ✅ Can add new techniques easily
- ✅ Easy to test each part
- ✅ Follows Single Responsibility Principle

### 2. **Clean Code**
- ✅ PEP-8 compliant
- ✅ Type hints everywhere
- ✅ Clear function names
- ✅ Docstrings on all functions
- ✅ No code duplication

### 3. **Reproducibility**
- ✅ requirements.txt has exact versions
- ✅ Random seeds set consistently
- ✅ Same results every run
- ✅ Easy to re-run evaluation
- ✅ Full logging of process

### 4. **Statistical Rigor**
- ✅ Calculate mean, std, median
- ✅ 95% confidence intervals
- ✅ Significance testing (if comparing)
- ✅ Clear visualizations
- ✅ Proper handling of edge cases

### 5. **Documentation**
- ✅ README with full instructions
- ✅ Code comments for complex logic
- ✅ Analysis report explaining results
- ✅ Examples in docstrings
- ✅ Setup guide for new users

### 6. **Performance**
- ✅ Cache API responses
- ✅ Parallel processing where possible
- ✅ Early exit on errors
- ✅ Timeout handling
- ✅ Memory efficiency

---

## 📈 The 4 Prompt Techniques

### 1. Baseline
```python
prompt = f"Question: {question}\nAnswer:"
response = llm.query(prompt)
```
- **Simple** - No special formatting
- **Fast** - Direct question to LLM
- **Baseline for comparison**
- Expected Accuracy: 50-60%

### 2. Few-Shot
```python
prompt = f"""
Examples:
Q: What is 2+2?
A: 4

Q: What is capital of France?
A: Paris

Question: {question}
Answer:"""
response = llm.query(prompt)
```
- **Context** - Shows examples first
- **Better** - LLM learns from examples
- **Medium complexity**
- Expected Accuracy: 65-75%

### 3. Chain-of-Thought (CoT)
```python
prompt = f"""
Let's think step by step.
Question: {question}
Step 1: ...
Step 2: ...
Answer:"""
response = llm.query(prompt)
```
- **Reasoning** - Forces step-by-step thinking
- **Better accuracy** - Reduces errors
- **Longer response**
- Expected Accuracy: 75-85%

### 4. ReAct (Reasoning + Acting)
```python
prompt = f"""
You can:
- Think: reason about the problem
- Act: perform an action
- Observe: see the result

Question: {question}

Think: ...
Act: ...
Observe: ...
Answer:"""
response = llm.query(prompt)
```
- **Complex** - Multi-step reasoning + actions
- **Best accuracy** - Often produces best results
- **Most tokens**
- Expected Accuracy: 80-90%

---

## 📊 Expected Results

### Accuracy by Technique:
```
Baseline:     ~50-60%
Few-shot:     ~65-75%
CoT:          ~75-85%
ReAct:        ~80-90%
```

### Speed by Technique:
```
Baseline:     Fast (1 sec per Q)
Few-shot:     Medium (2 sec per Q)
CoT:          Slow (3-4 sec per Q)
ReAct:        Slowest (5-10 sec per Q)
```

### Cost by Technique:
```
Baseline:     Cheapest (~$0.01 per Q)
Few-shot:     Medium (~$0.02 per Q)
CoT:          More (~$0.03 per Q)
ReAct:        Most (~$0.05 per Q)
```

---

## 🚀 How to Run Everything Together

### One-Command Execution:
```bash
# Full pipeline
python -m src.prom_eng.analysis.orchestrator \
  --dataset ground_truth_dataset.json \
  --output results/ \
  --techniques baseline few_shot cot react \
  --cache true \
  --parallel true
```

### Step-by-Step:
```bash
# 1. Validate dataset
python -m src.prom_eng.data.loader --validate

# 2. Run baseline
python -m src.prom_eng.evaluators.baseline --output results/baseline_results.json

# 3. Run few-shot
python -m src.prom_eng.evaluators.few_shot --output results/few_shot_results.json

# 4. Run CoT
python -m src.prom_eng.evaluators.cot --output results/cot_results.json

# 5. Run ReAct
python -m src.prom_eng.evaluators.react --output results/react_results.json

# 6. Analyze results
python -m src.prom_eng.analysis.orchestrator --analyze-only
```

---

## 🔍 Debugging & Troubleshooting

### API Key Issues:
```bash
# Check if .env is loaded
python -c "import os; print(os.getenv('OPENAI_API_KEY'))"

# Should print your key (or None if not set)
```

### Dataset Issues:
```bash
# Validate dataset format
python -m src.prom_eng.data.loader --validate-dataset ground_truth_dataset.json

# Check number of questions
python -c "import json; qs=json.load(open('ground_truth_dataset.json')); print(len(qs))"
```

### LLM Connection Issues:
```bash
# Test connection
python -m src.prom_eng.utils.llm_clients --test-openai
python -m src.prom_eng.utils.llm_clients --test-claude
```

---

## 🎓 Learning Outcomes

### What you'll learn:
1. **Prompt Engineering** - 4 different techniques
2. **Evaluation Frameworks** - How to measure LLM performance
3. **Statistical Analysis** - Comparing techniques
4. **Clean Code** - Modular, reusable code
5. **LLM APIs** - Working with different providers
6. **Project Management** - From planning to execution

### Next Learning Steps:
- [ ] Try with different LLMs (GPT-4, Gemini, etc.)
- [ ] Add more evaluation metrics
- [ ] Create visualization dashboard
- [ ] Deploy as web service
- [ ] A/B test in production
- [ ] Fine-tune prompts for your domain

---

## 📞 Available Resources

### Files Provided:
- ✅ `HW6_INSTRUCTIONS_HEBREW.md` - Instructions in Hebrew
- ✅ `HW6_INSTRUCTIONS_ENGLISH.md` - Instructions in English
- ✅ `kickoff_agent_core_v3.1.md` - Agent for planning projects
- ✅ `kickoff_templates_v3.1.md` - Templates library
- ✅ `grader_agent.md` - Agent for grading projects
- ✅ `ground_truth_dataset.json` - 100 test questions

### Key Project Files:
- `src/prom_eng/analysis/orchestrator.py` - Main entry point
- `ground_truth_dataset.json` - Your test data
- `results/ANALYSIS_REPORT.md` - Full analysis
- `requirements.txt` - All dependencies

### Next Steps:
1. ✅ Run `python -m src.prom_eng.analysis.orchestrator`
2. ✅ Check `results/summary.json`
3. ✅ Read `results/ANALYSIS_REPORT.md`
4. ✅ Use GRADER agent to get score
5. ✅ Submit to GitHub

---

## 📄 Final Notes

**This is YOUR project!** Everything is yours to:
- ✅ Re-run anytime
- ✅ Modify prompt techniques
- ✅ Add new questions
- ✅ Change evaluation metrics
- ✅ Adapt for new hardware/LLMs

**Key Files to Carry Forward:**
- `kickoff_agent_core_v3.1.md` - Use for planning new projects
- `grader_agent.md` - Use for grading any LLM project
- `ground_truth_dataset.json` - Use as benchmark questions

These are **reusable** for other projects and other LLMs!

---

**Good luck! 🚀**

Date: December 11, 2025
Status: ✅ Project Complete!