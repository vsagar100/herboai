import requests
import json
import re
from typing import Optional
from .settings import settings
from loguru import logger

class OllamaLLM:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.generate_url = f"{base_url}/api/generate"
        self.models_url = f"{base_url}/api/tags"
        
        # Test connection
        self._test_connection()
    
    def _test_connection(self):
        """Test if Ollama is running and accessible"""
        try:
            response = requests.get(self.models_url, timeout=5)
            response.raise_for_status()
            logger.info("✅ Successfully connected to Ollama")
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Cannot connect to Ollama at {self.base_url}")
            logger.error(f"   Make sure Ollama is running: ollama serve")
            raise ConnectionError(f"Ollama connection failed: {e}")
    
    def list_models(self):
        """List available models in Ollama"""
        try:
            response = requests.get(self.models_url)
            response.raise_for_status()
            models = response.json()
            return [model['name'] for model in models.get('models', [])]
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
    
    def generate(self, prompt: str, max_tokens: int | None = None, temperature: float | None = None) -> str:
        """Generate response using Ollama API"""
        
        # Prepare request data
        data = {
            'model': settings.OLLAMA_MODEL_NAME,
            'prompt': prompt,
            'stream': False,  # Get complete response at once
            'options': {
                'temperature': temperature or settings.TEMPERATURE,
                'num_predict': max_tokens or settings.MAX_TOKENS,
                'top_k': 40,
                'top_p': 0.9,
                'repeat_penalty': 1.1,
                'stop': ["<|eot_id|>", "<|end_of_text|>", "Human:", "User:", "\n\n---"]
            }
        }
        
        try:
            logger.debug(f"Sending request to Ollama: {settings.OLLAMA_MODEL_NAME}")
            response = requests.post(
                self.generate_url, 
                json=data, 
                timeout=settings.OLLAMA_TIMEOUT
            )
            response.raise_for_status()
            
            result = response.json()
            generated_text = result.get('response', '').strip()
            
            if not generated_text:
                logger.warning("Empty response from Ollama")
                return "I apologize, but I couldn't generate a proper response. Please try rephrasing your question."
            
            # Clean up the response
            cleaned_text = self._clean_response(generated_text)
            
            # Log generation stats if available
            if 'eval_count' in result:
                tokens = result['eval_count']
                duration = result.get('eval_duration', 0) / 1e9  # Convert to seconds
                if duration > 0:
                    tokens_per_sec = tokens / duration
                    logger.debug(f"Generated {tokens} tokens in {duration:.2f}s ({tokens_per_sec:.1f} tok/s)")
            
            return cleaned_text
            
        except requests.exceptions.Timeout:
            logger.error("Ollama request timed out")
            return "Request timed out. The model might be busy or the question too complex. Please try again."
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {e}")
            return "I'm experiencing technical difficulties. Please check if Ollama is running properly."
        
        except Exception as e:
            logger.error(f"Unexpected error in generate(): {e}")
            return "An unexpected error occurred while generating the response."
    
    def _clean_response(self, text: str) -> str:
        """Clean up model output to remove repetitive patterns and artifacts"""
        
        # Remove system prompt remnants
        patterns_to_remove = [
            r"You are an AYUSH.*?assistant\.?",
            r"Answer briefly and accurately.*?",
            r"Do not invent herbs.*?",
            r"Always respond in.*?",
            r"Question:.*?Context:",
            r"Answer:",
            r"Based on the.*?context.*?:",
            r"Here.*?is.*?response.*?:",
        ]
        
        for pattern in patterns_to_remove:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove excessive repetition (same phrase repeated more than 2 times)
        def remove_repetition(match):
            phrase = match.group(1)
            return phrase * 2  # Keep maximum 2 repetitions
        
        # Handle different types of repetition
        text = re.sub(r'(.{10,}?)\1{2,}', remove_repetition, text)
        text = re.sub(r'\b(\w+)\s+\1(\s+\1)+\b', r'\1', text)  # word repetition
        
        # Clean up formatting
        text = re.sub(r'\n{3,}', '\n\n', text)  # Multiple newlines
        text = re.sub(r'\s{3,}', ' ', text)     # Multiple spaces
        text = re.sub(r'^\s*[-•]\s*', '', text, flags=re.MULTILINE)  # Remove bullet points at start
        
        # Remove incomplete sentences at the end
        sentences = text.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 10:
            text = '.'.join(sentences[:-1]) + '.'
        
        return text.strip()

class LocalLLM(OllamaLLM):
    """Compatibility alias for existing code"""
    pass

async def get_llm() -> OllamaLLM:
    """Get LLM instance using Ollama"""
    return OllamaLLM()