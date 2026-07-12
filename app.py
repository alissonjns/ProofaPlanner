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
                resultados = engine.buscar(texto=tema, faixa=faixa_filtro, campo=campo_filtro)[:4] # Limita aos 4 melhores resultados

            if resultados:
                st.markdown("**2. Escolha os Códigos BNCC (Mostrando os 4 melhores):**")
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
            with st.expander(f"🧩 Atividade {i+1}: {ativ.get('nome', '')}", expanded=False):
                nome_a = st.text_input("Nome da Atividade", value=ativ.get("nome", ""), key=f"n_{i}")
                desc_a = st.text_area("Passo a Passo", value=ativ.get("descricao", ""), height=150, key=f"d_{i}")
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


# ──────────────────────────────────────────────────────────────────────────────

def pagina_alunos():
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
