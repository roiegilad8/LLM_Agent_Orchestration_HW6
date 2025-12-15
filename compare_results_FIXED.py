import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from pathlib import Path

# ============================================================================
# CREATE OUTPUT FOLDER
# ============================================================================

output_dir = Path('outputs')
output_dir.mkdir(exist_ok=True)
print(f"✓ Output folder: {output_dir}/")

# ============================================================================
# LOAD DATA
# ============================================================================

print("\nLoading data...")
results_df = pd.read_csv('results.csv')
ground_truth_df = pd.read_csv('ground_truth.csv')

print(f"  ✓ results.csv: {results_df.shape}")
print(f"  ✓ ground_truth.csv: {ground_truth_df.shape}")

# ============================================================================
# DEBUG: CHECK DATA
# ============================================================================

print("\n" + "="*80)
print("DEBUG: First 3 rows of ground_truth")
print("="*80)
print(ground_truth_df.head(3))

print("\n" + "="*80)
print("DEBUG: First 3 rows of results")
print("="*80)
print(results_df.head(3))

# ============================================================================
# IMPROVED GRADING: Clean & Compare
# ============================================================================

def clean_answer(answer):
    """Clean answer for comparison (strip spaces, lowercase)"""
    if pd.isna(answer) or answer is None:
        return ""
    return str(answer).strip().lower()

print("\n" + "="*80)
print("GRADING RESPONSES")
print("="*80)

# Get the model-technique columns
model_cols = [col for col in results_df.columns if col != 'question_id' and col != 'domain']
print(f"\nFound {len(model_cols)} model-technique combinations:")
for col in model_cols:
    print(f"  - {col}")

# Grade each response
graded = pd.DataFrame({
    'question_id': results_df['question_id']
})

# Add ground truth
graded['ground_truth'] = ground_truth_df['ground_truth_answer'].values

# Grade each model-technique combo
for col in model_cols:
    scores = []
    for idx in range(len(results_df)):
        pred = clean_answer(results_df[col].iloc[idx])
        true = clean_answer(graded['ground_truth'].iloc[idx])
        
        # IMPROVED MATCHING:
        # 1. Exact match (with cleaning)
        # 2. Substring match
        # 3. Partial word match
        
        if pred == true:
            score = 1.0
        elif pred in true or true in pred:
            score = 0.8  # Partial match
        elif any(word in true for word in pred.split() if len(word) > 2):
            score = 0.5  # Some words match
        else:
            score = 0.0
        
        scores.append(score)
    
    graded[col] = scores

print(f"\n✓ Graded all responses")

# Save graded scores
graded.to_csv(output_dir / 'graded_scores.csv', index=False)
print(f"✓ graded_scores.csv saved to outputs/")

# ============================================================================
# CALCULATE METRICS
# ============================================================================

print("\n" + "="*80)
print("CALCULATING METRICS")
print("="*80)

# Extract model and technique from column names
metrics_list = []

for col in model_cols:
    parts = col.split('_')
    if len(parts) >= 2:
        model = parts[0]  # GPT, Grok, Perplexity
        technique = '_'.join(parts[1:])  # Baseline, FewShot, CoT, ReACT
    else:
        model = col
        technique = "Unknown"
    
    scores = graded[col]
    
    metrics_list.append({
        'Model': model,
        'Technique': technique,
        'Column': col,
        'Accuracy': scores.mean(),
        'Std_Dev': scores.std(),
        'Min': scores.min(),
        'Max': scores.max(),
        'Total_Correct': (scores == 1.0).sum(),
        'Partial_Correct': ((scores > 0) & (scores < 1.0)).sum(),
        'Total_Wrong': (scores == 0.0).sum()
    })

metrics_df = pd.DataFrame(metrics_list)
metrics_df = metrics_df.sort_values('Accuracy', ascending=False)

# Save metrics
metrics_df.to_csv(output_dir / 'detailed_metrics.csv', index=False)
print(f"✓ detailed_metrics.csv saved to outputs/")

# ============================================================================
# CONSOLE OUTPUT
# ============================================================================

print("\n" + "="*80)
print("ACCURACY BY TECHNIQUE")
print("="*80)

technique_stats = metrics_df.groupby('Technique')[['Accuracy']].agg(['mean', 'std']).round(4)
technique_stats.columns = ['Mean_Accuracy', 'Std_Dev']
technique_stats = technique_stats.sort_values('Mean_Accuracy', ascending=False)
print(technique_stats)

print("\n" + "="*80)
print("ACCURACY BY MODEL")
print("="*80)

model_stats = metrics_df.groupby('Model')[['Accuracy']].agg(['mean', 'std']).round(4)
model_stats.columns = ['Mean_Accuracy', 'Std_Dev']
model_stats = model_stats.sort_values('Mean_Accuracy', ascending=False)
print(model_stats)

print("\n" + "="*80)
print("TOP 5 BEST COMBINATIONS")
print("="*80)

top_5 = metrics_df[['Model', 'Technique', 'Accuracy', 'Total_Correct']].head(5)
for idx, row in top_5.iterrows():
    print(f"  {row['Model']:12} + {row['Technique']:10} = {row['Accuracy']:.2%} ({int(row['Total_Correct'])}/100 correct)")

print("\n" + "="*80)
print("BOTTOM 5 WORST COMBINATIONS")
print("="*80)

bottom_5 = metrics_df[['Model', 'Technique', 'Accuracy', 'Total_Correct']].tail(5)
for idx, row in bottom_5.iterrows():
    print(f"  {row['Model']:12} + {row['Technique']:10} = {row['Accuracy']:.2%} ({int(row['Total_Correct'])}/100 correct)")

# ============================================================================
# GENERATE VISUALIZATIONS
# ============================================================================

print("\n" + "="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

# 1. Accuracy by Technique
fig, ax = plt.subplots(figsize=(10, 6))
technique_data = metrics_df.groupby('Technique')['Accuracy'].mean().sort_values(ascending=False)
technique_data.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
ax.set_title('Accuracy by Prompting Technique', fontsize=14, fontweight='bold')
ax.set_ylabel('Accuracy', fontsize=12)
ax.set_xlabel('Technique', fontsize=12)
ax.set_ylim([0, 1])
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_dir / 'accuracy_by_technique.png', dpi=300, bbox_inches='tight')
print("✓ accuracy_by_technique.png")
plt.close()

# 2. Accuracy by Model
fig, ax = plt.subplots(figsize=(10, 6))
model_data = metrics_df.groupby('Model')['Accuracy'].mean().sort_values(ascending=False)
model_data.plot(kind='bar', ax=ax, color='lightcoral', edgecolor='black')
ax.set_title('Accuracy by LLM Model', fontsize=14, fontweight='bold')
ax.set_ylabel('Accuracy', fontsize=12)
ax.set_xlabel('Model', fontsize=12)
ax.set_ylim([0, 1])
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_dir / 'accuracy_by_model.png', dpi=300, bbox_inches='tight')
print("✓ accuracy_by_model.png")
plt.close()

# 3. Heatmap: Model vs Technique
pivot_data = metrics_df.pivot_table(values='Accuracy', index='Model', columns='Technique')
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(pivot_data, annot=True, fmt='.2%', cmap='RdYlGn', ax=ax, cbar_kws={'label': 'Accuracy'})
ax.set_title('Accuracy by Model & Technique', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(output_dir / 'model_technique_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ model_technique_heatmap.png")
plt.close()

# 4. Detailed Bar Chart (All 12 combos)
fig, ax = plt.subplots(figsize=(14, 6))
combo_labels = metrics_df['Model'] + '\n' + metrics_df['Technique']
colors = ['green' if x > 0.5 else 'orange' if x > 0.3 else 'red' for x in metrics_df['Accuracy']]
ax.bar(range(len(metrics_df)), metrics_df['Accuracy'], color=colors, edgecolor='black')
ax.set_xticks(range(len(metrics_df)))
ax.set_xticklabels(combo_labels, rotation=45, ha='right')
ax.set_ylabel('Accuracy', fontsize=12)
ax.set_title('All 12 Model-Technique Combinations', fontsize=14, fontweight='bold')
ax.set_ylim([0, 1])
ax.axhline(y=metrics_df['Accuracy'].mean(), color='blue', linestyle='--', label='Mean')
ax.legend()
plt.tight_layout()
plt.savefig(output_dir / 'all_combinations.png', dpi=300, bbox_inches='tight')
print("✓ all_combinations.png")
plt.close()

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("✓ ANALYSIS COMPLETE!")
print("="*80)
print(f"\nAll results saved to: {output_dir}/")
print("\nFiles created:")
print("  ✓ graded_scores.csv - Individual question scores")
print("  ✓ detailed_metrics.csv - Stats per combination")
print("  ✓ accuracy_by_technique.png - Technique comparison")
print("  ✓ accuracy_by_model.png - Model comparison")
print("  ✓ model_technique_heatmap.png - Combined heatmap")
print("  ✓ all_combinations.png - All 12 combos bar chart")
print("\n" + "="*80)
