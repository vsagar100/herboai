# save as ollama_chat_simple.py
import requests
import json

def check_ollama_connection():
    try:
        response = requests.get('http://localhost:11434/api/tags')
        return response.status_code == 200
    except:
        return False

def list_models():
    try:
        response = requests.get('http://localhost:11434/api/tags')
        if response.status_code == 200:
            models = response.json()['models']
            return [model['name'] for model in models]
    except:
        pass
    return []

def chat_with_model(prompt, model='herboai'):
    url = 'http://localhost:11434/api/generate'
    data = {
        'model': model,
        'prompt': prompt,
        'stream': False,
        'options': {
            'temperature': 0.7,
            'num_predict': 200
        }
    }
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()['response']
    else:
        return f"Error: {response.status_code}"

def main():
    if not check_ollama_connection():
        print("Cannot connect to Ollama. Make sure it's running!")
        return
    
    models = list_models()
    print(f"Available models: {models}")
    
    model = 'herboai:latest'
    if model not in models:
        print(f"Model '{model}' not found!")
        return
    
    print(f"Using model: {model}")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        response = chat_with_model(user_input, model)
        print(f"AI: {response}\n")

if __name__ == "__main__":
    main()