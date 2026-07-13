import google.generativeai as genai
from typing import List, Dict
import os
import tempfile
import asyncio
import edge_tts

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
5. PROIBIÇÃO DE ASSUNTOS ALEATÓRIOS: Se a pessoa perguntar sobre qualquer tema fora do contexto escolar/pedagógico (ex: "quem nasceu primeiro, o ovo ou a galinha?", política, receitas não-pedagógicas, programação, etc.), VOCÊ DEVE RECUSAR GENTILMENTE.
   - Exemplo de recusa: "Desculpe, mas meu foco é ajudar com os planejamentos pedagógicos e a BNCC! Sobre que tema vamos montar nossa próxima aula?"

═══════════════════════════════════════════════
MODO ENTREVISTA (CRIAÇÃO DE PLANO DE AULA)
═══════════════════════════════════════════════
Se você estiver conduzindo uma entrevista para criar um plano de aula:
- Na sua PRIMEIRA PERGUNTA da entrevista, sempre pergunte o NOME da pessoa para manter uma comunicação carinhosa e personalizada.
- Você DEVE fazer as perguntas necessárias para montar um plano BNCC perfeito (Idade, Tema, Duração, Materiais disponíveis, Interesses das crianças, etc).
- IMPORTANTE: Pergunte se a pessoa deseja um plano para um DIA, uma SEMANA ou um MÊS, para saber exatamente a quantidade e a abrangência das atividades que você deverá criar!
- Pergunte UMA COISA DE CADA VEZ. Nunca mande uma lista de 5 perguntas.
- Quando você perceber que já tem informações suficientes para gerar um plano de aula completo, VOCÊ DEVE ENCERRAR A ENTREVISTA escrevendo EXATAMENTE a tag mágica: [GERAR_PLANO].
- Exemplo de finalização: "Perfeito! Já tenho tudo que preciso. [GERAR_PLANO]"
"""

class Aurora:
    """Chatbot pedagógico usando Google Gemini com suporte a áudio."""

    def __init__(self, api_key: str = ""):
        if not api_key:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")
            
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
            model_name="gemini-flash-lite-latest",
            system_instruction=SYSTEM_PROMPT,
        )

    def transcrever_audio(self, audio_bytes: bytes) -> str:
        """Recebe bytes de áudio, envia de forma inline pro Gemini e retorna o texto transcrito."""
        try:
            audio_part = {
                "mime_type": "audio/wav",
                "data": audio_bytes
            }
            resp = self.model.generate_content([
                "Transcreva exatamente o que foi dito neste áudio (em português do Brasil). Não adicione nenhum comentário seu, retorne apenas a transcrição direta.",
                audio_part
            ])
            return resp.text.strip()
        except Exception as e:
            return f"[Erro ao transcrever áudio: {str(e)}]"

    def gerar_audio_resposta(self, texto: str) -> str:
        """Gera um arquivo MP3 com a voz neural da Aurora a partir de um texto."""
        texto_limpo = texto.replace("[GERAR_PLANO]", "") # não fala a tag secreta
        
        async def _gerar_tts(texto_para_falar, filename):
            communicate = edge_tts.Communicate(texto_para_falar, "pt-BR-ThalitaNeural")
            await communicate.save(filename)
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            asyncio.run(_gerar_tts(texto_limpo, tmp.name))
            return tmp.name

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

    def gerar_plano_do_chat(self, historico: List[Dict]) -> dict:
        """Gera um plano completo no formato JSON analisando a entrevista dinâmica realizada."""
        
        chat_texto = ""
        for msg in historico:
            papel = "Professor(a)" if msg["role"] == "user" else "Aurora"
            chat_texto += f"{papel}: {msg['content']}\n"
            
        prompt = f"""
Você é uma especialista em pedagogia da Educação Infantil. 
Baseado EXCLUSIVAMENTE na entrevista abaixo conduzida entre a Aurora e a Professor(a), extraia as informações e escreva o conteúdo de um plano de aula completo seguindo as diretrizes da BNCC.

HISTÓRICO DA ENTREVISTA:
{chat_texto}

INSTRUÇÕES:
- Você deve definir e escolher os Códigos e Objetivos BNCC mais adequados baseados no que foi discutido.
- Se algum campo não foi discutido (ex: duração), assuma um padrão razoável para a Educação Infantil (ex: 1 aula).

Retorne APENAS um JSON válido com a seguinte estrutura (sem markdown extra, sem ```json, apenas as chaves e valores):
{{
    "tema": "Tema central extraído do chat",
    "turma": "Turma/Faixa etária discutida",
    "duracao": "Duração extraída",
    "objetivos_bncc": [
        {{"codigo": "EI02...", "descricao": "Descrição do objetivo escolhido por você..."}}
    ],
    "justificativa": "Texto explicando a importância pedagógica...",
    "obj_geral": "O objetivo geral formatado de forma clara...",
    "atividades": [
        {{"nome": "Nome criativo da atividade 1", "descricao": "Explique passo a passo de forma detalhada e lúdica..."}},
        {{"nome": "Nome criativo da atividade 2", "descricao": "Explique passo a passo de forma detalhada e lúdica..."}},
        {{"nome": "Nome criativo da atividade 3", "descricao": "Explique passo a passo de forma detalhada e lúdica..."}}
        // IMPORTANTE: Gere de 3 a 5 atividades sequenciais formando uma verdadeira Sequência Didática elegante e completa!
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
            print(f"Erro na geração do plano pelo chat: {e}")
            return None
