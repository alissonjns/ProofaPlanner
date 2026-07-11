import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Nova implementação da função pagina_plano_aula
nova_funcao = '''def pagina_plano_aula():
    st.markdown('<div class="sec">✨ Criar Sequência Didática com IA</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748B;">Preencha o básico e deixe a nossa Inteligência Artificial escrever a aula completa para você revisar!</p>', unsafe_allow_html=True)

    col_form, col_result = st.columns([1.2, 1], gap="large")

    with col_form:
        st.markdown("**1. Sobre a Aula:**")
        titulo_sd = st.text_input("📌 Título da Sequência", placeholder="Ex: Descobrindo meu corpo")

        c_seg, c_faixa = st.columns(2)
        with c_seg:
            segmento = st.selectbox("Segmento", ["Berçário 1", "Berçário 2", "Maternal 1", "Maternal 2", "Pré 1", "Pré 2"])
        with c_faixa:
            _faixas = {"EI01": "👶 Bebês (0 a 1a6m)", "EI02": "🧒 Crianças (1a7m a 3a11m)", "Ambas": "Mista"}
            faixa_sel = st.selectbox("Faixa Etária", options=list(_faixas.keys()), format_func=lambda x: _faixas[x])

        c_dur, c_camp = st.columns(2)
        with c_dur:
            duracao = st.selectbox("⏱️ Duração", ["Diário", "Semanal", "Quinzenal", "Mensal", "Bimestral"])
        with c_camp:
            _campos = {
                "Todos": "🔍 Todos os campos",
                "EO": "🤝 O eu, o outro e o nós",
                "CG": "🏃 Corpo, gestos e movimentos",
                "TS": "🎨 Traços, sons, cores e formas",
                "EF": "💬 Escuta, fala, pensamento...",
                "ET": "🔢 Espaços, tempos...",
            }
            campo_sel = st.selectbox("Campo Principal", options=list(_campos.keys()), format_func=lambda x: _campos[x])

        tema = st.text_input("🎯 Tema / Atividade Principal", placeholder="Ex: Brincadeira com argila e água")
        
        st.markdown("<br>", unsafe_allow_html=True)
        buscar = st.button("🔍  1. Encontrar objetivos BNCC", type="primary", use_container_width=True)

    with col_result:
        if buscar or st.session_state.get("bncc_buscados"):
            st.session_state.bncc_buscados = True
            
            if not tema.strip():
                st.error("⚠️ Escreva o Tema/Foco da aula para podermos buscar os objetivos na BNCC.")
                return

            faixa_filtro = None if faixa_sel == "Ambas" else faixa_sel
            campo_filtro = None if campo_sel == "Todos" else campo_sel

            with st.spinner("Buscando os objetivos certos para você..."):
                resultados = engine.buscar(texto=tema, faixa=faixa_filtro, campo=campo_filtro)

            if resultados:
                st.markdown("**2. Escolha os Códigos BNCC:**")
                selecionados = []
                for obj in resultados:
                    if st.checkbox(f"{obj['codigo']} - {obj['descricao']}", value=True, key=f"obj_{obj['codigo']}"):
                        selecionados.append(obj)
                
                st.session_state.objetivos_selecionados = selecionados
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("✨ 2. Gerar Plano Completo com IA", type="primary", use_container_width=True):
                    with st.spinner("A Inteligência Artificial está escrevendo seu plano... Isso pode levar uns 10 segundos."):
                        from modules.chatbot import ProfaBot
                        bot = ProfaBot()
                        plano_gerado = bot.gerar_plano_completo(
                            tema=tema,
                            faixa=_faixas[faixa_sel],
                            campo=_campos.get(campo_sel, campo_sel),
                            objetivos=selecionados
                        )
                        if plano_gerado:
                            st.session_state.plano_gerado = plano_gerado
                            st.success("Plano gerado com sucesso! Role a página para baixo para revisar.")
                        else:
                            st.error("Houve um erro ao gerar o plano. Tente novamente.")
            else:
                st.warning("Não encontrei objetivos para essas palavras. Tente descrever de outro jeito.")
        else:
            st.info("👈 Preencha os dados e clique em 'Encontrar objetivos BNCC'")

    # Seção de Revisão do Plano Gerado
    if st.session_state.get("plano_gerado"):
        st.divider()
        st.markdown("### 📝 Revisão do Plano Gerado")
        
        pg = st.session_state.plano_gerado
        
        col_ed1, col_ed2 = st.columns(2)
        with col_ed1:
            justificativa = st.text_area("Justificativa", value=pg.get("justificativa", ""), height=150)
        with col_ed2:
            obj_geral = st.text_area("Objetivo Geral", value=pg.get("obj_geral", ""), height=150)
            
        st.markdown("**Atividades Propostas:**")
        atividades = []
        for i, ativ in enumerate(pg.get("atividades", [])):
            c_a1, c_a2 = st.columns([1, 3])
            with c_a1:
                nome_a = st.text_input(f"Nome Ativ {i+1}", value=ativ.get("nome", ""))
            with c_a2:
                desc_a = st.text_area(f"Descrição Ativ {i+1}", value=ativ.get("descricao", ""), height=100)
            atividades.append({"nome": nome_a, "descricao": desc_a})
            
        avaliacao = st.text_area("Avaliação", value=pg.get("avaliacao", ""))
        
        # Feedback para a IA
        st.markdown("---")
        st.markdown("**🤖 Não gostou de algo? Peça para a IA refazer:**")
        feedback_ia = st.text_input("O que você quer mudar?", placeholder="Ex: Achei as atividades muito complexas para bebês, faça algo mais simples com música.")
        if st.button("🔄 Refazer plano com estas instruções", use_container_width=False):
            with st.spinner("Reescrevendo plano..."):
                from modules.chatbot import ProfaBot
                bot = ProfaBot()
                novo_plano = bot.gerar_plano_completo(
                    tema=tema,
                    faixa=_faixas[faixa_sel],
                    campo=_campos.get(campo_sel, campo_sel),
                    objetivos=st.session_state.objetivos_selecionados,
                    feedbacks=feedback_ia
                )
                if novo_plano:
                    st.session_state.plano_gerado = novo_plano
                    st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### ⬇️ Tudo certo? Baixar Documento!")
        
        # Prepara o objeto final para exportação
        st.session_state.plano_atual = {
            "titulo": titulo_sd if titulo_sd else "Sequência Didática",
            "tema": tema,
            "segmento": segmento,
            "faixa": _faixas[faixa_sel],
            "campo": _campos.get(campo_sel, campo_sel),
            "duracao": duracao,
            "justificativa": justificativa,
            "obj_geral": obj_geral,
            "avaliacao": avaliacao,
            "atividades": atividades,
            "objetivos_bncc": st.session_state.objetivos_selecionados,
        }
        
        c_word, c_pdf = st.columns(2)
        from modules.exportador import Exportador
        exportador = Exportador()
        
        with c_word:
            doc_word = exportador.gerar_sd_word(st.session_state.plano_atual)
            nome_word = f"SD_{tema[:15].replace(' ', '_').lower()}.docx"
            st.download_button("📄 Baixar em Word", data=doc_word, file_name=nome_word, 
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                               use_container_width=True, type="primary")
        
        with c_pdf:
            doc_pdf = exportador.gerar_sd_pdf(st.session_state.plano_atual)
            nome_pdf = f"SD_{tema[:15].replace(' ', '_').lower()}.pdf"
            st.download_button("📕 Baixar em PDF", data=doc_pdf, file_name=nome_pdf, 
                               mime="application/pdf", 
                               use_container_width=True)

'''

# Regex para substituir a função antiga pela nova
pattern = re.compile(r'def pagina_plano_aula\(\):.*?# ──────────────────────────────────────────────────────────────────────────────\n\ndef pagina_alunos\(\):', re.DOTALL)
new_content = re.sub(pattern, nova_funcao + '\n# ──────────────────────────────────────────────────────────────────────────────\n\ndef pagina_alunos():', content)

if content == new_content:
    print("ERRO: A regex não encontrou a função pagina_plano_aula.")
else:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("app.py atualizado com sucesso!")
