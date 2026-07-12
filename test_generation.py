import google.generativeai as genai
from modules.chatbot import ProfaBot

bot = ProfaBot()
bot.model = genai.GenerativeModel('gemini-flash-latest')

print("Iniciando geração de plano com flash...")
try:
    resultado = bot.gerar_plano_completo(
        tema="descobrindo corpo",
        faixa="Bebês",
        campo="Todos",
        objetivos=[{"codigo": "EI01FO01", "descricao": "Perceber"}]
    )
    print("Resultado flash:", resultado)
except Exception as e:
    print("ERRO:", e)
