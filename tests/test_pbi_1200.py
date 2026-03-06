import json
import os

def test_gold_dataset_exists():
    assert os.path.exists("tests/gold_dataset.json")

def test_gold_dataset_structure():
    with open("tests/gold_dataset.json", "r") as f:
        data = json.load(f)
    
    assert isinstance(data, list)
    assert len(data) >= 20
    
    for entry in data:
        assert "question" in entry
        assert "context" in entry
        assert "ground_truth" in entry
        assert "product_name" in entry  # Optional but good for traceability
