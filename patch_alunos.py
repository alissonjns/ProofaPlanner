import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

nova_funcao = '''def pagina_alunos():
    st.markdown('<div class="sec">👶 Relatório dos Alunos</div>', unsafe_allow_html=True)
    
    from modules.db import BancoDados
    db = BancoDados()
    alunos_db = db.get_alunos()

    tab1, tab2 = st.tabs(["📋  Minha Turma", "📊  Registro de Desenvolvimento"])

    with tab1:
        st.markdown("**Adicionar aluno à turma:**")
        c1, c2, c3 = st.columns([2.5, 2, 0.8])
        with c1:
            nome_aluno = st.text_input("Nome da criança", placeholder="Nome completo",
                                       label_visibility="collapsed")
        with c2:
            faixa_aluno = st.selectbox("Faixa",
                                       ["EI01 — Bebês (0 a 1a 6m)", "EI02 — Crianças maiores (1a7m a 3a11m)"],
                                       label_visibility="collapsed")
        with c3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Adicionar", type="primary", use_container_width=True):
                if nome_aluno.strip():
                    faixa_cod = "EI01" if "EI01" in faixa_aluno else "EI02"
                    nomes = [a["nome"].lower() for a in alunos_db]
                    if nome_aluno.strip().lower() in nomes:
                        st.error("Já existe um aluno com esse nome.")
                    else:
                        db.add_aluno(nome_aluno.strip(), faixa_cod)
                        st.success(f"✅ {nome_aluno} adicionado(a)!")
                        st.rerun()
                else:
                    st.error("Digite o nome da criança.")

        st.divider()

        if alunos_db:
            st.markdown(f"**{len(alunos_db)} criança(s) na turma:**")
            for aluno in alunos_db:
                c_nome, c_prog, c_del = st.columns([3, 2, 0.4])
                with c_nome:
                    tag = "tag-ei01" if aluno["faixa"] == "EI01" else "tag-ei02"
                    label = "Bebê" if aluno["faixa"] == "EI01" else "Criança maior"
                    st.markdown(f'<span style="color:#1E293B; font-weight:500;">👤 {aluno["nome"]}</span>'
                                f'&nbsp;&nbsp;<span class="{tag}">{label}</span>',
                                unsafe_allow_html=True)
                with c_prog:
                    n_av = len(aluno.get("evolucao", {}))
                    n_at = sum(1 for v in aluno.get("evolucao", {}).values() if v == "A")
                    st.markdown(f'<span style="color:#475569; font-size:0.82rem;">'
                                f'{n_av} avaliados · {n_at} atingidos</span>', unsafe_allow_html=True)
                with c_del:
                    if st.button("🗑️", key=f"del_{aluno['id']}"):
                        db.delete_aluno(aluno["id"])
                        st.rerun()
                st.divider()
        else:
            st.info("Ainda não há crianças cadastradas. Adicione os alunos da sua turma acima.")

    with tab2:
        if not alunos_db:
            st.info("Cadastre os alunos na aba **Minha Turma** primeiro.")
            return

        aluno_nome = st.selectbox("Qual criança você quer avaliar?",
                                  [a["nome"] for a in alunos_db])
        aluno = next(a for a in alunos_db if a["nome"] == aluno_nome)

        _status_opts = {"A": "✅ Já consegue fazer", "D": "🔄 Está aprendendo", "N": "⏳ Ainda não iniciou"}

        st.markdown(
            f'<div style="color:#64748B; font-size:0.85rem; margin:0.5rem 0 1rem;">'
            f"Para cada habilidade abaixo, marque como <strong style='color:#1E293B;'>{aluno_nome}</strong> está:</div>",
            unsafe_allow_html=True)

        for campo_nome, objetivos in engine.get_objetivos_por_faixa(aluno["faixa"]).items():
            n_at = sum(1 for o in objetivos if aluno["evolucao"].get(o["codigo"]) == "A")
            # Correção do translate quebrando o expander: evitamos emoji no título se possivel, ou usamos icon nativo (Streamlit 1.35+)
            with st.expander(f"{campo_nome} — {n_at}/{len(objetivos)} conquistados", icon="📌"):
                for obj in objetivos:
                    c_desc, c_st = st.columns([4, 1.4])
                    with c_desc:
                        st.markdown(
                            f'<span class="badge-bncc">{obj["codigo"]}</span>'
                            f'<span style="color:#334155; font-size:0.85rem; margin-left:6px;">{obj["descricao"]}</span>',
                            unsafe_allow_html=True)
                    with c_st:
                        status = aluno["evolucao"].get(obj["codigo"], "N")
                        novo = st.selectbox("s", list(_status_opts.keys()),
                                            format_func=lambda x: _status_opts[x],
                                            index=list(_status_opts.keys()).index(status),
                                            key=f"st_{aluno_nome}_{obj['codigo']}",
                                            label_visibility="collapsed")
                        
                        if novo != status:
                            evolucao_atual = aluno["evolucao"].copy()
                            evolucao_atual[obj["codigo"]] = novo
                            db.update_evolucao(aluno["id"], evolucao_atual)
                            st.rerun()
                    st.divider()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬇️  Gerar Relatório Bimestral desta criança",
                     type="primary", use_container_width=True):
            with st.spinner(f"Gerando relatório de {aluno_nome}..."):
                doc_bytes = Exportador().gerar_relatorio_aluno(aluno, engine)
            nome_arquivo = f"relatorio_{aluno_nome.replace(' ', '_').lower()}.docx"
            st.download_button(
                label=f"📄  Baixar Relatório de {aluno_nome}",
                data=doc_bytes, file_name=nome_arquivo,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True)'''

pattern = re.compile(r'def pagina_alunos\(\):.*?# ──────────────────────────────────────────────────────────────────────────────\n\ndef pagina_profabot\(\):', re.DOTALL)
new_content = re.sub(pattern, nova_funcao + '\n\n# ──────────────────────────────────────────────────────────────────────────────\n\ndef pagina_profabot():', content)

if content == new_content:
    print("ERRO: A regex não encontrou a função pagina_alunos.")
else:
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("app.py atualizado com sucesso (Alunos DB)!")
