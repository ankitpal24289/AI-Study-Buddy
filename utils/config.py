import os
from dotenv import load_dotenv

load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key not found. Check your .env file.")
        
        use_groq = os.getenv("GROQ_ENABLED", "false").lower() == "true"
        
        if use_groq:
            from groq import Groq
            _client = Groq(api_key=api_key)
        else:
            from openai import OpenAI
            _client = OpenAI(api_key=api_key)
    
    return _client

def get_model():
    return os.getenv("OPENAI_MODEL", "llama-3.3-70b-versatile")

def chat_completion(messages, temperature=0.7):
    client = get_client()
    response = client.chat.completions.create(
        model=get_model(),
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()