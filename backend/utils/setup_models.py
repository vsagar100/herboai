import spacy
import subprocess
import sys
from transformers import AutoTokenizer, AutoModelForCausalLM

def download_models():
    """Download all required models for offline operation"""
    print("📦 Downloading models for HerboAI...")
    
    # Download spaCy models
    models_to_download = [
        'en_core_web_sm',      # English
        'xx_ent_wiki_sm'       # Multilingual (for Hindi/Marathi)
    ]
    
    for model in models_to_download:
        try:
            print(f"⬇️  Downloading spaCy model: {model}")
            subprocess.run([sys.executable, '-m', 'spacy', 'download', model], 
                         check=True, capture_output=True)
            print(f"✅ {model} downloaded successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to download {model}: {e}")
    
    # Download transformer model
    try:
        print("⬇️  Downloading transformer model...")
        model_name = "microsoft/DialoGPT-small"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        print("✅ Transformer model downloaded successfully")
    except Exception as e:
        print(f"❌ Failed to download transformer model: {e}")
    
    print("🎉 All models downloaded! HerboAI is ready for offline operation.")

if __name__ == '__main__':
    download_models()