from pydantic import BaseModel
import os


class Settings(BaseModel):
    # Ollama Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL_NAME: str = os.getenv("OLLAMA_MODEL_NAME", "herboai:latest")
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "120"))  # seconds
    
    # Fallback to direct GGUF loading (keeping for compatibility)
    LLM_MODEL_PATH: str = os.getenv("LLM_MODEL_PATH", "./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf")
    
    # Multilingual embedding model for better semantic search
    EMBEDDINGS_MODEL: str = os.getenv("EMBEDDINGS_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    
    # Database and index paths
    DB_PATH: str = os.getenv("DB_PATH", "./ayush.db")
    INDEX_PATH: str = os.getenv("INDEX_PATH", "./vector_store/faiss.index")
    
    # Model cache directory
    HF_HOME: str = os.getenv("HF_HOME", "./models_cache")
    
    # Generation parameters optimized for medical/herbal information
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", 400))  # Reduced for focused responses
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", 0.2))  # Low for consistency
    
    # Additional settings for better performance
    CONTEXT_LENGTH: int = int(os.getenv("CONTEXT_LENGTH", 4096))
    TOP_K_SEARCH: int = int(os.getenv("TOP_K_SEARCH", 4))
    MIN_SIMILARITY_SCORE: float = float(os.getenv("MIN_SIMILARITY_SCORE", 0.1))


settings = Settings()

# Ollama model recommendations for AYUSH system:
OLLAMA_MODEL_RECOMMENDATIONS = {
    "llama3.2:3b-instruct": {
        "description": "Balanced quality and speed, good for medical Q&A",
        "ram_usage": "~4-5 GB",
        "install": "ollama pull llama3.2:3b-instruct"
    },
    "llama3.2:1b-instruct": {
        "description": "Lightweight, faster responses",
        "ram_usage": "~2-3 GB", 
        "install": "ollama pull llama3.2:1b-instruct"
    },
    "llama2:7b-chat": {
        "description": "High quality, slower responses",
        "ram_usage": "~8-10 GB",
        "install": "ollama pull llama2:7b-chat"
    },
    "mistral:7b-instruct": {
        "description": "Good instruction following, efficient",
        "ram_usage": "~6-8 GB",
        "install": "ollama pull mistral:7b-instruct"
    }
}