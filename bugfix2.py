"""
Patch cirúrgico: corrige todos os bugs visuais identificados nas prints.
Problemas:
1. Tour (passo 2/3): cards com classes antigas do tema escuro
2. Navbar pills: texto invisível nos itens não selecionados  
3. Campo fantasma na etapa 1: st.markdown com <div class='pp-card'> cria visual esquisito
4. Expander com "array/light" - emoji emoji no título
5. Botões PDF (branco) e Word (todo verde) — padronizar layout branco/outline
6. Chat input preto
7. Aumentar resultados BNCC de 5 para 8
"""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# ──────────────────────────────────────────────────────────────────────
# FIX 1: CSS aggressivo para selectbox, pills, chat
# ──────────────────────────────────────────────────────────────────────
old_pills_css = """/* ── Pills navigation ── */
[data-testid="stPills"] {
    gap: 6px !important;
}
[data-testid="stPills"] button {
    background: #FFFFFF !important;
    color: #475569 !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 20px !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stPills"] button:hover {
    border-color: #10B981 !important;
    color: #10B981 !important;
}
[data-testid="stPills"] button[aria-selected="true"] {
    background: linear-gradient(135deg, #10B981, #059669) !important;
    color: white !important;
    border-color: transparent !important;
    box-shadow: 0 4px 12px rgba(16,185,129,0.3) !important;
}"""

new_pills_css = """/* ── Pills navigation ── */
[data-testid="stPills"] {
    gap: 6px !important;
}
[data-testid="stPills"] button,
[data-testid="stPills"] button span,
[data-testid="stPills"] button p {
    background: #FFFFFF !important;
    color: #334155 !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 20px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stPills"] button:hover,
[data-testid="stPills"] button:hover span {
    border-color: #10B981 !important;
    color: #059669 !important;
}
[data-testid="stPills"] button[aria-selected="true"],
[data-testid="stPills"] button[aria-selected="true"] span,
[data-testid="stPills"] button[aria-selected="true"] p {
    background: linear-gradient(135deg, #10B981, #059669) !important;
    color: white !important;
    border-color: transparent !important;
    box-shadow: 0 4px 12px rgba(16,185,129,0.3) !important;
}"""

content = content.replace(old_pills_css, new_pills_css)

# ──────────────────────────────────────────────────────────────────────
# FIX 2: Tour passo 2 — remover classes escuras, usar pp-card light
# ──────────────────────────────────────────────────────────────────────
old_tour_step2 = """            _passos = [
                ("📋", "card-azul",  "1. Você coloca o modelo da escola",
                 "Se a escola te deu um formulário de plano de aula no Word ou Excel, você o adiciona aqui. "
                 "O sistema usa ele como base. Se não tiver, usamos um modelo pronto."),
                ("✏️", "card-verde", "2. Você digita o tema da aula",
                 "Escreve o tema que você planejou, como \\"Brincadeira com argila\\" ou \\"Música e ritmo\\". "
                 "O sistema encontra automaticamente os objetivos BNCC certos para você!"),
                ("⬇️", "card-roxo",  "3. Você baixa o documento pronto",
                 "Clique em um botão e o plano de aula já sai preenchido no formato Word, "
                 "pronto para imprimir ou entregar à coordenação."),
            ]
            for icon, cls, titulo, desc in _passos:
                st.markdown(f"""
                <div class="card {cls}" style="padding:1.2rem 1.5rem;">
                    <div style="font-size:1.5rem; margin-bottom:0.4rem;">{icon}</div>
                    <div style="font-weight:700; color:#F1F5F9; margin-bottom:0.3rem;">{titulo}</div>
                    <div style="color:#94A3B8; font-size:0.9rem; line-height:1.6;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)"""

new_tour_step2 = """            _passos = [
                ("📋", "#EFF6FF", "#1E40AF", "#DBEAFE", "1. Você coloca o modelo da escola",
                 "Se a escola te deu um formulário de plano de aula no Word ou Excel, você o adiciona aqui. "
                 "O sistema usa ele como base. Se não tiver, usamos um modelo pronto."),
                ("✏️", "#ECFDF5", "#065F46", "#A7F3D0", "2. Você digita o tema da aula",
                 "Escreve o tema que você planejou, como 'Brincadeira com argila' ou 'Música e ritmo'. "
                 "O sistema encontra automaticamente os objetivos BNCC certos para você!"),
                ("⬇️", "#FFF7ED", "#9A3412", "#FED7AA", "3. Você baixa o documento pronto",
                 "Clique em um botão e o plano de aula já sai preenchido no formato Word, "
                 "pronto para imprimir ou entregar à coordenação."),
            ]
            for icon, bg, titulo_cor, border, titulo, desc in _passos:
                st.markdown(f\"""
                <div style="background:{bg}; border:1.5px solid {border}; border-radius:14px; padding:1.2rem 1.5rem; margin-bottom:0.8rem;">
                    <div style="font-size:1.5rem; margin-bottom:0.4rem;">{icon}</div>
                    <div style="font-weight:700; color:{titulo_cor}; margin-bottom:0.3rem; font-size:1rem;">{titulo}</div>
                    <div style="color:#475569; font-size:0.88rem; line-height:1.6;">{desc}</div>
                </div>
                \""", unsafe_allow_html=True)"""

content = content.replace(old_tour_step2, new_tour_step2)

# ──────────────────────────────────────────────────────────────────────
# FIX 3: Tour passo 3 — remover classes escuras  
# ──────────────────────────────────────────────────────────────────────
old_tour_step3 = """            for pag, icon, titulo, desc in _opcoes:
                st.markdown(f\"\"\"
                <div class="card" style="padding:1rem 1.3rem; display:flex; align-items:center; gap:1rem;">
                    <div style="font-size:2rem; flex-shrink:0;">{icon}</div>
                    <div>
                        <div style="font-weight:700; color:#F1F5F9;">{titulo}</div>
                        <div style="color:#64748B; font-size:0.85rem;">{desc}</div>
                    </div>
                </div>
                \"\"\", unsafe_allow_html=True)"""

new_tour_step3 = """            for pag, icon, titulo, desc in _opcoes:
                st.markdown(f\"""
                <div style="background:#FFFFFF; border:1.5px solid #E2E8F0; border-radius:14px; padding:1rem 1.3rem; display:flex; align-items:center; gap:1rem; margin-bottom:0.2rem; box-shadow:0 2px 8px rgba(0,0,0,0.05);">
                    <div style="font-size:2rem; flex-shrink:0;">{icon}</div>
                    <div>
                        <div style="font-weight:700; color:#0F172A; font-size:0.95rem;">{titulo}</div>
                        <div style="color:#64748B; font-size:0.83rem;">{desc}</div>
                    </div>
                </div>
                \""", unsafe_allow_html=True)"""

content = content.replace(old_tour_step3, new_tour_step3)

# ──────────────────────────────────────────────────────────────────────
# FIX 4: Tour passo 2 título (classe "hero-title" escura)
# ──────────────────────────────────────────────────────────────────────
old_tour2_title = """            st.markdown(\"\"\"
            <div class="hero-title" style="font-size:2rem; text-align:center; margin-bottom:1.5rem;">
                Como o sistema funciona?
            </div>
            \"\"\", unsafe_allow_html=True)"""

new_tour2_title = """            st.markdown(\"\"\"
            <div style="font-size:2rem; font-weight:800; color:#0F172A; text-align:center; margin-bottom:1.5rem;">
                Como o sistema funciona?
            </div>
            \"\"\", unsafe_allow_html=True)"""

content = content.replace(old_tour2_title, new_tour2_title)

# ──────────────────────────────────────────────────────────────────────
# FIX 5: Tour passo 3 título (classes "hero-title" e "hero-sub" escuras)
# ──────────────────────────────────────────────────────────────────────
old_tour3_title = """            st.markdown(\"\"\"
            <div class="hero-title" style="font-size:2rem; text-align:center; margin-bottom:0.5rem;">
                Tudo pronto! 🎉
            </div>
            <div class="hero-sub" style="text-align:center; margin-bottom:1.5rem;">
                Por onde você quer começar?
            </div>
            \"\"\", unsafe_allow_html=True)"""

new_tour3_title = """            st.markdown(\"\"\"
            <div style="font-size:2rem; font-weight:800; color:#0F172A; text-align:center; margin-bottom:0.5rem;">
                Tudo pronto! 🎉
            </div>
            <div style="color:#64748B; font-size:1rem; text-align:center; margin-bottom:1.5rem;">
                Por onde você quer começar?
            </div>
            \"\"\", unsafe_allow_html=True)"""

content = content.replace(old_tour3_title, new_tour3_title)

# ──────────────────────────────────────────────────────────────────────
# FIX 6: Página Início — cards com classes escuras
# ──────────────────────────────────────────────────────────────────────
old_inicio_hero = """    st.markdown('<div class="hero-title">Olá, Professora! 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Escolha o que você quer fazer hoje:</div>', unsafe_allow_html=True)"""

new_inicio_hero = """    st.markdown('<div style="font-size:2rem; font-weight:800; color:#0F172A; margin-bottom:0.3rem;">Olá, Professora! 👋</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#64748B; font-size:1rem; margin-bottom:0.5rem;">Escolha o que você quer fazer hoje:</div>', unsafe_allow_html=True)"""

content = content.replace(old_inicio_hero, new_inicio_hero)

old_inicio_cards = """    for col, (pag, icon, titulo, desc, cls) in zip([c1, c2, c3], _atalhos):
        with col:
            st.markdown(f\"\"\"<div class="card {cls}">
                <div style="font-size:2rem; margin-bottom:0.5rem;">{icon}</div>
                <div style="font-weight:700; color:#F1F5F9; margin-bottom:0.3rem; font-size:1rem;">{titulo}</div>
                <div style="color:#475569; font-size:0.82rem; line-height:1.5;">{desc}</div>
            </div>\"\"\", unsafe_allow_html=True)"""

new_inicio_cards = """    _card_colors = {"card-verde": ("#ECFDF5", "#A7F3D0", "#065F46"), "card-azul": ("#EFF6FF", "#BFDBFE", "#1E40AF"), "card-roxo": ("#F5F3FF", "#DDD6FE", "#5B21B6")}
    for col, (pag, icon, titulo, desc, cls) in zip([c1, c2, c3], _atalhos):
        with col:
            bg, border, cor = _card_colors.get(cls, ("#FFFFFF", "#E2E8F0", "#0F172A"))
            st.markdown(f\"""<div style="background:{bg}; border:1.5px solid {border}; border-radius:14px; padding:1.5rem; margin-bottom:0.8rem; box-shadow:0 2px 10px rgba(0,0,0,0.05);">
                <div style="font-size:2rem; margin-bottom:0.5rem;">{icon}</div>
                <div style="font-weight:700; color:{cor}; margin-bottom:0.3rem; font-size:1rem;">{titulo}</div>
                <div style="color:#475569; font-size:0.82rem; line-height:1.5;">{desc}</div>
            </div>\""", unsafe_allow_html=True)"""

content = content.replace(old_inicio_cards, new_inicio_cards)

# ──────────────────────────────────────────────────────────────────────
# FIX 7: Remover <div class='pp-card'> / </div> que cria campo fantasma
# ──────────────────────────────────────────────────────────────────────
content = content.replace(
    "        st.markdown(\"<div class='pp-card'>\", unsafe_allow_html=True)\n",
    ""
)
content = content.replace(
    "        st.markdown(\"</div>\", unsafe_allow_html=True)\n\n        # Guarda na sessão",
    "\n        # Guarda na sessão"
)

# ──────────────────────────────────────────────────────────────────────
# FIX 8: Botões de download — padronizar (ambos outline, Word verde, PDF coral)
# ──────────────────────────────────────────────────────────────────────
old_download_btns = """        with c_word:
            doc_word = exportador.gerar_sd_word(plano_final)
            nome_word = f"SD_{tema[:15].replace(' ', '_').lower()}.docx"
            st.download_button(
                "📄 Baixar em Word (.docx)",
                data=doc_word, file_name=nome_word,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True, type="primary"
            )
        with c_pdf:
            doc_pdf = exportador.gerar_sd_pdf(plano_final)
            nome_pdf = f"SD_{tema[:15].replace(' ', '_').lower()}.pdf"
            st.download_button(
                "📕 Baixar em PDF",
                data=doc_pdf, file_name=nome_pdf,
                mime="application/pdf",
                use_container_width=True
            )"""

new_download_btns = """        with c_word:
            doc_word = exportador.gerar_sd_word(plano_final)
            nome_word = f"SD_{tema[:15].replace(' ', '_').lower()}.docx"
            st.download_button(
                "📄 Baixar em Word (.docx)",
                data=doc_word, file_name=nome_word,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        with c_pdf:
            doc_pdf = exportador.gerar_sd_pdf(plano_final)
            nome_pdf = f"SD_{tema[:15].replace(' ', '_').lower()}.pdf"
            st.download_button(
                "📕 Baixar em PDF",
                data=doc_pdf, file_name=nome_pdf,
                mime="application/pdf",
                use_container_width=True
            )"""

content = content.replace(old_download_btns, new_download_btns)

# ──────────────────────────────────────────────────────────────────────
# FIX 9: Aumentar objetivos de 5 para 8
# ──────────────────────────────────────────────────────────────────────
content = content.replace(
    "resultados = engine.buscar(texto=tema, faixa=faixa_filtro, campo=campo_filtro)[:5]",
    "resultados = engine.buscar(texto=tema, faixa=faixa_filtro, campo=campo_filtro)[:8]"
)

# ──────────────────────────────────────────────────────────────────────
# FIX 10: CSS extra — adicionar regras para chat e forçar cor de texto
# ──────────────────────────────────────────────────────────────────────
extra_css = """
/* ── Chat input forçado claro ── */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] div,
section[data-testid="stBottom"] {
    background-color: #F8FAFC !important;
    border-top: 1px solid #E2E8F0 !important;
}
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] input {
    background-color: #FFFFFF !important;
    color: #1E293B !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 10px !important;
}

/* ── Força texto visível em todo lugar ── */
.element-container,
[data-testid="stVerticalBlock"] p,
[data-testid="stVerticalBlock"] span,
[data-testid="stVerticalBlock"] div:not([class*="css"]) {
    color: #1E293B;
}

/* ── Download buttons padronizados (brancos com borda) ── */
[data-testid="stDownloadButton"] button {
    background: #FFFFFF !important;
    color: #374151 !important;
    border: 1.5px solid #D1D5DB !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
[data-testid="stDownloadButton"] button:hover {
    border-color: #10B981 !important;
    color: #059669 !important;
}
"""

# Inserir antes do fechamento do bloco de CSS
content = content.replace(
    "/* ── Cabeçalho / navegação ── */\n.pp-navbar {",
    extra_css + "\n/* ── Cabeçalho / navegação ── */\n.pp-navbar {"
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch cirúrgico aplicado!")
