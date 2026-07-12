import re

with open('modules/chatbot.py', 'r', encoding='utf-8') as f:
    chat_content = f.read()

chat_content = chat_content.replace('model_name="gemini-pro-latest"', 'model_name="gemini-flash-latest"')
chat_content = chat_content.replace('model_name="gemini-pro"', 'model_name="gemini-flash-latest"')

with open('modules/chatbot.py', 'w', encoding='utf-8') as f:
    f.write(chat_content)

print("Chatbot atualizado para gemini-flash-latest!")
