"""
ProfaPlanner — Assistente de Planejamento Pedagógico BNCC
Educação Infantil · EI01 e EI02
"""

import io
import random
from pathlib import Path

import streamlit as st

from modules.bncc_engine import BNCCEngine
from modules.chatbot import ProfaBot
from modules.exportador import Exportador

# ─── Configuração da Página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="ProfaPlanner | Seu assistente de planejamento",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
* { font-family: 'Outfit', sans-serif !important; }

/* Fundo geral mais sofisticado */
.stApp {
    background: radial-gradient(circle at top left, #1E293B, #0F172A 40%, #0B1120 100%) !important;
}

/* Esconde sidebar durante o tour */
.sidebar-oculta [data-testid="stSidebar"] { display: none !important; }

/* Sidebar Glassmorphism */
[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.7) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* Botões da Sidebar com efeito elegante */
[data-testid="stSidebar"] .stButton > button {
    text-align: left !important;
    border-radius: 12px !important;
    border: 1px solid transparent !important;
    font-weight: 500 !important;
    background: transparent !important;
    color: #CBD5E1 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    padding: 0.5rem 1rem !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255, 255, 255, 0.05) !important;
    border-color: rgba(255, 255, 255, 0.1) !important;
    color: #F8FAFC !important;
    transform: translateX(4px);
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%) !important;
    border-left: 3px solid #10B981 !important;
    color: #10B981 !important;
}

/* Inputs Premium */
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
    background: rgba(30, 41, 59, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #F8FAFC !important;
    border-radius: 10px !important;
    backdrop-filter: blur(8px);
    transition: all 0.2s;
}
.stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
    border-color: #10B981 !important;
    box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2) !important;
}

/* Cards Glassmorphism */
.card {
    background: rgba(30, 41, 59, 0.5);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}
.card:hover { 
    border-color: rgba(16, 185, 129, 0.4); 
    box-shadow: 0 8px 32px rgba(16, 185, 129, 0.1); 
    transform: translateY(-2px);
}
.card-verde { background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(30, 41, 59, 0.5)); border-color: rgba(16, 185, 129, 0.3); }
.card-azul  { background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(30, 41, 59, 0.5)); border-color: rgba(37, 99, 235, 0.3); }

/* Badges */
.badge-bncc {
    display: inline-block;
    background: #064E3B; color: #6EE7B7;
    border: 1px solid #059669; border-radius: 6px;
    padding: 1px 7px; font-size: 0.72rem; font-weight: 700;
    font-family: 'Courier New', monospace !important; letter-spacing: 0.5px;
}
.tag-ei01 { background:#1E3A5F; color:#93C5FD; border:1px solid #2563EB44; border-radius:20px; padding:2px 10px; font-size:0.78rem; font-weight:600; }
.tag-ei02 { background:#3B1F5E; color:#C4B5FD; border:1px solid #7C3AED44; border-radius:20px; padding:2px 10px; font-size:0.78rem; font-weight:600; }

/* Botões Principais */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #10B981, #059669) !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    padding: 0.6rem 2rem !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    transition: all 0.3s ease !important;
}
.stButton > button[kind="primary"]:hover { 
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
}

/* Hero Title com Gradiente Premium */
.hero-title {
    font-size: 2.8rem; font-weight: 700; letter-spacing: -0.5px;
    background: linear-gradient(135deg, #34D399 0%, #059669 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub { color: #94A3B8; font-size: 1.15rem; margin-top: 0.5rem; font-weight: 300; }

/* Seção */
.sec { font-size: 1.15rem; font-weight: 700; color: #F8FAFC; border-left: 4px solid #10B981; padding-left: 0.75rem; margin: 1.5rem 0 1rem; border-radius: 2px; }

/* Tour */
.tour-card {
    background: rgba(15, 23, 42, 0.8);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px; padding: 2rem 1.5rem;
    text-align: center; display: flex;
    flex-direction: column; align-items: center; gap: 1rem;
    height: 220px; justify-content: center;
    transition: all 0.3s;
}
.tour-card:hover { border-color: rgba(16, 185, 129, 0.5); transform: translateY(-4px); box-shadow: 0 10px 30px rgba(0,0,0,0.2); }

/* Progress bar tour */
.prog-bar-bg { background: rgba(30, 41, 59, 0.8); border-radius:99px; height:8px; width:100%; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1); }
.prog-bar    { background:linear-gradient(90deg,#10B981,#34D399); border-radius:99px; height:8px; transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 0 10px rgba(16, 185, 129, 0.5); }

/* Chat */
[data-testid="stChatMessage"] { background: rgba(30, 41, 59, 0.4)!important; border:1px solid rgba(255,255,255,0.05)!important; border-radius:12px!important; margin-bottom:0.75rem!important; backdrop-filter: blur(8px); }
[data-testid="stTab"] { color:#94A3B8!important; font-weight: 500!important; }
[data-testid="stTab"][aria-selected="true"] { color:#10B981!important; }
[data-testid="stExpander"] { background: rgba(30, 41, 59, 0.6)!important; border:1px solid rgba(255,255,255,0.1)!important; border-radius:12px!important; }
#MainMenu, footer { visibility: hidden; }
hr { border-color: rgba(255,255,255,0.05)!important; margin:1.5rem 0!important; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
_def = {
    "pagina": "boas_vindas",   # começa no tour obrigatório
    "tour_step": 1,
    "alunos": [],
    "historico_chat": [],
    "modelo_escola": None,
    "plano_atual": {},
    "gemini_key": "",
}
for _k, _v in _def.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ─── Motor BNCC ───────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Carregando base BNCC...")
def _engine():
    return BNCCEngine()
engine = _engine()


# ─── Detecta documentos na pasta do projeto ───────────────────────────────────
def detectar_arquivos_locais() -> list[Path]:
    """Retorna .docx e .xlsx encontrados na mesma pasta do app.py"""
    pasta = Path(__file__).parent
    return sorted(
        [f for f in pasta.iterdir()
         if f.suffix.lower() in (".docx", ".xlsx", ".xls", ".doc")],
        key=lambda f: f.name
    )


# ─── Top Navigation ─────────────────────────────────────────────────────────────
_NA_TOUR = st.session_state.pagina == "boas_vindas"

if not _NA_TOUR:
    st.markdown("""
    <div style='display:flex; align-items:center; gap:12px; margin-bottom: 2rem;'>
        <div style='font-size:2.8rem;'>📚</div>
        <div>
            <div style='font-size:1.8rem; font-weight:700; color:#10B981; line-height:1.1;'>ProfaPlanner</div>
            <div style='font-size:0.75rem; color:#475569; letter-spacing:1px; font-weight:600;'>BNCC · EDUCAÇÃO INFANTIL</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _nav_options = {
        "🏠 Início": "inicio",
        "📋 Meu Modelo": "modelo",
        "✏️ Criar Plano": "plano",
        "👶 Alunos": "alunos",
        "💬 ProfaBot": "profabot"
    }

    # Pegar a chave atual pelo valor
    current_key = next((k for k, v in _nav_options.items() if v == st.session_state.pagina), "🏠 Início")

    selected = st.pills(
        "Navegação",
        options=list(_nav_options.keys()),
        default=current_key,
        label_visibility="collapsed"
    )

    if selected and _nav_options[selected] != st.session_state.pagina:
        st.session_state.pagina = _nav_options[selected]
        st.rerun()

    st.divider()


# ═══════════════════════════════════════════════════════════════════════════════
#  TOUR OBRIGATÓRIO DE BOAS-VINDAS
# ═══════════════════════════════════════════════════════════════════════════════
def pagina_boas_vindas():
    # Esconde sidebar durante o tour
    st.markdown("""<style>[data-testid="stSidebar"]{display:none!important}</style>""",
                unsafe_allow_html=True)

    step = st.session_state.tour_step

    # ── Barra de progresso ────────────────────────────────────────────────
    pct = int((step / 3) * 100)
    st.markdown(f"""
    <div style="max-width:700px; margin:0 auto 2rem;">
        <div style="display:flex; justify-content:space-between; color:#475569; font-size:0.78rem; margin-bottom:6px;">
            <span>Apresentação do sistema</span>
            <span>Passo {step} de 3</span>
        </div>
        <div class="prog-bar-bg"><div class="prog-bar" style="width:{pct}%"></div></div>
    </div>
    """, unsafe_allow_html=True)

    col_c, _ = st.columns([2, 1])  # centraliza conteúdo
    with col_c:

        # ── PASSO 1: Boas-vindas ──────────────────────────────────────────
        if step == 1:
            st.markdown("""
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
            """, unsafe_allow_html=True)

            st.markdown("""
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
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Próximo →  Entender como funciona", type="primary", use_container_width=True):
                st.session_state.tour_step = 2
                st.rerun()

        # ── PASSO 2: Como funciona ────────────────────────────────────────
        elif step == 2:
            st.markdown("""
            <div class="hero-title" style="font-size:2rem; text-align:center; margin-bottom:1.5rem;">
                Como o sistema funciona?
            </div>
            """, unsafe_allow_html=True)

            _passos = [
                ("📋", "card-azul",  "1. Você coloca o modelo da escola",
                 "Se a escola te deu um formulário de plano de aula no Word ou Excel, você o adiciona aqui. "
                 "O sistema usa ele como base. Se não tiver, usamos um modelo pronto."),
                ("✏️", "card-verde", "2. Você digita o tema da aula",
                 "Escreve o tema que você planejou, como \"Brincadeira com argila\" ou \"Música e ritmo\". "
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
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("← Voltar", use_container_width=True):
                    st.session_state.tour_step = 1
                    st.rerun()
            with c2:
                if st.button("Próximo →  Começar agora", type="primary", use_container_width=True):
                    st.session_state.tour_step = 3
                    st.rerun()

        # ── PASSO 3: Começar ──────────────────────────────────────────────
        elif step == 3:
            st.markdown("""
            <div class="hero-title" style="font-size:2rem; text-align:center; margin-bottom:0.5rem;">
                Tudo pronto! 🎉
            </div>
            <div class="hero-sub" style="text-align:center; margin-bottom:1.5rem;">
                Por onde você quer começar?
            </div>
            """, unsafe_allow_html=True)

            _opcoes = [
                ("modelo",   "📋", "Carregar o modelo da escola",
                 "Tenho o arquivo que a escola me deu e quero carregá-lo"),
                ("plano",    "✏️", "Criar meu primeiro plano de aula",
                 "Quero digitar o tema de uma aula e gerar o documento agora"),
                ("profabot", "💬", "Fazer uma pergunta sobre a BNCC",
                 "Tenho uma dúvida e quero perguntar para a assistente virtual"),
            ]
            for pag, icon, titulo, desc in _opcoes:
                st.markdown(f"""
                <div class="card" style="padding:1rem 1.3rem; display:flex; align-items:center; gap:1rem;">
                    <div style="font-size:2rem; flex-shrink:0;">{icon}</div>
                    <div>
                        <div style="font-weight:700; color:#F1F5F9;">{titulo}</div>
                        <div style="color:#64748B; font-size:0.85rem;">{desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Ir para: {titulo}", key=f"tour_ir_{pag}",
                             use_container_width=True, type="primary"):
                    st.session_state.pagina = pag
                    st.session_state.tour_step = 1
                    st.rerun()
                st.markdown("<br style='margin:0'>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("← Voltar", use_container_width=False):
                st.session_state.tour_step = 2
                st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  PÁGINAS PRINCIPAIS
# ═══════════════════════════════════════════════════════════════════════════════

def pagina_inicio():
    st.markdown('<div class="hero-title">Olá, Professora! 👋</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Escolha o que você quer fazer hoje:</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    _atalhos = [
        ("plano",    "✏️", "Criar Plano de Aula",
         "Digite o tema da aula e o sistema monta o plano com os objetivos BNCC certos", "card-verde"),
        ("alunos",   "👶", "Relatório dos Alunos",
         "Registre como cada aluno está se desenvolvendo e gere o relatório bimestral", "card-azul"),
        ("profabot", "💬", "Tirar uma Dúvida",
         "Pergunte qualquer coisa sobre a BNCC ou sobre como usar o sistema", "card-roxo"),
    ]
    for col, (pag, icon, titulo, desc, cls) in zip([c1, c2, c3], _atalhos):
        with col:
            st.markdown(f"""<div class="card {cls}">
                <div style="font-size:2rem; margin-bottom:0.5rem;">{icon}</div>
                <div style="font-weight:700; color:#F1F5F9; margin-bottom:0.3rem; font-size:1rem;">{titulo}</div>
                <div style="color:#475569; font-size:0.82rem; line-height:1.5;">{desc}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(titulo, key=f"at_{pag}", use_container_width=True, type="primary"):
                st.session_state.pagina = pag
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec">💡 Dica do Dia</div>', unsafe_allow_html=True)
    _dicas = [
        "Os campos de experiência da BNCC não são disciplinas — eles integram diferentes saberes de forma lúdica e contextualizada.",
        "Ao planejar uma atividade, pense primeiro na vivência que a criança vai ter, depois o sistema te ajuda a associar os objetivos BNCC.",
        "A mesma atividade pode ter objetivos BNCC diferentes para bebês (EI01) e crianças maiores (EI02). O ProfaPlanner diferencia automaticamente!",
        "Argila e massinha de modelar se encaixam no campo 'Traços, Sons, Cores e Formas' — experimente digitar esse tema no Plano de Aula!",
        "Conflitos entre crianças são oportunidades pedagógicas — a BNCC tem objetivos específicos para isso no campo 'O eu, o outro e o nós'.",
    ]
    st.markdown(f"""<div class="card">
        <div style="color:#94A3B8; font-size:0.93rem; line-height:1.7;">{random.choice(_dicas)}</div>
    </div>""", unsafe_allow_html=True)

    # Link para retornar ao tour
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  Rever a apresentação do sistema", use_container_width=False):
        st.session_state.pagina = "boas_vindas"
        st.session_state.tour_step = 1
        st.rerun()


# ──────────────────────────────────────────────────────────────────────────────

def pagina_modelo():
    st.markdown('<div class="sec">📋 Meu Modelo de Plano de Aula</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94A3B8;">Aqui você coloca o formulário de plano de aula que a sua escola usa. '
                'O sistema usa ele para gerar os documentos no formato certo.</p>', unsafe_allow_html=True)

    col_upload, col_info = st.columns([1.3, 0.7])

    with col_upload:

        # ── Arquivos detectados automaticamente na pasta ──────────────────
        arquivos_locais = detectar_arquivos_locais()
        if arquivos_locais:
            st.markdown("""<div class="card card-verde" style="padding:1rem 1.2rem;">
                <div style="font-weight:700; color:#10B981; margin-bottom:0.5rem;">
                    📁 Encontrei este(s) arquivo(s) na pasta do ProfaPlanner:
                </div>
            </div>""", unsafe_allow_html=True)

            for arq in arquivos_locais:
                c_nome, c_btn = st.columns([3, 1])
                with c_nome:
                    st.markdown(f'<div style="color:#CBD5E1; padding:0.3rem 0;">📄 <strong>{arq.name}</strong></div>',
                                unsafe_allow_html=True)
                with c_btn:
                    if st.button("Usar este", key=f"usar_{arq.name}", type="primary"):
                        ext = arq.suffix.lower()
                        try:
                            if ext in [".docx", ".doc"]:
                                from docx import Document
                                doc = Document(str(arq))
                                paragrafos = [p.text for p in doc.paragraphs if p.text.strip()]
                                st.session_state.modelo_escola = {
                                    "nome": arq.name,
                                    "tipo": "Word",
                                    "paragrafos": paragrafos[:15],
                                    "caminho": str(arq),
                                }
                            else:
                                import pandas as pd
                                df = pd.read_excel(str(arq))
                                st.session_state.modelo_escola = {
                                    "nome": arq.name,
                                    "tipo": "Excel",
                                    "colunas": list(df.columns),
                                    "caminho": str(arq),
                                }
                            st.success(f"✅ **{arq.name}** carregado como modelo!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Não consegui ler o arquivo: {e}")

            st.divider()

        # ── Upload manual ─────────────────────────────────────────────────
        st.markdown("**Ou faça o upload de outro arquivo:**")
        arquivo = st.file_uploader(
            "Selecione o arquivo do modelo",
            type=["xlsx", "xls", "docx", "doc"],
            help="Formatos aceitos: Word (.docx) ou Excel (.xlsx)",
        )
        if arquivo:
            ext = Path(arquivo.name).suffix.lower()
            with st.spinner("Lendo o arquivo..."):
                try:
                    if ext in [".docx", ".doc"]:
                        from docx import Document
                        doc = Document(io.BytesIO(arquivo.read()))
                        paragrafos = [p.text for p in doc.paragraphs if p.text.strip()]
                        st.session_state.modelo_escola = {
                            "nome": arquivo.name, "tipo": "Word", "paragrafos": paragrafos[:15],
                        }
                    else:
                        import pandas as pd
                        df = pd.read_excel(arquivo)
                        st.session_state.modelo_escola = {
                            "nome": arquivo.name, "tipo": "Excel", "colunas": list(df.columns),
                        }
                    st.success(f"✅ **{arquivo.name}** carregado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Não consegui ler o arquivo. Tente novamente. ({e})")

        st.divider()

        # ── Template padrão ───────────────────────────────────────────────
        st.markdown("**Não tem o arquivo agora?**")
        st.info("💡 Sem problema! Você pode usar o modelo padrão do ProfaPlanner. "
                "Depois, quando tiver o documento da escola, pode trocar.")
        if not st.session_state.modelo_escola:
            if st.button("📄  Usar o modelo padrão do sistema", type="primary", use_container_width=True):
                st.session_state.modelo_escola = {"nome": "Modelo Padrão ProfaPlanner", "tipo": "padrao"}
                st.success("✅ Modelo padrão ativado! Você já pode criar planos de aula.")
                st.rerun()
        else:
            if st.button("🔄  Trocar o modelo", use_container_width=True):
                st.session_state.modelo_escola = None
                st.rerun()

    with col_info:
        st.markdown("""<div class="card">
            <div style="font-weight:700; color:#10B981; margin-bottom:1rem;">📌 Para que serve isso?</div>
            <div style="color:#94A3B8; font-size:0.87rem; line-height:2;">
                A sua escola provavelmente tem um formulário específico para o plano de aula.<br><br>
                Ao adicionar esse arquivo aqui, o sistema vai <strong style="color:#CBD5E1;">gerar os documentos
                no formato que a sua escola pede</strong>, já preenchido com os objetivos BNCC certos. 📋
            </div>
        </div>""", unsafe_allow_html=True)

        _m = st.session_state.modelo_escola
        if _m:
            st.markdown(f"""<div class="card card-verde">
                <div style="font-weight:700; color:#10B981;">✅ Modelo Ativo</div>
                <div style="color:#CBD5E1; margin-top:0.4rem;">📄 {_m.get('nome','—')}</div>
                <div style="color:#475569; font-size:0.78rem;">Tipo: {_m.get('tipo','—')}</div>
            </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────

def pagina_plano_aula():
    st.markdown('<div class="sec">✏️ Criar Sequência Didática</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94A3B8;">Preencha os dados para gerar sua Sequência Didática completa (com Justificativa, Atividades e Avaliação).</p>', unsafe_allow_html=True)

    col_form, col_result = st.columns([1.2, 1], gap="large")

    with col_form:
        st.markdown("**Informações Gerais:**")
        
        titulo_sd = st.text_input("📌 Título da Sequência Didática", placeholder="Ex: Descobrindo meu corpo")

        c_seg, c_faixa = st.columns(2)
        with c_seg:
            segmentos = ["Berçário 1", "Berçário 2", "Maternal 1", "Maternal 2", "Pré 1", "Pré 2"]
            segmento = st.selectbox("Segmento", segmentos)
        with c_faixa:
            _faixas = {"EI01": "👶 Bebês (0 a 1a6m)", "EI02": "🧒 Crianças (1a7m a 3a11m)", "Ambas": "Mista"}
            faixa_sel = st.selectbox("Faixa Etária (BNCC)", options=list(_faixas.keys()), format_func=lambda x: _faixas[x])

        c_dur, c_camp = st.columns(2)
        with c_dur:
            duracao = st.selectbox("⏱️ Duração", ["Bimestral", "Mensal", "Semanal", "Diário", "Outro"])
        with c_camp:
            _campos = {
                "Todos": "🔍 Todos os campos (busca geral)",
                "EO": "🤝 O eu, o outro e o nós",
                "CG": "🏃 Corpo, gestos e movimentos",
                "TS": "🎨 Traços, sons, cores e formas",
                "EF": "💬 Escuta, fala, pensamento e imaginação",
                "ET": "🔢 Espaços, tempos, quantidades e relações",
            }
            campo_sel = st.selectbox("Área / Campo Principal", options=list(_campos.keys()), format_func=lambda x: _campos[x])

        tema = st.text_input("🎯 Tema / Foco (usado para buscar na BNCC)", placeholder="Ex: Explorar movimentos e gestos...")
        
        st.markdown("**Estrutura Pedagógica:**")
        justificativa = st.text_area("📖 Justificativa", placeholder="Por que essa sequência é importante? Ex: Essa sequência favorece o desenvolvimento motor...", height=80)
        obj_geral = st.text_area("🎯 Objetivo Geral", placeholder="Ex: Promover experiências corporais que favoreçam o movimento...", height=80)
        
        st.markdown("**Atividades (Opcional):**")
        st.caption("Você pode preencher as atividades aqui ou deixar em branco para preencher depois no Word.")
        ativ1 = st.text_input("Atividade 1 (Nome)", placeholder="Ex: Chute na bola")
        desc1 = st.text_area("Descrição Ativ. 1", placeholder="Como será a atividade...", height=68, label_visibility="collapsed")
        
        ativ2 = st.text_input("Atividade 2 (Nome)", placeholder="Ex: Circuito Sensorial")
        desc2 = st.text_area("Descrição Ativ. 2", placeholder="Como será a atividade...", height=68, label_visibility="collapsed")

        avaliacao = st.text_area("📝 Avaliação", placeholder="Como será avaliado? Ex: A avaliação será através da observação diária...", height=80)

        st.markdown("<br>", unsafe_allow_html=True)
        buscar = st.button("🔍  Encontrar objetivos BNCC para esta aula", type="primary", use_container_width=True)

    with col_result:
        if buscar:
            if not tema.strip():
                st.error("⚠️ Escreva o Tema/Foco da aula para podermos buscar os objetivos na BNCC.")
                return

            faixa_filtro = None if faixa_sel == "Ambas" else faixa_sel
            campo_filtro = None if campo_sel == "Todos" else campo_sel

            with st.spinner("Buscando os objetivos certos para você..."):
                resultados = engine.buscar(texto=tema, faixa=faixa_filtro, campo=campo_filtro)

            if resultados:
                st.markdown(f"""<div class="card card-verde" style="padding:0.8rem 1.2rem; margin-bottom:1rem;">
                    <div style="color:#10B981; font-weight:600;">✅ Encontrei {len(resultados)} objetivo(s) da BNCC</div>
                    <div style="color:#94A3B8; font-size:0.82rem; margin-top:0.2rem;">Marque os que deseja incluir na sua Sequência:</div>
                </div>""", unsafe_allow_html=True)

                selecionados = []
                for obj in resultados:
                    faixa_tag = "tag-ei01" if obj["faixa"] == "EI01" else "tag-ei02"
                    faixa_label = "Bebês" if obj["faixa"] == "EI01" else "Crianças maiores"
                    col_info, col_check = st.columns([11, 1])
                    with col_info:
                        st.markdown(
                            f'<span class="badge-bncc">{obj["codigo"]}</span>&nbsp;<span class="{faixa_tag}">{faixa_label}</span>'
                            f'&nbsp;<span style="color:#64748B; font-size:0.76rem;">{obj["campo_nome"]}</span>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(f'<div style="color:#CBD5E1; font-size:0.88rem; margin:3px 0 10px 4px;">{obj["descricao"]}</div>', unsafe_allow_html=True)
                    with col_check:
                        if st.checkbox("", key=f"obj_{obj['codigo']}", value=True, label_visibility="collapsed"):
                            selecionados.append(obj)
                    st.divider()

                if selecionados:
                    atividades = []
                    if ativ1 or desc1: atividades.append({"nome": ativ1, "descricao": desc1})
                    if ativ2 or desc2: atividades.append({"nome": ativ2, "descricao": desc2})

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
                        "objetivos_bncc": selecionados,
                    }
                    
                    st.markdown("**⬇️ Exportar Documento**")
                    c_word, c_pdf = st.columns(2)
                    
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
            else:
                st.warning("Não encontrei objetivos para essas palavras. Tente descrever de outro jeito.")
        else:
            st.markdown("""<div class="card" style="text-align:center; padding:3rem 1rem;">
                <div style="font-size:3rem;">✏️</div>
                <div style="color:#334155; font-size:1.3rem; font-weight:700; margin:0.5rem 0;">Pronta para planejar?</div>
                <div style="color:#475569; font-size:0.9rem;">Preencha o formulário e clique em<br><strong style="color:#10B981;">Encontrar objetivos BNCC</strong></div>
            </div>""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────

def pagina_alunos():
    st.markdown('<div class="sec">👶 Relatório dos Alunos</div>', unsafe_allow_html=True)

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
                    nomes = [a["nome"].lower() for a in st.session_state.alunos]
                    if nome_aluno.strip().lower() in nomes:
                        st.error("Já existe um aluno com esse nome.")
                    else:
                        st.session_state.alunos.append(
                            {"nome": nome_aluno.strip(), "faixa": faixa_cod, "evolucao": {}})
                        st.success(f"✅ {nome_aluno} adicionado(a)!")
                        st.rerun()
                else:
                    st.error("Digite o nome da criança.")

        st.divider()

        if st.session_state.alunos:
            st.markdown(f"**{len(st.session_state.alunos)} criança(s) na turma:**")
            for i, aluno in enumerate(st.session_state.alunos):
                c_nome, c_prog, c_del = st.columns([3, 2, 0.4])
                with c_nome:
                    tag = "tag-ei01" if aluno["faixa"] == "EI01" else "tag-ei02"
                    label = "Bebê" if aluno["faixa"] == "EI01" else "Criança maior"
                    st.markdown(f'<span style="color:#F1F5F9; font-weight:500;">👤 {aluno["nome"]}</span>'
                                f'&nbsp;&nbsp;<span class="{tag}">{label}</span>',
                                unsafe_allow_html=True)
                with c_prog:
                    n_av = len(aluno.get("evolucao", {}))
                    n_at = sum(1 for v in aluno.get("evolucao", {}).values() if v == "A")
                    st.markdown(f'<span style="color:#475569; font-size:0.82rem;">'
                                f'{n_av} avaliados · {n_at} atingidos</span>', unsafe_allow_html=True)
                with c_del:
                    if st.button("🗑️", key=f"del_{i}"):
                        st.session_state.alunos.pop(i)
                        st.rerun()
                st.divider()
        else:
            st.info("Ainda não há crianças cadastradas. Adicione os alunos da sua turma acima.")

    with tab2:
        if not st.session_state.alunos:
            st.info("Cadastre os alunos na aba **Minha Turma** primeiro.")
            return

        aluno_nome = st.selectbox("Qual criança você quer avaliar?",
                                  [a["nome"] for a in st.session_state.alunos])
        idx = next(i for i, a in enumerate(st.session_state.alunos) if a["nome"] == aluno_nome)
        aluno = st.session_state.alunos[idx]

        _status_opts = {"A": "✅ Já consegue fazer", "D": "🔄 Está aprendendo", "N": "⏳ Ainda não iniciou"}

        st.markdown(
            f'<div style="color:#64748B; font-size:0.85rem; margin:0.5rem 0 1rem;">'
            f"Para cada habilidade abaixo, marque como <strong style='color:#F1F5F9;'>{aluno_nome}</strong> está:</div>",
            unsafe_allow_html=True)

        for campo_nome, objetivos in engine.get_objetivos_por_faixa(aluno["faixa"]).items():
            n_at = sum(1 for o in objetivos if aluno["evolucao"].get(o["codigo"]) == "A")
            with st.expander(f"📌 {campo_nome}  —  {n_at}/{len(objetivos)} conquistados"):
                for obj in objetivos:
                    c_desc, c_st = st.columns([4, 1.4])
                    with c_desc:
                        st.markdown(
                            f'<span class="badge-bncc">{obj["codigo"]}</span>'
                            f'<span style="color:#CBD5E1; font-size:0.85rem; margin-left:6px;">{obj["descricao"]}</span>',
                            unsafe_allow_html=True)
                    with c_st:
                        status = aluno["evolucao"].get(obj["codigo"], "N")
                        novo = st.selectbox("s", list(_status_opts.keys()),
                                            format_func=lambda x: _status_opts[x],
                                            index=list(_status_opts.keys()).index(status),
                                            key=f"st_{aluno_nome}_{obj['codigo']}",
                                            label_visibility="collapsed")
                        st.session_state.alunos[idx]["evolucao"][obj["codigo"]] = novo
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
                use_container_width=True)


# ──────────────────────────────────────────────────────────────────────────────

def pagina_profabot():
    st.markdown('<div class="sec">💬 Tirar Dúvidas com a Assistente Virtual</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94A3B8;">Pode perguntar à vontade sobre a BNCC, '
                'sobre planejamento ou sobre como usar o sistema. '
                'Ela responde em linguagem simples! 😊</p>', unsafe_allow_html=True)

    _sugestoes = [
        "Qual código BNCC usar com argila?",
        "Como escrever o relatório de um bebê?",
        "O que é o campo 'Traços, sons, cores e formas'?",
        "Diferença entre EI01 e EI02",
        "Atividades para trabalhar o campo EO",
        "Como usar o sistema para criar um plano?",
    ]
    st.markdown("**💡 Perguntas frequentes — clique para enviar:**")
    _cols = st.columns(2)
    for _i, _s in enumerate(_sugestoes):
        with _cols[_i % 2]:
            if st.button(f"💬 {_s}", key=f"sug_{_i}", use_container_width=True):
                st.session_state.historico_chat.append({"role": "user", "content": _s})
                with st.spinner("Pensando..."):
                    bot = ProfaBot(st.session_state.gemini_key)
                    resp = bot.responder(_s, st.session_state.historico_chat[:-1])
                st.session_state.historico_chat.append({"role": "assistant", "content": resp})
                st.rerun()

    st.divider()

    for msg in st.session_state.historico_chat:
        with st.chat_message(msg["role"], avatar="👩‍🏫" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Digite sua pergunta aqui..."):
        st.session_state.historico_chat.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👩‍🏫"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Pensando..."):
                bot = ProfaBot(st.session_state.gemini_key)
                resp = bot.responder(prompt, st.session_state.historico_chat[:-1])
            st.markdown(resp)
            st.session_state.historico_chat.append({"role": "assistant", "content": resp})

    if st.session_state.historico_chat:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️  Limpar conversa"):
            st.session_state.historico_chat = []
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  ROTEAMENTO
# ═══════════════════════════════════════════════════════════════════════════════
_PAGINAS = {
    "boas_vindas": pagina_boas_vindas,
    "inicio":      pagina_inicio,
    "modelo":      pagina_modelo,
    "plano":       pagina_plano_aula,
    "alunos":      pagina_alunos,
    "profabot":    pagina_profabot,
}
_PAGINAS[st.session_state.pagina]()
