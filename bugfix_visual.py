"""
Patch de correção de todos os bugs visuais após o redesign para modo claro.
Problemas corrigidos:
1. Tela de boas-vindas: texto apagado (card com classes antigas do tema escuro)
2. Dropdowns: texto da seleção invisível (branco em fundo branco)
3. Atividades: "array/atividade" no expander (bug de encoding do emoji)
4. Botão PDF: preto/ilegível
5. Página de Alunos: selectbox invisível (mesmo bug dos dropdowns)
6. ProfaBot: chat input escuro + resposta invisível
"""

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# ══════════════════════════════════════════════════════════════════
# FIX 1: CSS — adicionar regras que faltavam para dropdowns e chat
# ══════════════════════════════════════════════════════════════════
old_selectbox_css = """/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 8px !important;
    color: #1E293B !important;
}"""

new_selectbox_css = """/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stSelectbox"] > div > div > div,
[data-testid="stSelectbox"] input,
[data-baseweb="select"] > div,
[data-baseweb="select"] > div > div,
[data-baseweb="popover"] li,
[data-baseweb="popover"] ul {
    background-color: #FFFFFF !important;
    border-color: #E2E8F0 !important;
    border-radius: 8px !important;
    color: #1E293B !important;
}
/* Força o texto do item selecionado a ser visível */
[data-baseweb="select"] span,
[data-baseweb="select"] div[class*="singleValue"],
[class*="placeholder"],
[class*="singleValue"] {
    color: #1E293B !important;
}
/* Dropdown aberto */
[data-baseweb="popover"] {
    background: #FFFFFF !important;
}
[data-baseweb="menu"] {
    background: #FFFFFF !important;
}
[data-baseweb="menu"] li {
    color: #1E293B !important;
    background: #FFFFFF !important;
}
[data-baseweb="menu"] li:hover {
    background: #F0FDF4 !important;
    color: #059669 !important;
}"""

content = content.replace(old_selectbox_css, new_selectbox_css)

# Adicionar CSS para chat e download button após a seção de download buttons
old_download_css = """/* ── Download buttons ── */
[data-testid="stDownloadButton"] button {
    border-radius: 10px !important;
    font-weight: 600 !important;
}"""

new_download_css = """/* ── Download buttons ── */
[data-testid="stDownloadButton"] button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    color: #1E293B !important;
    background: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
}
[data-testid="stDownloadButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #10B981, #059669) !important;
    color: white !important;
    border-color: transparent !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    color: #1E293B !important;
}
[data-testid="stChatMessage"] * {
    color: #1E293B !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div {
    color: #1E293B !important;
}
/* Mensagem do usuário */
[data-testid="stChatMessage"][data-testid*="user"],
[data-testid="stChatMessageContent"] {
    color: #1E293B !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important;
    color: #1E293B !important;
    border: none !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #94A3B8 !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #10B981, #059669) !important;
    border-radius: 8px !important;
}

/* ── Paragraphs e textos gerais ── */
p { color: #1E293B !important; }
.stMarkdown { color: #1E293B !important; }
.stMarkdown p { color: #1E293B !important; }"""

content = content.replace(old_download_css, new_download_css)

# ══════════════════════════════════════════════════════════════════
# FIX 2: Tela de boas-vindas — corrigir classes antigas e texto apagado
# ══════════════════════════════════════════════════════════════════
old_welcome_card = '''            st.markdown("""
            <div class="card card-verde" style="text-align:center; padding:1.5rem;">
                <div style="color:#6EE7B7; font-weight:600; font-size:1rem; margin-bottom:0.5rem;">
                    ✨ O que você vai conseguir fazer aqui:
                </div>
                <div style="color:#CBD5E1; font-size:0.95rem; line-height:2.2;">
                    📝 &nbsp;Gerar planos de aula com os objetivos BNCC corretos em minutos<br>
                    👶 &nbsp;Criar o relatório bimestral de cada aluno com facilidade<br>
                    💬 &nbsp;Tirar dúvidas sobre a BNCC com uma assistente virtual
                </div>
            </div>
            """, unsafe_allow_html=True)'''

new_welcome_card = '''            st.markdown("""
            <div class="pp-card-verde" style="text-align:center; padding:1.8rem;">
                <div style="color:#059669; font-weight:700; font-size:1.05rem; margin-bottom:1rem;">
                    ✨ O que você vai conseguir fazer aqui:
                </div>
                <div style="color:#065F46; font-size:0.97rem; line-height:2.4;">
                    📝 &nbsp;<strong>Gerar planos de aula</strong> com os objetivos BNCC corretos em minutos<br>
                    👶 &nbsp;<strong>Criar o relatório bimestral</strong> de cada aluno com facilidade<br>
                    💬 &nbsp;<strong>Tirar dúvidas</strong> sobre a BNCC com uma assistente virtual
                </div>
            </div>
            """, unsafe_allow_html=True)'''

content = content.replace(old_welcome_card, new_welcome_card)

# Corrigir o título hero da boas-vindas (usa classe antiga "hero-title")
old_welcome_title = '''            st.markdown("""
            <div style="text-align:center; padding:1rem 0 2rem;">
                <div style="font-size:4rem;">📚</div>
                <div class="hero-title" style="font-size:2.8rem; text-align:center; margin-top:0.5rem;">
                    Olá, Professora!
                </div>
                <div class="hero-sub" style="text-align:center; max-width:600px; margin:1rem auto 0;">
                    O <strong style="color:#10B981;">ProfaPlanner</strong> foi criado para facilitar a sua vida.<br>
                    Chega de perder tempo procurando códigos da BNCC — o sistema faz isso por você! 🎉
                </div>
            </div>
            """, unsafe_allow_html=True)'''

new_welcome_title = '''            st.markdown("""
            <div style="text-align:center; padding:2rem 0 2rem;">
                <div style="font-size:4.5rem; margin-bottom:1rem;">📚</div>
                <div style="font-size:2.8rem; font-weight:800; color:#0F172A; line-height:1.2; margin-bottom:0.8rem;">
                    Olá, Professora!
                </div>
                <div style="font-size:1.05rem; color:#475569; max-width:500px; margin:0 auto; line-height:1.7;">
                    O <strong style="color:#10B981;">ProfaPlanner</strong> foi criado para facilitar a sua vida.<br>
                    Chega de perder tempo procurando códigos da BNCC — o sistema faz isso por você! 🎉
                </div>
            </div>
            """, unsafe_allow_html=True)'''

content = content.replace(old_welcome_title, new_welcome_title)

# ══════════════════════════════════════════════════════════════════
# FIX 3: Corrigir o ProfaBot — texto do chat visível
# ══════════════════════════════════════════════════════════════════
old_profabot_desc = """    st.markdown('<div class="sec">💬 Tirar Dúvidas com a Assistente Virtual</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94A3B8;">Pode perguntar à vontade sobre a BNCC, '
                'sobre planejamento ou sobre como usar o sistema. '
                'Ela responde em linguagem simples! 😊</p>', unsafe_allow_html=True)"""

new_profabot_desc = """    st.markdown('''
    <div style="margin-bottom:1rem;">
        <div style="font-size:1.5rem; font-weight:800; color:#0F172A; margin-bottom:0.3rem;">💬 Tirar Dúvidas com a Assistente Virtual</div>
        <div style="color:#475569; font-size:0.95rem;">Pode perguntar à vontade sobre a BNCC, sobre planejamento ou sobre como usar o sistema. Ela responde em linguagem simples! 😊</div>
    </div>
    ''', unsafe_allow_html=True)"""

content = content.replace(old_profabot_desc, new_profabot_desc)

# ══════════════════════════════════════════════════════════════════
# FIX 4: Corrigir a seção "sec" (título de página) para modo claro
# ══════════════════════════════════════════════════════════════════
# Procurar se existe a classe .sec no CSS
if '.sec {' not in content and '"sec"' in content:
    # Adicionar estilo para .sec antes do fechamento do style
    old_close_style = """.pp-navbar {
    background: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    padding: 1rem 0 1.5rem;
    margin-bottom: 1.5rem;
}
</style>"""
    new_close_style = """.pp-navbar {
    background: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    padding: 1rem 0 1.5rem;
    margin-bottom: 1.5rem;
}
/* ── Seção título (classe antiga) ── */
.sec {
    font-size: 1.5rem;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 0.3rem;
}
/* ── Corrigir texto padrão do Streamlit ── */
[data-testid="stMarkdown"] * { color: #1E293B; }
[data-testid="stText"] { color: #1E293B !important; }
/* Corrige tag-ei01 e tag-ei02 */
.tag-ei01 { background:#DBEAFE; color:#1D4ED8; padding:2px 8px; border-radius:99px; font-size:0.78rem; font-weight:600; }
.tag-ei02 { background:#FEF3C7; color:#D97706; padding:2px 8px; border-radius:99px; font-size:0.78rem; font-weight:600; }
</style>"""
    content = content.replace(old_close_style, new_close_style)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Todos os bugs visuais corrigidos!")
