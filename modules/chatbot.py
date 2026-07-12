import google.generativeai as genai
from typing import List, Dict

SYSTEM_PROMPT = """
Você é o ProfaBot 🤖, um assistente pedagógico especializado em Educação Infantil
e na BNCC (Base Nacional Comum Curricular). Você auxilia professoras de creche
(turmas de 0 a 3 anos) de forma prática, carinhosa e objetiva.

═══════════════════════════════════════════════
ESTRUTURA DA BNCC — EDUCAÇÃO INFANTIL (CRECHE)
═══════════════════════════════════════════════

FAIXAS ETÁRIAS:
• EI01: Bebês (0 a 1 ano e 6 meses)
• EI02: Crianças bem pequenas (1 ano e 7 meses a 3 anos e 11 meses)

CAMPOS DE EXPERIÊNCIA:
• EO — O eu, o outro e o nós
  → Identidade, autonomia, convivência, emoções, diversidade.

• CG — Corpo, gestos e movimentos
  → Motricidade, dança, expressão corporal, coordenação, autocuidado.

• TS — Traços, sons, cores e formas
  → Artes visuais, música, expressões artísticas, criação, sensibilidade.

• EF — Escuta, fala, pensamento e imaginação
  → Linguagem oral, leitura, escrita, literatura, imaginação.

• ET — Espaços, tempos, quantidades, relações e transformações
  → Matemática, ciências, natureza, espaço, tempo, lógica.

COMO LER UM CÓDIGO BNCC:
• EI02TS01 = Faixa EI02 + Campo TS (Traços) + Objetivo 01
• EI01CG03 = Faixa EI01 + Campo CG (Corpo) + Objetivo 03

═══════════════════════════════════════════════
COMO USAR O SISTEMA PROFAPLANNER
═══════════════════════════════════════════════

📂 "Modelo da Escola": faça upload do template de plano de aula (.xlsx ou .docx).
   O sistema usa esse modelo para gerar os documentos no formato correto.
   Se não tiver o arquivo, pode usar o template padrão do sistema.

📝 "Plano de Aula": 
   1. Escolha a faixa etária da turma (EI01 ou EI02)
   2. Escolha o campo de experiência (ou deixe "Todos")
   3. Digite o tema/atividade (ex: "brincadeira com argila")
   4. O sistema busca automaticamente os objetivos BNCC mais relevantes
   5. Marque os objetivos desejados e clique em "Gerar Documento"
   6. Baixe o Word pronto para entregar

👶 "Alunos e Relatórios":
   1. Cadastre os alunos da turma com nome e faixa etária
   2. Para cada aluno, marque cada objetivo BNCC como:
      ✅ Atingido | 🔄 Em Desenvolvimento | ⏳ Não Iniciado
   3. Clique em "Gerar Relatório" para baixar o relatório bimestral em Word

🤖 "ProfaBot" (você está aqui!):
   Tire dúvidas sobre BNCC, planejamento pedagógico e o uso do sistema.

═══════════════════════════════════════════════
REGRAS DE COMPORTAMENTO
═══════════════════════════════════════════════
- Responda SEMPRE em português do Brasil
- Use linguagem simples, acolhedora e encorajadora
- Seja específica e prática — cite códigos BNCC quando relevante
- Respostas objetivas (até 250 palavras), a menos que peçam mais detalhes
- Use emojis com moderação para deixar a resposta mais amigável
- Nunca invente objetivos ou códigos BNCC que não existem
- Se não souber algo específico da escola da professora, oriente a verificar com a coordenação
"""


class ProfaBot:
    """Chatbot pedagógico usando Google Gemini."""

    def __init__(self, api_key: str = ""):
        if not api_key:
            import os
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")
            
            # Se não achou no .env, tenta buscar no st.secrets (para rodar na nuvem)
            if not api_key:
                try:
                    import streamlit as st
                    api_key = st.secrets.get("GEMINI_API_KEY", "")
                except Exception:
                    pass

            if not api_key:
                raise ValueError("Chave da API não encontrada. Configure o arquivo .env ou o st.secrets")
                
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-pro",
            system_instruction=SYSTEM_PROMPT,
        )

    def responder(self, mensagem: str, historico: List[Dict]) -> str:
        """Envia uma mensagem e retorna a resposta do bot."""
        try:
            # Converte histórico do formato Streamlit para o formato Gemini
            gemini_history = []
            for msg in historico:
                role = "model" if msg["role"] == "assistant" else "user"
                gemini_history.append({"role": role, "parts": [msg["content"]]})

            chat = self.model.start_chat(history=gemini_history)
            resposta = chat.send_message(mensagem)
            return resposta.text

        except Exception as e:
            erro = str(e)
            if "API_KEY" in erro.upper() or "INVALID" in erro.upper():
                return (
                    "⚠️ **Chave API inválida.** Verifique se você copiou corretamente "
                    "a chave do [Google AI Studio](https://aistudio.google.com)."
                )
            return (
                f"⚠️ Não consegui me conectar agora. Erro: `{erro}`\n\n"
                "Tente novamente em alguns instantes."
            )

    def gerar_plano_completo(self, tema: str, faixa: str, campo: str, objetivos: list, feedbacks: str = "") -> dict:
        """Gera um plano completo no formato JSON usando os dados e objetivos fornecidos."""
        
        objs_texto = "\n".join([f"[{o['codigo']}] {o['descricao']}" for o in objetivos])
        
        prompt = f"""
Você é uma especialista em pedagogia da Educação Infantil. Escreva o conteúdo de um plano de aula completo baseado nestes parâmetros:
Tema: {tema}
Faixa Etária: {faixa}
Campo Principal: {campo}
Objetivos BNCC Escolhidos:
{objs_texto}

{('Atenção, a professora pediu a seguinte alteração no plano anterior: ' + feedbacks) if feedbacks else ''}

Retorne APENAS um JSON válido com a seguinte estrutura (sem markdown extra, sem ```json, apenas as chaves e valores):
{{
    "justificativa": "Texto explicando a importância pedagógica...",
    "obj_geral": "O objetivo geral formatado de forma clara...",
    "atividades": [
        {{"nome": "Nome criativo da atividade 1", "descricao": "Passo a passo bem detalhado da atividade 1..."}},
        {{"nome": "Nome criativo da atividade 2", "descricao": "Passo a passo bem detalhado da atividade 2..."}}
    ],
    "avaliacao": "Como o aprendizado será observado e registrado..."
}}
"""
        try:
            resp = self.model.generate_content(prompt)
            texto = resp.text.strip()
            if texto.startswith("```json"):
                texto = texto.replace("```json", "").replace("```", "").strip()
            
            import json
            return json.loads(texto)
        except Exception as e:
            print(f"Erro na geração do plano: {e}")
            return None
