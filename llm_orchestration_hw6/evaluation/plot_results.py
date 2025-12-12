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

    data = []
    # Find the table header line
    header_found = False
    for line in lines:
        if "| LLM | Baseline |" in line:
            header_found = True
            continue
        if header_found and "|---|" not in line: # Skip the separator line
            parts = [p.strip() for p in line.split('|') if p.strip() != '']
            if len(parts) >= 5:  # Ensure enough parts for all techniques + LLM name
                llm = parts[0]
                try:
                    accuracy_baseline = float(parts[1])
                    accuracy_few_shot = float(parts[2])
                    accuracy_cot = float(parts[3])
                    accuracy_react = float(parts[4])
                    data.append({'LLM': llm, 'Technique': 'baseline', 'Accuracy': accuracy_baseline})
                    data.append({'LLM': llm, 'Technique': 'few_shot', 'Accuracy': accuracy_few_shot})
                    data.append({'LLM': llm, 'Technique': 'cot', 'Accuracy': accuracy_cot})
                    data.append({'LLM': llm, 'Technique': 'react', 'Accuracy': accuracy_react})
                except ValueError:
                    continue # Skip lines where accuracy is not a valid float
            elif header_found and line.strip() == "": # Stop at the first empty line after the header
                break
    
    if not data:
        print("No valid data found in ANALYSIS_REPORT.md for plotting.")
        return

    df = pd.DataFrame(data)

    plt.figure(figsize=(12, 6))
    sns.barplot(x='LLM', y='Accuracy', hue='Technique', data=df)
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

@app.command()
def generate_plot(
    results_path: Annotated[str, typer.Option(help="Path to the evaluation results.")] = "results",
):
    """
    Generate a plot from the analysis results.
    """
    plot_results_function(results_path)
    
if __name__ == "__main__":
    app()