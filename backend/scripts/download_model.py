#!/usr/bin/env python3
"""
Script to download recommended models for the AYUSH Herbs AI system
"""

import os
import requests
from pathlib import Path
from tqdm import tqdm
import argparse

def download_file(url: str, destination: Path, chunk_size: int = 8192) -> bool:
    """Download file with progress bar"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(destination, 'wb') as file, tqdm(
            desc=destination.name,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
                    progress_bar.update(len(chunk))
        
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Download models for AYUSH Herbs AI")
    parser.add_argument(
        "--model", 
        choices=["small_fast", "better_quality", "lightweight"],
        default="small_fast",
        help="Which model to download (default: small_fast)"
    )
    parser.add_argument(
        "--models-dir",
        type=str,
        default="./models",
        help="Directory to save models (default: ./models)"
    )
    
    args = parser.parse_args()
    
    # Model configurations
    models = {
        "small_fast": {
            "name": "Llama-3.2-3B-Instruct",
            "file": "Llama-3.2-3B-Instruct-Q4_K_M.gguf",
            "url": "https://huggingface.co/unsloth/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
            
        },
        "better_quality": {
            "name": "Qwen2.5-VL-7B-Instruct-UD-Q2_K_XL", 
            "file": "Qwen2.5-VL-7B-Instruct-UD-Q2_K_XL.gguf",
            "url": "https://huggingface.co/unsloth/Qwen2.5-VL-7B-Instruct-GGUF/resolve/main/Qwen2.5-VL-7B-Instruct-UD-Q2_K_XL.gguf",
        },
        "lightweight": {
            "name": "Mistral 7B Instruct Q4_K_M",
            "file": "mistral-7b-instruct-v0.1.Q4_K_M.gguf", 
            "url": "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        }
    }
    
    model_config = models[args.model]
    models_dir = Path(args.models_dir)
    models_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = models_dir / model_config["file"]
    
    print(f"Downloading {model_config['name']}...")
    print(f"Destination: {model_path}")
    
    if model_path.exists():
        print(f"Model already exists at {model_path}")
        response = input("Do you want to re-download? (y/N): ")
        if response.lower() != 'y':
            print("Skipping download.")
            return
    
    success = download_file(model_config["url"], model_path)
    
    if success:
        print(f"\n✅ Successfully downloaded {model_config['name']}")
        print(f"Model saved to: {model_path}")
        print("\nUpdate your environment variable:")
        print(f"export LLM_MODEL_PATH=\"{model_path.absolute()}\"")
        print("\nOr update your .env file:")
        print(f"LLM_MODEL_PATH={model_path.absolute()}")
    else:
        print(f"\n❌ Failed to download {model_config['name']}")

if __name__ == "__main__":
    main()