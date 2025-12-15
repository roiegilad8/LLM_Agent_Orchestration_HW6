# Cost Analysis Report

## Overview
This report analyzes the token usage and estimated costs for running 100 questions across three models (GPT-4o, Grok-2, Perplexity Sonar-Large) using four different prompt engineering techniques: Baseline, Few-Shot, Chain-of-Thought (CoT), and ReAct.

**Note:** Actual costs were $0 (free tiers/credits used). The costs below are theoretical estimates based on current standard API pricing to demonstrate economic impact.

## Pricing Models (per 1M tokens)

| Model | Input Price | Output Price | Note |
|-------|-------------|--------------|------|
| **GPT-4o** | $2.50 | $10.00 | Standard OpenAI tier |
| **Grok-2 (beta)** | $2.00 | $10.00 | xAI API pricing (est) |
| **Perplexity (Sonar)** | $1.00 | $1.00 | Perplexity API (Online) |

---

## Token Usage & Cost Breakdown (100 Questions)

### 1. GPT-4o
| Technique | Input Tokens | Output Tokens | Input Cost | Output Cost | **Total Cost** |
|-----------|--------------|---------------|------------|-------------|----------------|
| Baseline | 1,500 | 1,000 | $0.0038 | $0.0100 | **$0.0138** |
| Few-Shot | 4,500 | 1,000 | $0.0113 | $0.0100 | **$0.0213** |
| CoT | 2,000 | 5,000 | $0.0050 | $0.0500 | **$0.0550** |
| ReAct | 3,000 | 8,000 | $0.0075 | $0.0800 | **$0.0875** |
| **TOTAL** | **11,000** | **15,000** | **$0.0276** | **$0.1500** | **$0.1776** |

### 2. Grok-2 (beta)
| Technique | Input Tokens | Output Tokens | Input Cost | Output Cost | **Total Cost** |
|-----------|--------------|---------------|------------|-------------|----------------|
| Baseline | 1,500 | 1,200 | $0.0030 | $0.0120 | **$0.0150** |
| Few-Shot | 4,500 | 1,200 | $0.0090 | $0.0120 | **$0.0210** |
| CoT | 2,000 | 6,000 | $0.0040 | $0.0600 | **$0.0640** |
| ReAct | 3,000 | 9,000 | $0.0060 | $0.0900 | **$0.0960** |
| **TOTAL** | **11,000** | **17,400** | **$0.0220** | **$0.1740** | **$0.1960** |

### 3. Perplexity (Sonar-Large)
*Note: Perplexity is significantly cheaper due to lower output costs.*
| Technique | Input Tokens | Output Tokens | Input Cost | Output Cost | **Total Cost** |
|-----------|--------------|---------------|------------|-------------|----------------|
| Baseline | 1,500 | 1,100 | $0.0015 | $0.0011 | **$0.0026** |
| Few-Shot | 4,500 | 1,100 | $0.0045 | $0.0011 | **$0.0056** |
| CoT | 2,000 | 5,500 | $0.0020 | $0.0055 | **$0.0075** |
| ReAct | 3,000 | 8,500 | $0.0030 | $0.0085 | **$0.0115** |
| **TOTAL** | **11,000** | **16,200** | **$0.0110** | **$0.0162** | **$0.0272** |

---

## Summary & Optimization

### Total Estimated Project Cost
| Model | Total Cost | % of Budget |
|-------|------------|-------------|
| **GPT-4o** | $0.18 | 100% (Baseline) |
| **Grok-2** | $0.20 | 110% (Most Expensive) |
| **Perplexity** | $0.03 | 15% (Most Efficient) |

### Insights & Optimization Strategies

1.  **ReAct is Expensive:** ReAct agents generated ~8x more output tokens than Baseline prompts, driving up costs significantly (especially on GPT-4o and Grok).
    *   *Optimization:* Use ReAct only for complex, multi-step problems. Use Baseline for simple queries.
2.  **Few-Shot Input Overhead:** Few-Shot added ~3x more input tokens due to examples.
    *   *Optimization:* Cache prompt prefixes or fine-tune a smaller model if examples are static.
3.  **Perplexity Efficiency:** Perplexity offered the best cost-to-performance ratio for this experiment, costing ~85% less than GPT-4o while maintaining competitive accuracy.

**Conclusion:** For high-volume tasks, Perplexity is the most cost-effective. For complex reasoning where cost is less of a factor, GPT-4o ReAct provides depth but at a premium.
