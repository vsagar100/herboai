#!/usr/bin/env python3
"""
Debug script to check model files and paths
"""

import os
from pathlib import Path

def check_model_setup():
    print("🔍 AYUSH Herbs AI - Model Debug")
    print("=" * 50)
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check models directory
    models_dir = current_dir / "models"
    print(f"📁 Models directory: {models_dir}")
    print(f"   Exists: {models_dir.exists()}")
    
    if models_dir.exists():
        print("\n📋 Files in models directory:")
        for file in models_dir.iterdir():
            size_mb = file.stat().st_size / (1024 * 1024) if file.is_file() else 0
            print(f"   {file.name} - {size_mb:.1f} MB")
    else:
        print("   ❌ Models directory does not exist")
        print("   💡 Creating models directory...")
        models_dir.mkdir(parents=True, exist_ok=True)
    
    # Check environment variables
    print("\n🌍 Environment Variables:")
    llm_path = os.getenv("LLM_MODEL_PATH")
    print(f"   LLM_MODEL_PATH: {llm_path}")
    
    # Check if the specified model exists
    model_path = Path(llm_path)
    print(f"\n🎯 Target model file: {model_path}")
    print(f"   Absolute path: {model_path.absolute()}")
    print(f"   Exists: {model_path.exists()}")
    
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"   Size: {size_mb:.1f} MB")
        
        # Check if file is complete (not corrupted)
        if size_mb < 100:  # GGUF models should be at least 100MB
            print("   ⚠️  Warning: File seems too small, might be corrupted")
        else:
            print("   ✅ File size looks good")
    else:
        print("   ❌ Model file not found!")
        
        # Suggest available models
        print("\n💡 Available model files in models directory:")
        if models_dir.exists():
            gguf_files = list(models_dir.glob("*.gguf"))
            if gguf_files:
                for gguf_file in gguf_files:
                    size_mb = gguf_file.stat().st_size / (1024 * 1024)
                    print(f"   - {gguf_file.name} ({size_mb:.1f} MB)")
            else:
                print("   - No .gguf files found")
        
        print("\n🔧 Solutions:")
        print("1. Download a model using: python scripts/download_model.py")
        print("2. Or set LLM_MODEL_PATH to an existing model file")
        print("3. Or use a different model path in settings.py")

if __name__ == "__main__":
    print("Testing model setup...\n")
    check_model_setup()