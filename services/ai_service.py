import requests
import json

class AIService:
    def __init__(self):
        self.base_url = "http://localhost:11434/api"

    def generate_response(self, prompt):
        try:
            response = requests.post(
                f"{self.base_url}/generate",
                json={
                    "model": "mistral",
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            print(f"Error calling Ollama API: {str(e)}")
            return None