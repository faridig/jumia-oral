import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Configure OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Directories
DATA_DIR = Path("data/raw/markdown/notebooks")
OUTPUT_FILE = Path("tests/gold_dataset.json")

def extract_product_data(file_path):
    """
    Extracts core metadata and category specs from the markdown frontmatter.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Simple markdown frontmatter parsing
    parts = content.split("---")
    if len(parts) < 3:
        return None
    
    try:
        data = json.loads(parts[1])
        return {
            "name": data.get("core_metadata", {}).get("name"),
            "specs": data.get("category_specs", {}),
            "price": data.get("core_metadata", {}).get("current_price"),
            "currency": data.get("core_metadata", {}).get("currency"),
            "brand": data.get("core_metadata", {}).get("brand")
        }
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing JSON frontmatter in {file_path}: {e}")
        return None

def generate_qa_pair(product_data):
    """
    Calls GPT-4o-mini to generate a (Question, Ground_Truth) pair based on product data.
    """
    if not product_data:
        return None
    
    prompt = f"""Tu es un expert Jumia. Voici les spécifications techniques d'un PC portable en format JSON.
Génère une question réaliste qu'un utilisateur marocain pourrait poser sur ce produit et sa réponse exacte basée strictement sur les données fournies.
La réponse doit être précise et concise.

Produit: {json.dumps(product_data, indent=2, ensure_ascii=False)}

Génère le résultat en format JSON avec les clés suivantes :
- question: La question utilisateur (en français).
- ground_truth: La réponse exacte.
- context: Un résumé des specs utilisées pour répondre.
- product_name: Le nom complet du produit.

Réponds UNIQUEMENT avec le bloc JSON."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un générateur de données de test pour un chatbot e-commerce."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        
        content = response.choices[0].message.content
        if not content:
            return None
        result = json.loads(content)
        return result
    except Exception as e:
        print(f"Error generating QA pair for {product_data.get('name')}: {e}")
        return None

def main():
    print(f"Starting Gold Dataset generation from {DATA_DIR}...")
    
    md_files = list(DATA_DIR.glob("*.md"))
    print(f"Found {len(md_files)} product files.")
    
    gold_dataset = []
    
    # For Sprint 11, we need at least 20 test cases.
    # We will process all files (26 files available).
    
    for i, file_path in enumerate(md_files):
        print(f"[{i+1}/{len(md_files)}] Processing {file_path.name}...")
        
        product_data = extract_product_data(file_path)
        if product_data:
            qa_pair = generate_qa_pair(product_data)
            if qa_pair:
                gold_dataset.append(qa_pair)
        
        # Stop early if we have enough? No, let's process all to have a better dataset.
        # But for the sake of speed in this task, I'll make sure we have at least 20.

    if len(gold_dataset) > 0:
        # Ensure tests/ directory exists
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(gold_dataset, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully generated {len(gold_dataset)} test cases in {OUTPUT_FILE}.")
    else:
        print("No test cases generated.")

if __name__ == "__main__":
    main()
