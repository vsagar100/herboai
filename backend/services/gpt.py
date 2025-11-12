import requests
import json

class OllamaChat:
    def __init__(self, model="gpt-oss:20b"):
        print("Initializing Ollama Chat Client...")
        self.model = model
        self.url = "http://localhost:11434/api/chat"
        self.messages = []
    
    def chat(self, user_message):
        """Chat with conversation history"""
        # Add user message
        print(f"User: {user_message}")
        self.messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Send to Ollama
        data = {
            "model": self.model,
            "messages": self.messages,
            "stream": False
        }
        
        response = requests.post(self.url, json=data)
        assistant_message = response.json()['message']['content']
        print(f"Assistant: {assistant_message}")
        # Add assistant response to history
        self.messages.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def clear_history(self):
        """Clear conversation history"""
        self.messages = []

# Usage
chat = OllamaChat()

print(chat.chat("What is Ashwagandha?"))
print(chat.chat("What are its benefits?"))  # Remembers context
print(chat.chat("इसे हिंदी में समझाइए"))  # Switch to Hindi