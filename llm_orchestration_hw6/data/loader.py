import pandas as pd
from typing import List, Dict

def load_dataset(file_path: str) -> List[Dict]:
    """
    Loads the ground truth dataset from a CSV file.

    Args:
        file_path: The path to the CSV file.

    Returns:
        A list of dictionaries, where each dictionary represents a question.
    """
    df = pd.read_csv(file_path)
    return df.to_dict('records')
