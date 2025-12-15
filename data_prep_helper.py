#!/usr/bin/env python3
"""
Data Preparation Helper for Prompt Engineering Comparison
Helps convert raw model outputs and ground truth into the expected CSV format
"""

import pandas as pd
import json
import os
from pathlib import Path

# ============================================================================
# HELPER FUNCTION 1: Build results.csv from separate model files
# ============================================================================

def build_results_csv_from_files(
    gpt_file, grok_file, perplexity_file, 
    output_path='results.csv',
    domain_mapping=None
):
    """
    Combine separate model output files into a single results.csv
    
    Expected input format (one per model file):
    - JSON: {"Q1": {"Baseline": "answer", "FewShot": "answer", ...}, ...}
    - CSV: question_id, Baseline, FewShot, CoT, ReACT
    - TXT: One line per question, format: Q#_TECHNIQUE: answer
    
    Args:
        gpt_file: Path to GPT responses
        grok_file: Path to Grok responses
        perplexity_file: Path to Perplexity responses
        output_path: Where to save combined results.csv
        domain_mapping: Optional dict {question_id: domain} for custom domains
    """
    
    TECHNIQUES = ['Baseline', 'FewShot', 'CoT', 'ReACT']
    MODELS = ['GPT', 'Grok', 'Perplexity']
    
    # Default domain mapping (7 domains)
    if domain_mapping is None:
        domain_mapping = {}
        domains_ranges = {
            'Arithmetic': (1, 7),
            'Logic': (16, 30),
            'Linguistics': (31, 44),
            'Programming': (45, 58),
            'General_Knowledge': (59, 72),
            'Design_Lateral': (73, 86),
            'Applied_Integration': (87, 100)
        }
        for domain, (start, end) in domains_ranges.items():
            for q_id in range(start, end + 1):
                domain_mapping[q_id] = domain
    
    # Initialize results dataframe
    results = {'question_id': [], 'domain': []}
    for model in MODELS:
        for technique in TECHNIQUES:
            results[f'{model}_{technique}'] = []
    
    # Load and parse each model's file
    model_data = {}
    
    print("[Loading Model Files]")
    
    # Load GPT
    print(f"  Loading {gpt_file}...")
    gpt_data = _load_responses(gpt_file, TECHNIQUES)
    model_data['GPT'] = gpt_data
    
    # Load Grok
    print(f"  Loading {grok_file}...")
    grok_data = _load_responses(grok_file, TECHNIQUES)
    model_data['Grok'] = grok_data
    
    # Load Perplexity
    print(f"  Loading {perplexity_file}...")
    perplexity_data = _load_responses(perplexity_file, TECHNIQUES)
    model_data['Perplexity'] = perplexity_data
    
    # Combine into single dataframe
    print("\n[Combining Data]")
    for q_id in range(1, 101):
        results['question_id'].append(q_id)
        results['domain'].append(domain_mapping.get(q_id, 'Unknown'))
        
        for model in MODELS:
            for technique in TECHNIQUES:
                answer = model_data[model].get(q_id, {}).get(technique, '')
                results[f'{model}_{technique}'].append(answer)
    
    # Save to CSV
    df_results = pd.DataFrame(results)
    df_results.to_csv(output_path, index=False)
    print(f"  ✓ Saved to {output_path}")
    
    return df_results


def _load_responses(filepath, techniques):
    """
    Parse response file into dict format {question_id: {technique: answer}}
    Supports JSON, CSV, and TXT formats
    """
    
    filepath = Path(filepath)
    data = {}
    
    if filepath.suffix.lower() == '.json':
        # JSON format: {"Q1": {"Baseline": "answer", ...}, ...}
        with open(filepath, 'r') as f:
            raw = json.load(f)
        
        for q_str, techniques_dict in raw.items():
            q_id = int(q_str.replace('Q', ''))
            data[q_id] = {}
            for tech in techniques:
                data[q_id][tech] = techniques_dict.get(tech, '')
    
    elif filepath.suffix.lower() == '.csv':
        # CSV format: question_id, Baseline, FewShot, CoT, ReACT
        df = pd.read_csv(filepath)
        for _, row in df.iterrows():
            q_id = int(row['question_id'])
            data[q_id] = {}
            for tech in techniques:
                data[q_id][tech] = row.get(tech, '')
    
    elif filepath.suffix.lower() == '.txt':
        # TXT format: Q1_Baseline: answer\nQ1_FewShot: answer\n...
        with open(filepath, 'r') as f:
            for line in f:
                if ':' not in line:
                    continue
                label, answer = line.split(':', 1)
                parts = label.strip().split('_')
                q_id = int(parts[0].replace('Q', ''))
                tech = parts[1] if len(parts) > 1 else ''
                
                if q_id not in data:
                    data[q_id] = {}
                data[q_id][tech] = answer.strip()
    
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")
    
    return data


# ============================================================================
# HELPER FUNCTION 2: Build ground_truth.csv from various formats
# ============================================================================

def build_ground_truth_csv(
    source_file, 
    output_path='ground_truth.csv',
    question_column='question_id',
    answer_column='answer'
):
    """
    Build ground_truth.csv from various source formats
    
    Args:
        source_file: Path to source file (CSV, JSON, TXT)
        output_path: Where to save ground_truth.csv
        question_column: Name of question ID column
        answer_column: Name of answer column
    """
    
    source = Path(source_file)
    print(f"\n[Processing Ground Truth from {source.name}]")
    
    if source.suffix.lower() == '.csv':
        df = pd.read_csv(source)
        if question_column in df.columns and answer_column in df.columns:
            truth = df[[question_column, answer_column]].copy()
            truth.columns = ['question_id', 'answer']
        else:
            print(f"  ✗ Columns '{question_column}' or '{answer_column}' not found")
            return None
    
    elif source.suffix.lower() == '.json':
        with open(source, 'r') as f:
            raw = json.load(f)
        
        truth_data = []
        for q_id in range(1, 101):
            q_key = f'Q{q_id}' if isinstance(raw.get(f'Q{q_id}'), dict) else str(q_id)
            answer = raw.get(q_key, '')
            if isinstance(answer, dict):
                answer = answer.get('answer', '')
            truth_data.append({'question_id': q_id, 'answer': answer})
        
        truth = pd.DataFrame(truth_data)
    
    elif source.suffix.lower() == '.txt':
        # Format: Q1: answer\nQ2: answer\n...
        truth_data = []
        with open(source, 'r') as f:
            for line in f:
                if ':' not in line:
                    continue
                parts = line.split(':', 1)
                q_id_str = parts[0].strip().replace('Q', '')
                try:
                    q_id = int(q_id_str)
                    answer = parts[1].strip()
                    truth_data.append({'question_id': q_id, 'answer': answer})
                except ValueError:
                    continue
        
        truth = pd.DataFrame(truth_data)
    
    else:
        raise ValueError(f"Unsupported file format: {source.suffix}")
    
    # Ensure question_id is sequential 1-100
    truth = truth[truth['question_id'].between(1, 100)].copy()
    truth = truth.sort_values('question_id').reset_index(drop=True)
    
    truth.to_csv(output_path, index=False)
    print(f"  ✓ Saved {len(truth)} answers to {output_path}")
    
    return truth


# ============================================================================
# HELPER FUNCTION 3: Validate and repair CSV files
# ============================================================================

def validate_results_csv(filepath):
    """
    Validate that results.csv has correct structure and no missing data
    """
    
    print(f"\n[Validating {filepath}]")
    
    df = pd.read_csv(filepath)
    
    TECHNIQUES = ['Baseline', 'FewShot', 'CoT', 'ReACT']
    MODELS = ['GPT', 'Grok', 'Perplexity']
    
    # Check basic structure
    expected_cols = {'question_id', 'domain'}
    for model in MODELS:
        for tech in TECHNIQUES:
            expected_cols.add(f'{model}_{tech}')
    
    actual_cols = set(df.columns)
    
    missing_cols = expected_cols - actual_cols
    if missing_cols:
        print(f"  ✗ Missing columns: {missing_cols}")
        return False
    
    # Check for missing values
    null_counts = df.isnull().sum()
    if null_counts.any():
        print(f"  ⚠ Warning: Found {null_counts.sum()} missing values")
        print(f"    {null_counts[null_counts > 0].to_dict()}")
    
    # Check question ID range
    if not df['question_id'].min() == 1 or df['question_id'].max() != 100:
        print(f"  ✗ Question IDs out of range: {df['question_id'].min()}-{df['question_id'].max()}")
        return False
    
    print(f"  ✓ Valid structure: {len(df)} questions × {len(expected_cols)} total columns")
    return True


def validate_ground_truth_csv(filepath):
    """
    Validate that ground_truth.csv has correct structure
    """
    
    print(f"\n[Validating {filepath}]")
    
    df = pd.read_csv(filepath)
    
    # Check columns
    if 'question_id' not in df.columns or 'answer' not in df.columns:
        print("  ✗ Missing required columns: question_id, answer")
        return False
    
    # Check for missing values
    if df.isnull().any().any():
        print(f"  ✗ Found missing values in ground truth")
        return False
    
    # Check question ID range
    if len(df) != 100 or df['question_id'].min() != 1 or df['question_id'].max() != 100:
        print(f"  ✗ Must have exactly 100 questions (Q1-Q100)")
        return False
    
    print(f"  ✓ Valid: {len(df)} questions with answers")
    return True


# ============================================================================
# MAIN EXECUTION EXAMPLE
# ============================================================================

def main():
    """
    Example usage - customize based on your file structure
    """
    
    print("=" * 80)
    print("PROMPT ENGINEERING DATA PREPARATION")
    print("=" * 80)
    
    # Example: Combine model responses from separate files
    print("\n[STEP 1: Combine Model Responses]")
    print("If you have separate files for each model, run:")
    print("""
    from data_prep import build_results_csv_from_files
    
    df = build_results_csv_from_files(
        gpt_file='gpt_responses.csv',       # or .json or .txt
        grok_file='grok_responses.csv',
        perplexity_file='perplexity_responses.csv',
        output_path='results.csv'
    )
    """)
    
    # Example: Build ground truth
    print("\n[STEP 2: Build Ground Truth]")
    print("If you have a file with correct answers, run:")
    print("""
    from data_prep import build_ground_truth_csv
    
    df = build_ground_truth_csv(
        source_file='your_ground_truth_file.csv',
        output_path='ground_truth.csv',
        question_column='id',        # Your column name for Q ID
        answer_column='correct'      # Your column name for answer
    )
    """)
    
    # Validation
    print("\n[STEP 3: Validate Generated CSVs]")
    print("After generation, validate your files:")
    print("""
    from data_prep import validate_results_csv, validate_ground_truth_csv
    
    if validate_results_csv('results.csv') and validate_ground_truth_csv('ground_truth.csv'):
        print("✓ Ready to run compare_results.py!")
    """)
    
    print("\n" + "=" * 80)
    print("Files will be created in CSV format for use with compare_results.py")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()
