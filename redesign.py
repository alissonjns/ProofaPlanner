"""
Script de redesign completo do ProfaPlanner:
- Muda para tema claro (fundo branco/creme)
- Reforma a página pagina_plano_aula para fluxo guiado em 3 etapas
"""

import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# ──────────────────────────────────────────────────────────
# 1. SUBSTITUIR O BLOCO DE CSS POR UM TEMA CLARO PROFISSIONAL
# ──────────────────────────────────────────────────────────
old_css = '''# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Remove margin around main container to look cleaner */
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 900px; }

/* Esconde menu do Streamlit Cloud */
#MainMenu {visibility: hidden;}
header {display: none !important;}
footer {display: none !important;}
.viewerBadge_container__1QSob {display: none !important;}
[data-testid="manage-app-button"] {display: none !important;}

/* Correção para o Bug do Google Tradutor (_arrowRight_) */
</style>
<meta name="google" content="notranslate">
""", unsafe_allow_html=True)'''

new_css = '''# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Reset & Base ── */
* { font-family: 'Inter', sans-serif !important; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #F8FAFC !important;
    color: #1E293B !important;
}
.block-container { 
    padding-top: 2rem; padding-bottom: 3rem; max-width: 960px; 
    background-color: #F8FAFC;
}

/* ── Esconde elementos do Streamlit Cloud ── */
#MainMenu {visibility: hidden;}
header {display: none !important;}
footer {display: none !important;}
.viewerBadge_container__1QSob {display: none !important;}
[data-testid="manage-app-button"] {display: none !important;}

/* ── Fundo geral forçado ── */
[data-testid="stMain"] { background-color: #F8FAFC !important; }

/* ── Divider ── */
hr { border-color: #E2E8F0 !important; }

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 8px !important;
    color: #1E293B !important;
    font-size: 0.92rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #10B981 !important;
    box-shadow: 0 0 0 3px rgba(16,185,129,0.12) !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 8px !important;
    color: #1E293B !important;
}

/* ── Labels ── */
label, [data-testid="stWidgetLabel"] {
    color: #475569 !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
}

/* ── Primary buttons ── */
[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #10B981, #059669) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.5rem !important;
    box-shadow: 0 4px 15px rgba(16,185,129,0.3) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stButton"] button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(16,185,129,0.4) !important;
}

/* ── Secondary buttons ── */
[data-testid="stButton"] button[kind="secondary"] {
    background: #FFFFFF !important;
    color: #475569 !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
}
[data-testid="stButton"] button[kind="secondary"]:hover {
    border-color: #10B981 !important;
    color: #10B981 !important;
}

/* ── Download buttons ── */
[data-testid="stDownloadButton"] button {
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ── Checkboxes ── */
[data-testid="stCheckbox"] { color: #1E293B !important; }
[data-testid="stCheckbox"] label { color: #334155 !important; font-size: 0.88rem !important; }

/* ── Expanders ── */
[data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 12px !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stExpander"] summary {
    color: #1E293B !important;
    font-weight: 600 !important;
}

/* ── Info / warning / success ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left-width: 4px !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #F1F5F9 !important;
    border-radius: 10px !important;
    padding: 4px !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    color: #64748B !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background-color: #FFFFFF !important;
    color: #10B981 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] { 
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
}

/* ── Pills navigation ── */
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
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #10B981 !important; }

/* ── Progress bar ── */
.prog-bar-bg { background:#E2E8F0; border-radius:99px; height:6px; overflow:hidden; }
.prog-bar { background: linear-gradient(90deg, #10B981, #34D399); height:100%; border-radius:99px; transition:width 0.4s ease; }

/* ── Custom cards ── */
.pp-card {
    background: #FFFFFF;
    border: 1.5px solid #E2E8F0;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.pp-card-verde {
    background: linear-gradient(135deg, #ECFDF5, #F0FDF4);
    border: 1.5px solid #A7F3D0;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.pp-card-coral {
    background: linear-gradient(135deg, #FFF7ED, #FFEDD5);
    border: 1.5px solid #FED7AA;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.pp-card-azul {
    background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
    border: 1.5px solid #BFDBFE;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.pp-step {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.8rem 1.2rem;
    border-radius: 99px;
    font-size: 0.88rem;
    font-weight: 600;
}
.pp-step-active {
    background: linear-gradient(135deg, #10B981, #059669);
    color: white;
    box-shadow: 0 4px 15px rgba(16,185,129,0.3);
}
.pp-step-done {
    background: #ECFDF5;
    color: #059669;
    border: 1.5px solid #A7F3D0;
}
.pp-step-pending {
    background: #F8FAFC;
    color: #94A3B8;
    border: 1.5px solid #E2E8F0;
}
.pp-step-num {
    width: 26px; height: 26px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 700;
}
.pp-hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.2;
}
.pp-hero-sub {
    font-size: 1rem;
    color: #64748B;
    line-height: 1.6;
}
.pp-section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0.5rem;
}
.pp-tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 0.78rem;
    font-weight: 600;
}
.pp-tag-verde { background: #ECFDF5; color: #059669; }
.pp-tag-coral { background: #FFF7ED; color: #EA580C; }
.pp-tag-azul  { background: #EFF6FF; color: #2563EB; }
.pp-obj-card {
    background: #FFFFFF;
    border: 1.5px solid #E2E8F0;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    transition: border-color 0.2s ease;
}
.pp-obj-card:hover { border-color: #10B981; }
.pp-divider { height: 1px; background: #E2E8F0; margin: 1.5rem 0; }

/* ── Cabeçalho / navegação ── */
.pp-navbar {
    background: #FFFFFF;
    border-bottom: 1px solid #E2E8F0;
    padding: 1rem 0 1.5rem;
    margin-bottom: 1.5rem;
}
</style>
<meta name="google" content="notranslate">
""", unsafe_allow_html=True)'''

content = content.replace(old_css, new_css)

# ──────────────────────────────────────────────────────────
# 2. SUBSTITUIR O NAVBAR PELO NOVO DESIGN
# ──────────────────────────────────────────────────────────
old_navbar = """if not _NA_TOUR:
    st.markdown(\"\"\"
    <div style='display:flex; align-items:center; gap:12px; margin-bottom: 2rem;'>
        <div style='font-size:2.8rem;'>📚</div>
        <div>
            <div style='font-size:1.8rem; font-weight:700; color:#10B981; line-height:1.1;'>ProfaPlanner</div>
            <div style='font-size:0.75rem; color:#475569; letter-spacing:1px; font-weight:600;'>BNCC · EDUCAÇÃO INFANTIL</div>
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)"""

new_navbar = """if not _NA_TOUR:
    st.markdown(\"\"\"
    <div class='pp-navbar' style='display:flex; align-items:center; gap:14px;'>
        <div style='width:46px; height:46px; background:linear-gradient(135deg,#10B981,#059669); border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:1.4rem; box-shadow:0 4px 12px rgba(16,185,129,0.3);'>📚</div>
        <div>
            <div style='font-size:1.5rem; font-weight:800; color:#0F172A; line-height:1;'>ProfaPlanner</div>
            <div style='font-size:0.72rem; color:#10B981; letter-spacing:1.5px; font-weight:700; text-transform:uppercase;'>BNCC · Educação Infantil</div>
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)"""

content = content.replace(old_navbar, new_navbar)

# ──────────────────────────────────────────────────────────
# 3. SUBSTITUIR A FUNÇÃO pagina_plano_aula COMPLETA
# ──────────────────────────────────────────────────────────
# Encontrar onde começa e termina a função pagina_plano_aula
import re

# Encontrar a função pagina_plano_aula
start_marker = "def pagina_plano_aula():"
end_marker = "\n\n# ──────────────────────────────────────────────────────────────────────────────\n\ndef pagina_alunos():"

start_idx = content.find(start_marker)
end_idx = content.find("def pagina_alunos():")
# Captura tudo de "def pagina_plano_aula" até "def pagina_alunos"
old_func = content[start_idx:end_idx].rstrip()

new_func = '''def pagina_plano_aula():
    # ── Inicializar estado do fluxo ──────────────────────────────────────────
    if "plano_step" not in st.session_state:
        st.session_state.plano_step = 1
    if "objetivos_selecionados" not in st.session_state:
        st.session_state.objetivos_selecionados = []
    if "plano_gerado" not in st.session_state:
        st.session_state.plano_gerado = None

    step = st.session_state.plano_step

    # ── Cabeçalho ─────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='margin-bottom:1.5rem;'>
        <div class='pp-hero-title'>✨ Criar Sequência Didática</div>
        <div class='pp-hero-sub'>Siga os 3 passos abaixo e a IA escreve o plano completo para você!</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Barra de Progresso em 3 Etapas ────────────────────────────────────────
    s1 = "pp-step-active" if step == 1 else ("pp-step-done" if step > 1 else "pp-step-pending")
    s2 = "pp-step-active" if step == 2 else ("pp-step-done" if step > 2 else "pp-step-pending")
    s3 = "pp-step-active" if step == 3 else ("pp-step-done" if step > 3 else "pp-step-pending")
    n1 = "✓" if step > 1 else "1"
    n2 = "✓" if step > 2 else "2"
    n3 = "✓" if step > 3 else "3"

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="pp-step {s1}">
            <span class="pp-step-num" style="background:rgba(255,255,255,0.25);">{n1}</span>
            📝 Dados da Aula
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="pp-step {s2}">
            <span class="pp-step-num" style="background:rgba(255,255,255,0.25);">{n2}</span>
            🎯 Objetivos BNCC
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="pp-step {s3}">
            <span class="pp-step-num" style="background:rgba(255,255,255,0.25);">{n3}</span>
            🤖 Plano Gerado
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='pp-divider'></div>", unsafe_allow_html=True)

    _faixas = {"EI01": "👶 Bebês (0 a 1a6m)", "EI02": "🧒 Crianças (1a7m a 3a11m)", "Ambas": "Mista"}
    _campos = {
        "Todos": "🔍 Todos os campos",
        "EO": "🤝 O eu, o outro e o nós",
        "CG": "🏃 Corpo, gestos e movimentos",
        "TS": "🎨 Traços, sons, cores e formas",
        "EF": "💬 Escuta, fala, pensamento e imaginação",
        "ET": "🔢 Espaços, tempos, quantidades e transformações",
    }

    # ══════════════════════════════════════════════════════════════════════════
    # ETAPA 1 — DADOS DA AULA
    # ══════════════════════════════════════════════════════════════════════════
    if step == 1:
        st.markdown("<div class='pp-section-title'>📝 Sobre a Sequência Didática</div>", unsafe_allow_html=True)
        st.markdown("<div class='pp-card'>", unsafe_allow_html=True)

        titulo_sd = st.text_input(
            "Título da Sequência *",
            placeholder="Ex: Descobrindo meu corpo através das brincadeiras",
            help="Dê um nome criativo à sua SD"
        )

        c_seg, c_faixa = st.columns(2)
        with c_seg:
            segmento = st.selectbox(
                "Segmento / Turma",
                ["Berçário 1", "Berçário 2", "Maternal 1", "Maternal 2", "Pré 1", "Pré 2"]
            )
        with c_faixa:
            faixa_sel = st.selectbox("Faixa Etária", options=list(_faixas.keys()), format_func=lambda x: _faixas[x])

        c_dur, c_camp = st.columns(2)
        with c_dur:
            duracao = st.selectbox("⏱️ Duração da SD", ["Diário", "Semanal", "Quinzenal", "Mensal", "Bimestral"])
        with c_camp:
            campo_sel = st.selectbox("Campo Principal de Experiência", options=list(_campos.keys()), format_func=lambda x: _campos[x])

        tema = st.text_input(
            "🎯 Tema / Atividade Central *",
            placeholder="Ex: Brincadeira com argila e água",
            help="O tema principal que será trabalhado na sequência"
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # Guarda na sessão para usar nas próximas etapas
        st.session_state._sd_titulo = titulo_sd
        st.session_state._sd_segmento = segmento
        st.session_state._sd_faixa = faixa_sel
        st.session_state._sd_duracao = duracao
        st.session_state._sd_campo = campo_sel
        st.session_state._sd_tema = tema

        if tema.strip():
            _, col_btn, _ = st.columns([1, 2, 1])
            with col_btn:
                if st.button("Próximo: Encontrar objetivos BNCC →", type="primary", use_container_width=True):
                    st.session_state.plano_step = 2
                    st.rerun()
        else:
            st.markdown("""
            <div class='pp-card-coral' style='padding:1rem;'>
                <span style='color:#EA580C; font-weight:600;'>💡 Dica:</span>
                <span style='color:#9A3412;'> Preencha o "Tema" para avançar para os objetivos BNCC!</span>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ETAPA 2 — OBJETIVOS BNCC
    # ══════════════════════════════════════════════════════════════════════════
    elif step == 2:
        tema = st.session_state.get("_sd_tema", "")
        faixa_sel = st.session_state.get("_sd_faixa", "EI01")
        campo_sel = st.session_state.get("_sd_campo", "Todos")

        st.markdown(f"""
        <div class='pp-card-verde' style='padding:1rem 1.4rem;'>
            <span style='color:#059669; font-weight:600;'>🎯 Tema selecionado:</span>
            <span style='color:#065F46; font-size:1.05rem; font-weight:700;'> {tema}</span>
        </div>
        """, unsafe_allow_html=True)

        faixa_filtro = None if faixa_sel == "Ambas" else faixa_sel
        campo_filtro = None if campo_sel == "Todos" else campo_sel

        with st.spinner("🔍 Buscando os objetivos BNCC mais relevantes..."):
            resultados = engine.buscar(texto=tema, faixa=faixa_filtro, campo=campo_filtro)[:5]

        if resultados:
            st.markdown("""
            <div class='pp-section-title'>
                🎯 Objetivos BNCC encontrados — marque os que se aplicam à sua SD:
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='color:#64748B; font-size:0.85rem; margin-bottom:0.8rem;'>Todos já vêm marcados. Desmarque se não quiser incluir algum.</div>", unsafe_allow_html=True)

            selecionados = []
            for obj in resultados:
                campo_nome = _campos.get(obj.get('campo', ''), obj.get('campo', ''))
                col_chk, col_info = st.columns([0.05, 0.95])
                with col_chk:
                    checked = st.checkbox("", value=True, key=f"obj_{obj['codigo']}", label_visibility="collapsed")
                with col_info:
                    st.markdown(f"""
                    <div class="pp-obj-card" style="{'border-color:#10B981; background:#ECFDF5;' if True else ''}">
                        <div style='display:flex; align-items:center; gap:8px; margin-bottom:4px;'>
                            <span style='background:#10B981; color:white; padding:2px 8px; border-radius:6px; font-size:0.78rem; font-weight:700;'>{obj['codigo']}</span>
                            <span class='pp-tag pp-tag-verde'>{campo_nome}</span>
                        </div>
                        <div style='color:#1E293B; font-size:0.88rem; line-height:1.5;'>{obj['descricao']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                if checked:
                    selecionados.append(obj)

            st.session_state.objetivos_selecionados = selecionados

            st.markdown("<div class='pp-divider'></div>", unsafe_allow_html=True)

            c_back, c_next = st.columns(2)
            with c_back:
                if st.button("← Voltar e editar dados", use_container_width=True):
                    st.session_state.plano_step = 1
                    st.rerun()
            with c_next:
                if selecionados:
                    if st.button(f"🤖 Gerar Plano com IA ({len(selecionados)} objetivo(s)) →", type="primary", use_container_width=True):
                        with st.spinner("✨ A IA está escrevendo sua Sequência Didática completa... isso pode levar uns 15 segundos!"):
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
                                st.session_state.plano_step = 3
                                st.rerun()
                            else:
                                st.error("Houve um erro ao gerar o plano. Tente novamente.")
                else:
                    st.warning("Selecione pelo menos 1 objetivo para continuar.")
        else:
            st.warning("Não encontrei objetivos para essas palavras. Volte e tente um tema diferente.")
            if st.button("← Voltar"):
                st.session_state.plano_step = 1
                st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # ETAPA 3 — PLANO GERADO (REVISÃO E DOWNLOAD)
    # ══════════════════════════════════════════════════════════════════════════
    elif step == 3:
        pg = st.session_state.plano_gerado
        tema = st.session_state.get("_sd_tema", "")
        faixa_sel = st.session_state.get("_sd_faixa", "EI01")
        campo_sel = st.session_state.get("_sd_campo", "Todos")
        segmento = st.session_state.get("_sd_segmento", "")
        duracao = st.session_state.get("_sd_duracao", "Diário")
        titulo_sd = st.session_state.get("_sd_titulo", "Sequência Didática")

        st.markdown("""
        <div class='pp-card-verde' style='padding:1.2rem 1.5rem;'>
            <div style='display:flex; align-items:center; gap:10px;'>
                <span style='font-size:1.8rem;'>🎉</span>
                <div>
                    <div style='font-weight:700; color:#065F46; font-size:1.05rem;'>Plano criado com sucesso!</div>
                    <div style='color:#059669; font-size:0.88rem;'>Revise abaixo e baixe quando estiver pronto.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Resumo rápido
        col_j, col_o = st.columns(2)
        with col_j:
            st.markdown("<div class='pp-section-title'>📖 Justificativa</div>", unsafe_allow_html=True)
            justificativa = st.text_area("Justificativa", value=pg.get("justificativa", ""), height=120, label_visibility="collapsed")
        with col_o:
            st.markdown("<div class='pp-section-title'>🎯 Objetivo Geral</div>", unsafe_allow_html=True)
            obj_geral = st.text_area("Objetivo Geral", value=pg.get("obj_geral", ""), height=120, label_visibility="collapsed")

        st.markdown("<div class='pp-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='pp-section-title'>🧩 Atividades Propostas</div>", unsafe_allow_html=True)
        st.markdown("<div style='color:#64748B; font-size:0.85rem; margin-bottom:0.8rem;'>Clique em cada atividade para expandir e editar.</div>", unsafe_allow_html=True)

        atividades = []
        for i, ativ in enumerate(pg.get("atividades", [])):
            with st.expander(f"🧩 Atividade {i+1}: {ativ.get('nome', '')}", expanded=False):
                nome_a = st.text_input("Nome da Atividade", value=ativ.get("nome", ""), key=f"n_{i}")
                desc_a = st.text_area("Passo a Passo Detalhado", value=ativ.get("descricao", ""), height=150, key=f"d_{i}")
                atividades.append({"nome": nome_a, "descricao": desc_a})

        st.markdown("<div class='pp-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='pp-section-title'>📊 Avaliação e Registro</div>", unsafe_allow_html=True)
        avaliacao = st.text_area("Como o aprendizado será observado e registrado", value=pg.get("avaliacao", ""), height=100, label_visibility="collapsed")

        # Feedback para IA
        st.markdown("""
        <div class='pp-card-azul' style='padding:1.2rem; margin-top:1rem;'>
            <div style='font-weight:700; color:#1D4ED8; margin-bottom:0.4rem;'>🤖 Quer ajustar algo?</div>
            <div style='color:#1E40AF; font-size:0.88rem;'>Diga à IA o que deve mudar e ela reescreve o plano para você!</div>
        </div>
        """, unsafe_allow_html=True)
        feedback_ia = st.text_input("O que você quer mudar?", placeholder="Ex: As atividades estão muito complexas para bebês, inclua mais músicas e movimentos suaves.")

        c_refazer, _ = st.columns([1, 2])
        with c_refazer:
            if feedback_ia and st.button("🔄 Refazer com IA", type="primary", use_container_width=True):
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

        st.markdown("<div class='pp-divider'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size:1.05rem; font-weight:700; color:#0F172A; margin-bottom:0.8rem;'>
            ⬇️ Tudo certo? Baixe seu documento!
        </div>
        """, unsafe_allow_html=True)

        plano_final = {
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
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🆕 Criar nova Sequência Didática", use_container_width=False):
            for k in ["plano_step", "plano_gerado", "objetivos_selecionados", "_sd_tema", "_sd_titulo",
                      "_sd_faixa", "_sd_campo", "_sd_segmento", "_sd_duracao", "plano_atual"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()
'''

content = content[:start_idx] + new_func + "\n\n\n" + content[end_idx:]

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Redesign completo aplicado com sucesso!")
