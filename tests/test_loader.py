import os
import pandas as pd
from llm_orchestration_hw6.data.loader import load_dataset

def test_load_dataset():
    # Create a dummy CSV file for testing
    data = {
        'id': ['1', '2'],
        'question': ['What is 2+2?', 'What is the capital of France?'],
        'ground_truth_answer': ['4', 'Paris']
    }
    df = pd.DataFrame(data)
    test_csv_path = 'test_dataset.csv'
    df.to_csv(test_csv_path, index=False)

    # Test loading the dataset
    dataset = load_dataset(test_csv_path)

    # Check that the dataset is a list of dictionaries
    assert isinstance(dataset, list)
    assert len(dataset) == 2
    assert isinstance(dataset[0], dict)

    # Check the content of the dataset
    assert dataset[0]['id'] == 1
    assert dataset[0]['question'] == 'What is 2+2?'
    assert dataset[0]['ground_truth_answer'] == '4'

    # Clean up the dummy CSV file
    os.remove(test_csv_path)
