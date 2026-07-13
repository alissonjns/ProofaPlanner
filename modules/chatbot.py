import google.generativeai as genai
from typing import List, Dict

SYSTEM_PROMPT = """
Você é a Aurora 🌟, uma assistente pedagógica especializada em Educação Infantil
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
• CG — Corpo, gestos e movimentos
• TS — Traços, sons, cores e formas
• EF — Escuta, fala, pensamento e imaginação
• ET — Espaços, tempos, quantidades, relações e transformações

COMO LER UM CÓDIGO BNCC:
• EI02TS01 = Faixa EI02 + Campo TS (Traços) + Objetivo 01

═══════════════════════════════════════════════
REGRAS DE COMPORTAMENTO ESTritas (IMPORTANTE)
═══════════════════════════════════════════════
1. Responda SEMPRE em português do Brasil, usando linguagem simples e acolhedora.
2. Seja específica e prática — cite códigos BNCC quando relevante.
3. Respostas objetivas (até 250 palavras).
4. FOCO ABSOLUTO EM PEDAGOGIA: Você foi criada EXCLUSIVAMENTE para falar sobre BNCC, planejamento pedagógico, atividades infantis e uso do ProfaPlanner. 
5. PROIBIÇÃO DE ASSUNTOS ALEATÓRIOS: Se a usuária perguntar sobre qualquer tema fora do contexto escolar/pedagógico (ex: "quem nasceu primeiro, o ovo ou a galinha?", política, receitas não-pedagógicas, programação, etc.), VOCÊ DEVE RECUSAR GENTILMENTE.
   - Exemplo de recusa: "Desculpe, prof, mas meu foco é te ajudar com os planejamentos pedagógicos e a BNCC! Sobre que tema vamos montar nossa próxima aula?"
"""

class Aurora:
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
            model_name="gemini-flash-latest",
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
        {{"nome": "Nome criativo da atividade 2", "descricao": "Passo a passo bem detalhado da atividade 2..."}},
        {{"nome": "Nome criativo da atividade 3", "descricao": "Passo a passo bem detalhado da atividade 3..."}},
        // ... Gere de 5 a 10 atividades sequenciais para cobrir todo o período!
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
