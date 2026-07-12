import re

# 1. Corrigir chatbot.py (Mudar modelo para gemini-pro)
with open('modules/chatbot.py', 'r', encoding='utf-8') as f:
    chat_content = f.read()
chat_content = chat_content.replace('model_name="gemini-1.5-pro-latest"', 'model_name="gemini-pro"')
chat_content = chat_content.replace('model_name="gemini-1.5-flash"', 'model_name="gemini-pro"')
with open('modules/chatbot.py', 'w', encoding='utf-8') as f:
    f.write(chat_content)

# 2. Corrigir app.py (Limitar resultados a 5 e melhorar CSS do header)
with open('app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

# Substituir o CSS
old_css = """#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}"""
new_css = """#MainMenu {visibility: hidden;}
header {display: none !important;}
footer {display: none !important;}
.viewerBadge_container__1QSob {display: none !important;}
[data-testid="manage-app-button"] {display: none !important;}"""
app_content = app_content.replace(old_css, new_css)

# Limitar resultados da busca
old_busca = "resultados = engine.buscar(texto=tema, faixa=faixa_filtro, campo=campo_filtro)"
new_busca = "resultados = engine.buscar(texto=tema, faixa=faixa_filtro, campo=campo_filtro)[:4] # Limita aos 4 melhores resultados"
app_content = app_content.replace(old_busca, new_busca)

# Alterar texto
old_text = "**2. Escolha os Códigos BNCC:**"
new_text = "**2. Escolha os Códigos BNCC (Mostrando os 4 melhores):**"
app_content = app_content.replace(old_text, new_text)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

print("Patch aplicado com sucesso!")
