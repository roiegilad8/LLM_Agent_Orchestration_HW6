# Prompt Engineering Experiments - Exact Prompts Used

**Date:** Dec 15, 2025  
**Models Tested:** GPT, Grok, Perplexity  
**Questions:** 100 (Math, Logic, Language, Code, Knowledge, Puzzles)  
**Results:** Final analysis and visualizations are in the `outputs/` folder.

---

This document logs the exact prompt templates and examples used for each of the four prompt engineering techniques in this experiment.

## 1. Baseline Prompt

The baseline prompt provides the question directly with no additional context or examples.

### Template
```
Question: {question}
Answer:
```

### Example from File (Question 1)
```
----- Prompt for Question 1 -----
Question: What is 15 + 23?
Answer:
```

---

## 2. Few-Shot Prompt

The few-shot prompt provides two static examples of correct question-answer pairs before presenting the actual question.

### Template
```
Examples:
Q: What is 2+2?
A: 4

Q: What is capital of France?
A: Paris

Question: {question}
Answer:
```

### Example from File (Question 1)
```
----- Prompt for Question 1 -----
Examples:
Q: What is 2+2?
A: 4

Q: What is capital of France?
A: Paris

Question: What is 15 + 23?
Answer:
```

---

## 3. Chain-of-Thought (CoT) Prompt

The CoT prompt instructs the model to "think step by step" before providing the final answer, encouraging a reasoning process.

### Template
```
Let's think step by step.
Question: {question}
Step 1: ...
Step 2: ...
Answer:
```

### Example from File (Question 1)
```
----- Prompt for Question 1 -----
Let's think step by step.
Question: What is 15 + 23?
Step 1: ...
Step 2: ...
Answer:
```

---

## 4. ReAct Prompt

The ReAct prompt provides a framework for the model to "Think, Act, and Observe," simulating a reasoning loop to break down the problem.

### Template
```
You can:
- Think: reason about the problem
- Act: perform an action  
- Observe: see the result

Question: {question}

Think: ...
Act: ...
Observe: ...
Answer:
```

### Example from File (Question 1)
```
----- Prompt for Question 1 -----
You can:
- Think: reason about the problem
- Act: perform an action
- Observe: see the result

Question: What is 15 + 23?

Think: ...
Act: ...
Observe: ...
Answer:
```
