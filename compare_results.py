#!/usr/bin/env python3
"""
Prompt Engineering Techniques - Results Comparison & Analysis
Compares 4 techniques (Baseline, Few-Shot, CoT, ReACT) across 3 models (GPT, Grok, Perplexity)
against ground truth with detailed analysis and visualizations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from difflib import SequenceMatcher
from pathlib import Path
import json

# ============================================================================
# CONFIGURATION
# ============================================================================

TECHNIQUES = ['Baseline', 'FewShot', 'CoT', 'ReACT']
MODELS = ['GPT', 'Grok', 'Perplexity']
DOMAINS = {
    'Arithmetic': (1, 7),
    'Logic': (16, 30),
    'Linguistics': (31, 44),
    'Programming': (45, 58),
    'General_Knowledge': (59, 72),
    'Design_Lateral': (73, 86),
    'Applied_Integration': (87, 100)
}

GRADING_METHOD = 'fuzzy'  # Options: 'exact', 'fuzzy', 'semantic'
FUZZY_THRESHOLD = 0.85  # For fuzzy matching (0-1)

# ============================================================================
# GRADING FUNCTIONS
# ============================================================================

def exact_match(ground_truth, predicted):
    """Exact string matching (case-insensitive)."""
    gt_clean = str(ground_truth).strip().lower()
    pred_clean = str(predicted).strip().lower()
    return 1.0 if gt_clean == pred_clean else 0.0


def fuzzy_match(ground_truth, predicted, threshold=0.85):
    """
    Fuzzy matching using SequenceMatcher.
    Returns similarity ratio (0-1), 1.0 if above threshold, else scaled partial credit.
    """
    gt_clean = str(ground_truth).strip().lower()
    pred_clean = str(predicted).strip().lower()
    
    if gt_clean == pred_clean:
        return 1.0
    
    similarity = SequenceMatcher(None, gt_clean, pred_clean).ratio()
    
    if similarity >= threshold:
        return 1.0  # Full credit
    elif similarity >= threshold * 0.5:
        return similarity  # Partial credit (normalized)
    else:
        return 0.0  # No credit


def semantic_similarity(ground_truth, predicted):
    """
    Placeholder for semantic similarity (would use embeddings in production).
    For now, uses fuzzy match as proxy.
    """
    return fuzzy_match(ground_truth, predicted, threshold=0.80)


# ============================================================================
# DATA LOADING & PROCESSING
# ============================================================================

def load_data(results_csv_path, ground_truth_path):
    """
    Load results and ground truth from CSV files.
    
    Expected format:
    - results_csv: columns = [question_id, domain, GPT_Baseline, GPT_FewShot, ..., Perplexity_ReACT]
    - ground_truth_path: columns = [question_id, answer] or loaded separately
    """
    df_results = pd.read_csv(results_csv_path)
    df_truth = pd.read_csv(ground_truth_path)
    
    return df_results, df_truth


def grade_responses(df_results, ground_truth_dict, method='fuzzy'):
    """
    Grade all model responses against ground truth.
    
    Args:
        df_results: DataFrame with model responses
        ground_truth_dict: Dict {question_id: correct_answer}
        method: 'exact', 'fuzzy', or 'semantic'
    
    Returns:
        DataFrame with scores for each model-technique combination
    """
    
    grader = {
        'exact': exact_match,
        'fuzzy': lambda gt, pred: fuzzy_match(gt, pred, FUZZY_THRESHOLD),
        'semantic': semantic_similarity
    }[method]
    
    # Create scoring dataframe
    score_df = df_results[['question_id', 'domain']].copy()
    
    # Score each model-technique combination
    for model in MODELS:
        for technique in TECHNIQUES:
            col_name = f'{model}_{technique}'
            scores = []
            
            for _, row in df_results.iterrows():
                q_id = row['question_id']
                ground_truth = ground_truth_dict.get(q_id, None)
                predicted = row.get(col_name, None)
                
                if ground_truth is None or predicted is None:
                    score = 0.0
                else:
                    score = grader(ground_truth, predicted)
                
                scores.append(score)
            
            score_df[col_name] = scores
    
    return score_df


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def calculate_aggregate_stats(score_df):
    """Calculate accuracy metrics by model, technique, and domain."""
    
    stats = {}
    
    # Overall accuracy by model
    stats['by_model'] = {}
    for model in MODELS:
        model_cols = [col for col in score_df.columns if col.startswith(model)]
        stats['by_model'][model] = score_df[model_cols].mean().mean()
    
    # Overall accuracy by technique
    stats['by_technique'] = {}
    for technique in TECHNIQUES:
        technique_cols = [col for col in score_df.columns if technique in col]
        stats['by_technique'][technique] = score_df[technique_cols].mean().mean()
    
    # Accuracy by domain
    stats['by_domain'] = {}
    for domain, (start, end) in DOMAINS.items():
        domain_df = score_df[score_df['question_id'].between(start, end)]
        domain_cols = [col for col in domain_df.columns 
                      if any(model in col for model in MODELS)]
        stats['by_domain'][domain] = domain_df[domain_cols].mean().mean()
    
    # Model-Technique matrix
    stats['model_technique_matrix'] = {}
    for model in MODELS:
        stats['model_technique_matrix'][model] = {}
        for technique in TECHNIQUES:
            col_name = f'{model}_{technique}'
            if col_name in score_df.columns:
                stats['model_technique_matrix'][model][technique] = score_df[col_name].mean()
    
    return stats


def calculate_detailed_metrics(score_df):
    """Calculate detailed metrics for each model-technique combination."""
    
    metrics = []
    
    for model in MODELS:
        for technique in TECHNIQUES:
            col_name = f'{model}_{technique}'
            if col_name in score_df.columns:
                scores = score_df[col_name]
                metrics.append({
                    'Model': model,
                    'Technique': technique,
                    'Accuracy': scores.mean(),
                    'Std_Dev': scores.std(),
                    'Min': scores.min(),
                    'Max': scores.max(),
                    'Median': scores.median(),
                    'Total_Questions': len(scores)
                })
    
    return pd.DataFrame(metrics)


def domain_performance(score_df):
    """Calculate accuracy by domain for each model-technique combo."""
    
    results = []
    
    for domain, (start, end) in DOMAINS.items():
        domain_df = score_df[score_df['question_id'].between(start, end)]
        
        for model in MODELS:
            for technique in TECHNIQUES:
                col_name = f'{model}_{technique}'
                if col_name in domain_df.columns:
                    accuracy = domain_df[col_name].mean()
                    results.append({
                        'Domain': domain,
                        'Model': model,
                        'Technique': technique,
                        'Accuracy': accuracy
                    })
    
    return pd.DataFrame(results)


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def plot_accuracy_by_technique(stats):
    """Plot 1: Accuracy comparison by technique (bar chart)."""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    techniques = list(stats['by_technique'].keys())
    accuracies = list(stats['by_technique'].values())
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    bars = ax.bar(techniques, accuracies, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    ax.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
    ax.set_xlabel('Technique', fontsize=12, fontweight='bold')
    ax.set_title('Overall Accuracy by Technique\n(All Models & Domains)', 
                 fontsize=14, fontweight='bold')
    ax.set_ylim([0, 1.0])
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2%}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    return fig


def plot_accuracy_by_model(stats):
    """Plot 2: Accuracy comparison by model (bar chart)."""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    models = list(stats['by_model'].keys())
    accuracies = list(stats['by_model'].values())
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    bars = ax.bar(models, accuracies, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    ax.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
    ax.set_xlabel('Model', fontsize=12, fontweight='bold')
    ax.set_title('Overall Accuracy by Model\n(All Techniques & Domains)', 
                 fontsize=14, fontweight='bold')
    ax.set_ylim([0, 1.0])
    ax.grid(axis='y', alpha=0.3)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2%}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    return fig


def plot_model_technique_heatmap(stats):
    """Plot 3: Heatmap of accuracy by model × technique."""
    
    # Build matrix from stats
    matrix_data = []
    for model in MODELS:
        row = [stats['model_technique_matrix'][model][tech] 
               for tech in TECHNIQUES]
        matrix_data.append(row)
    
    matrix = np.array(matrix_data)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(matrix, annot=True, fmt='.2%', cmap='RdYlGn', 
                xticklabels=TECHNIQUES, yticklabels=MODELS,
                cbar_kws={'label': 'Accuracy'}, ax=ax, linewidths=0.5)
    
    ax.set_title('Accuracy: Model × Technique Heatmap', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Technique', fontsize=12, fontweight='bold')
    ax.set_ylabel('Model', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    return fig


def plot_domain_performance(domain_perf_df):
    """Plot 4: Accuracy by domain (grouped bar chart)."""
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    domains = list(DOMAINS.keys())
    x = np.arange(len(domains))
    width = 0.08
    
    colors_by_combo = {}
    color_idx = 0
    for model in MODELS:
        for technique in TECHNIQUES:
            colors_by_combo[f'{model}_{technique}'] = plt.cm.tab20(color_idx)
            color_idx += 1
    
    for i, model in enumerate(MODELS):
        for j, technique in enumerate(TECHNIQUES):
            mask = (domain_perf_df['Model'] == model) & (domain_perf_df['Technique'] == technique)
            values = domain_perf_df[mask].set_index('Domain').reindex(domains)['Accuracy'].values
            offset = (i * len(TECHNIQUES) + j - len(MODELS) * len(TECHNIQUES) / 2) * width
            ax.bar(x + offset, values, width, label=f'{model}-{technique}', alpha=0.8)
    
    ax.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
    ax.set_xlabel('Domain', fontsize=12, fontweight='bold')
    ax.set_title('Accuracy by Domain (All Model-Technique Combinations)', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(domains, rotation=45, ha='right')
    ax.set_ylim([0, 1.0])
    ax.grid(axis='y', alpha=0.3)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=1, fontsize=8)
    
    plt.tight_layout()
    return fig


def plot_domain_aggregate(domain_perf_df):
    """Plot 5: Average accuracy by domain (simpler view)."""
    
    domain_avg = domain_perf_df.groupby('Domain')['Accuracy'].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.viridis(np.linspace(0, 1, len(domain_avg)))
    bars = ax.barh(domain_avg.index, domain_avg.values, color=colors, edgecolor='black', linewidth=1.5)
    
    ax.set_xlabel('Average Accuracy', fontsize=12, fontweight='bold')
    ax.set_title('Average Accuracy by Domain\n(Across All Models & Techniques)', 
                 fontsize=14, fontweight='bold')
    ax.set_xlim([0, 1.0])
    ax.grid(axis='x', alpha=0.3)
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2.,
                f'{width:.1%}', ha='left', va='center', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    return fig


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution flow.
    
    Required files:
    1. 'results.csv' - Model responses with structure:
       question_id, domain, GPT_Baseline, GPT_FewShot, GPT_CoT, GPT_ReACT,
       Grok_Baseline, Grok_FewShot, Grok_CoT, Grok_ReACT,
       Perplexity_Baseline, Perplexity_FewShot, Perplexity_CoT, Perplexity_ReACT
    
    2. 'ground_truth.csv' - Correct answers with structure:
       question_id, answer
    """
    
    print("=" * 80)
    print("PROMPT ENGINEERING COMPARISON & ANALYSIS")
    print("=" * 80)
    
    # Load data
    print("\n[1/5] Loading data...")
    try:
        df_results, df_truth = load_data('results.csv', 'ground_truth.csv')
        print(f"  ✓ Loaded {len(df_results)} questions")
        print(f"  ✓ Models: {MODELS}")
        print(f"  ✓ Techniques: {TECHNIQUES}")
    except FileNotFoundError as e:
        print(f"  ✗ Error: {e}")
        print("  Please ensure 'results.csv' and 'ground_truth.csv' exist")
        return
    
    # Create ground truth dict
    ground_truth_dict = dict(zip(df_truth['question_id'], df_truth['answer']))
    
    # Grade responses
    print("\n[2/5] Grading responses...")
    score_df = grade_responses(df_results, ground_truth_dict, method=GRADING_METHOD)
    print(f"  ✓ Used grading method: {GRADING_METHOD.upper()}")
    print(f"  ✓ Fuzzy threshold: {FUZZY_THRESHOLD}")
    
    # Calculate statistics
    print("\n[3/5] Calculating statistics...")
    stats = calculate_aggregate_stats(score_df)
    detailed_metrics = calculate_detailed_metrics(score_df)
    domain_perf = domain_performance(score_df)
    print(f"  ✓ Calculated {len(detailed_metrics)} model-technique combinations")
    
    # Print detailed results
    print("\n" + "=" * 80)
    print("DETAILED RESULTS")
    print("=" * 80)
    
    print("\n[ACCURACY BY TECHNIQUE]")
    for tech, acc in sorted(stats['by_technique'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {tech:15s}: {acc:.2%}")
    
    print("\n[ACCURACY BY MODEL]")
    for model, acc in sorted(stats['by_model'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {model:15s}: {acc:.2%}")
    
    print("\n[ACCURACY BY DOMAIN]")
    for domain, acc in sorted(stats['by_domain'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {domain:25s}: {acc:.2%}")
    
    print("\n[MODEL × TECHNIQUE MATRIX]")
    print(detailed_metrics.to_string(index=False))
    
    # Generate visualizations
    print("\n[4/5] Generating visualizations...")
    
    figs = {
        'accuracy_by_technique.png': plot_accuracy_by_technique(stats),
        'accuracy_by_model.png': plot_accuracy_by_model(stats),
        'model_technique_heatmap.png': plot_model_technique_heatmap(stats),
        'domain_performance.png': plot_domain_performance(domain_perf),
        'domain_aggregate.png': plot_domain_aggregate(domain_perf),
    }
    
    for filename, fig in figs.items():
        fig.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved {filename}")
        plt.close(fig)
    
    # Export results to CSV
    print("\n[5/5] Exporting results...")
    detailed_metrics.to_csv('detailed_metrics.csv', index=False)
    domain_perf.to_csv('domain_performance.csv', index=False)
    score_df.to_csv('graded_scores.csv', index=False)
    print("  ✓ Exported detailed_metrics.csv")
    print("  ✓ Exported domain_performance.csv")
    print("  ✓ Exported graded_scores.csv")
    
    # Summary report
    print("\n" + "=" * 80)
    print("SUMMARY REPORT")
    print("=" * 80)
    overall_accuracy = score_df.iloc[:, 2:].mean().mean()
    print(f"\nOverall Accuracy (All Models & Techniques): {overall_accuracy:.2%}")
    print(f"Grading Method: {GRADING_METHOD.upper()}")
    print(f"Questions Evaluated: {len(score_df)}")
    print(f"\nBest Technique: {max(stats['by_technique'], key=stats['by_technique'].get)}")
    print(f"Best Model: {max(stats['by_model'], key=stats['by_model'].get)}")
    print(f"Best Domain: {max(stats['by_domain'], key=stats['by_domain'].get)}")
    
    print("\n" + "=" * 80)
    print("✓ Analysis complete! Check generated files for detailed insights.")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()
