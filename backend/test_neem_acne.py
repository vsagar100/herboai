"""Test if Neem for acne query now returns remedies"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set UTF-8 encoding for console output
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from init import create_app

# Initialize Flask app
app = create_app()

with app.app_context():
    print("\n=== TESTING: 'Neem for acne' ===\n")
    
    # Test using API endpoint
    with app.test_client() as client:
        response = client.post(
            "/api/query",
            json={"text": "Neem for acne", "lang": "en"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.get_json()
            
            print("Full response keys:", list(data.keys()))
            print("\nQuery:", data.get('query', 'N/A'))
            print("\nIntent:", data.get('intent', 'N/A'))
            print("\nDiseases Found:", data.get('diseases', []))
            print("\nPlants Found:", data.get('plants', []))
            print("\nPreparations Found:", len(data.get('preparations', [])))
            print("\nProvisional:", len(data.get('provisional', [])))
            
            print("\n" + "="*50)
            print("RESPONSE TEXT:")
            print("="*50)
            
            # Try different response keys
            response_text = (data.get('response') or 
                           data.get('answer') or 
                           data.get('text') or 
                           "No response field found")
            print(response_text)
            
            # Check if remedies are present
            response_lower = str(response_text).lower()
            has_remedies = any(keyword in response_lower for keyword in [
                "preparation", "remedy", "use", "apply", "treatment", "paste", "powder"
            ])
            
            print("\n" + "="*50)
            print(f"✓ Contains remedies: {has_remedies}")
            
            # Print full JSON for debugging
            print("\n" + "="*50)
            print("FULL JSON RESPONSE:")
            print("="*50)
            import json
            print(json.dumps(data, indent=2, default=str)[:1000])
        else:
            print(f"Error: {response.status_code}")
            print(response.get_json())
