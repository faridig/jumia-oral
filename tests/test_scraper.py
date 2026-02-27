import os
import json
import pytest
from pydantic import ValidationError
from src.scraper import ProductExtractionSchema, save_to_markdown

def test_product_extraction_schema_v1_1():
    # Test valid data with 'images' list
    valid_data = {
        "name": "Test Product",
        "current_price": 100.0,
        "old_price": 120.0,
        "images": ["http://example.com/main.jpg", "http://example.com/thumb1.jpg"],
        "url": "http://example.com/product",
        "technical_specs": {"Processeur": "i7"},
        "rating": 4.5,
        "review_count": 10,
        "review_summary": "Good product"
    }
    product = ProductExtractionSchema(**valid_data)
    assert product.name == "Test Product"
    assert product.images == ["http://example.com/main.jpg", "http://example.com/thumb1.jpg"]
    
    # Test missing images (should fail as it's required)
    invalid_data = valid_data.copy()
    del invalid_data["images"]
    with pytest.raises(ValidationError):
        ProductExtractionSchema(**invalid_data)

    # Test old 'image_url' (should fail as we replaced it)
    old_data = valid_data.copy()
    del old_data["images"]
    old_data["image_url"] = "http://example.com/main.jpg"
    with pytest.raises(ValidationError):
        ProductExtractionSchema(**old_data)

def test_save_to_markdown_v1_1(tmp_path, monkeypatch):
    # Mock the base_dir to use a temporary directory
    mock_base_dir = tmp_path / "data/raw/markdown/informatique"
    mock_base_dir.mkdir(parents=True)
    
    # Monkeypatch the base_dir in save_to_markdown if it was a constant, 
    # but it's defined inside the function. I'll modify the function to accept base_dir or 
    # just rely on the fact that I can check the file content after creation.
    # Wait, I'll modify src/scraper.py first and then run this test.
    
    product = {
        "name": "Test Product Gallery",
        "current_price": 100.0,
        "old_price": 120.0,
        "images": ["http://example.com/main.jpg", "http://example.com/thumb1.jpg", "http://example.com/thumb2.jpg"],
        "url": "http://example.com/product",
        "technical_specs": {"Processeur": "i7"},
        "trust_score": 4.5,
        "rating": 4.5,
        "review_count": 10,
        "review_summary": "Good product summary"
    }
    
    # We need to make sure save_to_markdown uses our tmp_path
    # I'll modify src/scraper.py to use an environment variable for the base directory if it exists
    monkeypatch.setenv("SCRAPER_BASE_DIR", str(mock_base_dir))
    
    from src.scraper import save_to_markdown
    
    filepath = save_to_markdown(product)
    
    assert os.path.exists(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Check if main image is present and large
    assert "![Image Principale](http://example.com/main.jpg)" in content
    # Check if gallery images are present
    assert "![Image 1](http://example.com/thumb1.jpg)" in content
    assert "![Image 2](http://example.com/thumb2.jpg)" in content
    # Check frontmatter
    assert '"images": [' in content
    assert '"http://example.com/main.jpg"' in content
