import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API Key not found in .env")
    exit(1)

genai.configure(api_key=api_key)

try:
    print("Available models:")
    for m in genai.list_models():
        print(f"- {m.name}")
        if 'generateContent' in m.supported_generation_methods:
            print("  Supports generateContent")
except Exception as e:
    print(f"Error calling API: {e}")
