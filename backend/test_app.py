#!/usr/bin/env python3

print("=== Testing HerboAI Dependencies ===\n")

try:
    print("Testing imports...")
    
    import flask
    print("✅ Flask imported")
    
    import spacy
    print("✅ spaCy imported")
    
    from sentence_transformers import SentenceTransformer
    print("✅ SentenceTransformers imported")
    
    import sklearn
    print("✅ scikit-learn imported")
    
    # Test spaCy model
    nlp = spacy.load('en_core_web_sm')
    print("✅ spaCy model loaded")
    
    # Test SentenceTransformer (note: no 's' at the end)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ SentenceTransformer model loaded")
    
    print("\n🎉 All imports successful! You can now run the main app.")
    
except Exception as e:
    print(f"❌ Error: {e}")