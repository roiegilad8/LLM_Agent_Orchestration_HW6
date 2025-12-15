import pandas as pd
import os

# ============================================================================
# CONFIG: YOUR EXACT FILENAMES
# ============================================================================

GPT_FILES = {
    'Baseline': 'results/GPT/baseline_prompts_GPT.txt',
    'FewShot': 'results/GPT/few_shot_prompts_GPT.txt',
    'CoT': 'results/GPT/cot_prompts_GPT.txt',
    'ReACT': 'results/GPT/react_prompts_GPT.txt'
}

GROK_FILES = {
    'Baseline': 'results/Grok/baseline_prompts_grok.txt',
    'FewShot': 'results/Grok/few_shot_prompts_grok.txt',
    'CoT': 'results/Grok/cot_prompts_grok.txt',
    'ReACT': 'results/Grok/react_prompts_grok.txt'
}

PERPLEXITY_FILES = {
    'Baseline': 'results/Perplexity/baseline_prompts_perplexity.txt',
    'FewShot': 'results/Perplexity/few_shot_prompts_perplexity.txt',
    'CoT': 'results/Perplexity/cot_prompts_perplexity.txt',
    'ReACT': 'results/Perplexity/react_prompts_perplexity.txt'
}

GROUND_TRUTH_FILE = 'ground_truth.csv'
GROUND_TRUTH_Q_COLUMN = 'question_id'
GROUND_TRUTH_A_COLUMN = 'answer'

RESPONSE_COLUMN = 'answer'

# ============================================================================
# FUNCTION: Load responses from one file
# ============================================================================

def load_responses(filepath, response_column='answer'):
    """Load responses from CSV/JSON/TXT file"""
    try:
        if filepath.endswith('.json'):
            df = pd.read_json(filepath)
        elif filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filepath.endswith('.txt'):
            df = pd.read_csv(filepath, sep='\t')
        else:
            raise ValueError(f"Unsupported format: {filepath}")
        
        # Extract just the response column if it exists
        if response_column in df.columns:
            return df[response_column].tolist()
        else:
            # If no specific column, take the last column
            return df.iloc[:, -1].tolist()
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return None

# ============================================================================
# MAIN: Combine all 12 files into results.csv (WITH FIX FOR DIFFERENT LENGTHS)
# ============================================================================

print("\n" + "="*80)
print("BUILDING RESULTS.CSV FROM 12 FILES")
print("="*80)

# Step 1: Load all 12 files
print("\nLoading responses...")

gpt_data = {}
grok_data = {}
perplexity_data = {}

# Load GPT
for technique, filepath in GPT_FILES.items():
    print(f"  Loading GPT {technique}... ", end='')
    responses = load_responses(filepath, RESPONSE_COLUMN)
    if responses:
        gpt_data[technique] = responses
        print(f"✓ ({len(responses)} responses)")
    else:
        print("❌ FAILED")

# Load Grok
for technique, filepath in GROK_FILES.items():
    print(f"  Loading Grok {technique}... ", end='')
    responses = load_responses(filepath, RESPONSE_COLUMN)
    if responses:
        grok_data[technique] = responses
        print(f"✓ ({len(responses)} responses)")
    else:
        print("❌ FAILED")

# Load Perplexity
for technique, filepath in PERPLEXITY_FILES.items():
    print(f"  Loading Perplexity {technique}... ", end='')
    responses = load_responses(filepath, RESPONSE_COLUMN)
    if responses:
        perplexity_data[technique] = responses
        print(f"✓ ({len(responses)} responses)")
    else:
        print("❌ FAILED")

# Step 2: Create results DataFrame (FIX: TRIM ALL RESPONSES TO 100 ROWS)
print("\nCombining into results.csv...")

# Base: question_id and domain
results = pd.DataFrame({
    'question_id': range(1, 101),  # 1-100
    'domain': [''] * 100
})

# Add all responses - TRIM to 100 rows to match
for technique in ['Baseline', 'FewShot', 'CoT', 'ReACT']:
    if technique in gpt_data:
        # Trim to 100 rows
        trimmed = gpt_data[technique][:100]
        # Pad with NaN if needed
        if len(trimmed) < 100:
            trimmed = trimmed + [None] * (100 - len(trimmed))
        results[f'GPT_{technique}'] = trimmed
        
    if technique in grok_data:
        trimmed = grok_data[technique][:100]
        if len(trimmed) < 100:
            trimmed = trimmed + [None] * (100 - len(trimmed))
        results[f'Grok_{technique}'] = trimmed
        
    if technique in perplexity_data:
        trimmed = perplexity_data[technique][:100]
        if len(trimmed) < 100:
            trimmed = trimmed + [None] * (100 - len(trimmed))
        results[f'Perplexity_{technique}'] = trimmed

# Save results.csv
results.to_csv('results.csv', index=False)
print(f"✓ results.csv created ({results.shape[0]} rows × {results.shape[1]} columns)")

# Step 3: Build ground_truth.csv
print("\nBuilding ground_truth.csv...")

try:
    ground_truth_df = pd.read_csv(GROUND_TRUTH_FILE)
    
    # Extract just Q ID and answer
    truth = pd.DataFrame({
        'question_id': ground_truth_df[GROUND_TRUTH_Q_COLUMN],
        'answer': ground_truth_df[GROUND_TRUTH_A_COLUMN]
    })
    
    truth.to_csv('ground_truth.csv', index=False)
    print(f"✓ ground_truth.csv created ({truth.shape[0]} rows)")
except Exception as e:
    print(f"❌ Error creating ground_truth.csv: {e}")

# Step 4: Summary
print("\n" + "="*80)
print("✓ DONE!")
print("="*80)
print(f"\nResults:")
print(f"  ✓ results.csv (100 questions × 12 model-technique combos)")
print(f"  ✓ ground_truth.csv (100 correct answers)")
print(f"\n⚠️  NOTE: Files were trimmed/padded to 100 rows")
print(f"\nNext step: python compare_results.py")
print("\n" + "="*80)
