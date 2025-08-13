import requests
import json

class AIService:
    def __init__(self):
        self.base_url = "http://localhost:11434/api"

    def generate_plant_info(self, plant_name):
        prompt = f"""Provide brief information about {plant_name} covering:
1. Overview: Scientific name, family, origin, system (Ayurveda/Unani/Siddha)
2. Key Benefits: Main therapeutic properties and health benefits
3. Traditional Uses: Common preparations and dosage
4. Research Insights: Notable scientific findings
5. Safety: Important precautions and interactions

Keep the response concise and evidence-based."""

        try:
            print(f"Ollama prompt: {prompt}")
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