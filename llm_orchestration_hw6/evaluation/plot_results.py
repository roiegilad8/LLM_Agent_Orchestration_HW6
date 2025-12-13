import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import typer
from typing_extensions import Annotated

app = typer.Typer(help="LLM Agent Orchestration plot generator.")

def plot_results_function(results_path: str):
    report_path = os.path.join(results_path, 'ANALYSIS_REPORT.md')
    with open(report_path, 'r') as f:
        lines = f.readlines()

    accuracy_data = []
    f1_data = []
    
    # Flag to indicate when we are in the data table
    in_data_section = False
    
    for line_num, line in enumerate(lines):
        if "| LLM | Metric |" in line: # Found the header for the new format
            in_data_section = True
            continue
        if in_data_section and "|---|" in line: # Skip the separator line
            continue
        if in_data_section and line.strip() == "": # End of data section
            in_data_section = False
            continue
        
        if in_data_section:
            parts = [p.strip() for p in line.split('|') if p.strip() != '']
            if len(parts) >= 6: # Expecting LLM, Metric, and 4 technique scores
                llm = parts[0]
                metric_type = parts[1]
                
                row_scores = {}
                techniques_list = ["baseline", "few_shot", "cot", "react"] # Order of techniques in the report
                
                for i, technique in enumerate(techniques_list):
                    score_str = parts[2 + i]
                    try:
                        score = float(score_str)
                    except ValueError:
                        score = None # Use None for "N/A" or other non-float values
                    row_scores[technique] = score
                
                if metric_type == "Accuracy":
                    for technique, score in row_scores.items():
                        if score is not None:
                            accuracy_data.append({'LLM': llm, 'Technique': technique, 'Accuracy': score})
                elif metric_type == "F1-Score":
                    for technique, score in row_scores.items():
                        if score is not None:
                            f1_data.append({'LLM': llm, 'Technique': technique, 'F1-Score': score})
    
    if not accuracy_data:
        print("No valid accuracy data found in ANALYSIS_REPORT.md for plotting.")
        return

    df_accuracy = pd.DataFrame(accuracy_data)

    plt.figure(figsize=(12, 6))
    sns.barplot(x='LLM', y='Accuracy', hue='Technique', data=df_accuracy)
    plt.title('Accuracy of Prompt Engineering Techniques by LLM')
    plt.ylim(0, 1)
    plt.ylabel('Accuracy')
    plt.xlabel('LLM')
    plt.legend(title='Technique')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()

    # Save the plot
    output_path = os.path.join(results_path, 'accuracy_comparison.png')
    plt.savefig(output_path)
    print(f'Plot saved to {output_path}')

    # Optionally, you can generate a plot for F1-Score as well
    if f1_data:
        df_f1 = pd.DataFrame(f1_data)
        plt.figure(figsize=(12, 6))
        sns.barplot(x='LLM', y='F1-Score', hue='Technique', data=df_f1)
        plt.title('F1-Score of Prompt Engineering Techniques by LLM')
        plt.ylim(0, 1)
        plt.ylabel('F1-Score')
        plt.xlabel('LLM')
        plt.legend(title='Technique')
        plt.grid(axis='y', linestyle='--')
        plt.tight_layout()
        output_path_f1 = os.path.join(results_path, 'f1_score_comparison.png')
        plt.savefig(output_path_f1)
        print(f'F1-Score Plot saved to {output_path_f1}')