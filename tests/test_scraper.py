import os
import json
import pytest
from pydantic import ValidationError
from src.models import CategoryAgnosticProduct, SentimentAxis
from src.scraper import save_to_markdown

def test_category_agnostic_product_schema_v2():
    # Test valid data for PBI-120
    valid_data = {
        "core_metadata": {
            "name": "Laptop XPS 13",
            "current_price": 15000.0,
            "old_price": 17000.0,
            "brand": "Dell",
            "images": ["http://example.com/xps13.jpg"],
            "url": "http://example.com/xps13",
            "category": "Informatique",
            "rating": 4.8,
            "review_count": 50
        },
        "category_specs": {
            "RAM": "16 GB",
            "Storage": "512 GB SSD",
            "CPU": "Intel i7"
        },
        "sentiment_analysis": [
            {"axis": "Performance", "score": 9.0, "rationale": "Very fast"},
            {"axis": "Design", "score": 9.5, "rationale": "Sleek and light"},
            {"axis": "Prix", "score": 7.0, "rationale": "Premium price"}
        ],
        "value_for_money_score": 8.5,
        "trust_score": 4.2,
        "raw_review_summary": "Excellent laptop for professionals."
    }
    product = CategoryAgnosticProduct(**valid_data)
    assert product.core_metadata.name == "Laptop XPS 13"
    assert product.category_specs["RAM"] == "16 GB"
    assert len(product.sentiment_analysis) == 3
    assert product.sentiment_analysis[0].axis == "Performance"

    # Test invalid data (missing core_metadata)
    invalid_data = valid_data.copy()
    del invalid_data["core_metadata"]
    with pytest.raises(ValidationError):
        CategoryAgnosticProduct(**invalid_data)

def test_save_to_markdown_v2(tmp_path, monkeypatch):
    mock_base_dir = tmp_path / "data/raw/markdown"
    mock_base_dir.mkdir(parents=True)
    monkeypatch.setenv("SCRAPER_BASE_DIR", str(mock_base_dir))
    
    product_data = {
        "core_metadata": {
            "name": "Crème Hydratante",
            "current_price": 200.0,
            "category": "Cosmétique",
            "images": ["http://example.com/cream.jpg"],
            "url": "http://example.com/cream"
        },
        "category_specs": {
            "Contenance": "50 ml"
        },
        "sentiment_analysis": [
            {"axis": "Efficacité", "score": 8.0, "rationale": "Bonne hydratation"}
        ],
        "value_for_money_score": 8.0,
        "trust_score": 4.0
    }
    
    filepath = save_to_markdown(product_data)
    
    assert os.path.exists(filepath)
    assert "cosmétique" in filepath.lower()
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    assert "# Crème Hydratante" in content
    assert "![Image Principale](http://example.com/cream.jpg)" in content
    assert "50 ml" in content
    assert "Efficacité" in content
    assert "8.0/10" in content
