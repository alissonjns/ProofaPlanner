import re

with open('modules/chatbot.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_content = content.replace('model_name="gemini-1.5-flash",', 'model_name="gemini-1.5-pro-latest",')

with open('modules/chatbot.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print("Chatbot atualizado para gemini-1.5-pro-latest!")
