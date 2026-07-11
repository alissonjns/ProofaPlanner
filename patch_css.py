import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir TODO o bloco de st.markdown inicial
pattern = re.compile(r'st\.markdown\("""\s*<style>.*?<meta name="google" content="notranslate">\s*""", unsafe_allow_html=True\)', re.DOTALL)

novo_css = '''st.markdown("""
<style>
/* Remove margin around main container to look cleaner */
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 900px; }
/* Correção para o Bug do Google Tradutor (_arrowRight_) */
</style>
<meta name="google" content="notranslate">
""", unsafe_allow_html=True)'''

new_content = re.sub(pattern, novo_css, content)
# limpar vestígios do # Estilos Globais mal inserido
new_content = new_content.replace("# ─── Estilos Globais ────────────────────────────────────────────────────────────\n# ─── Estilos Globais", "# ─── Estilos Globais")
new_content = new_content.replace("# ─── Estilos Globais ────────────────────────────────────────────────────────────\n\nst.markdown", "st.markdown")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("CSS totalmente limpo e corrigido!")
