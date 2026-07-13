    def gerar_audio_resposta(self, texto: str) -> str:
        """Gera um arquivo MP3 com a voz da Aurora a partir de um texto e retorna o caminho."""
        texto_limpo = texto.replace("[GERAR_PLANO]", "") # não fala a tag secreta
        tts = gTTS(text=texto_limpo, lang='pt', tld='com.br', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
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
        {{"nome": "Nome criativo da atividade 1", "descricao": "Passo a passo bem detalhado da atividade 1..."}}
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
