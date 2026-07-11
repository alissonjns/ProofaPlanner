import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

novo_css = '''st.markdown("""
<style>
/* Remove margin around main container to look cleaner */
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 900px; }

/* Esconde menu do Streamlit Cloud */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Correção para o Bug do Google Tradutor (_arrowRight_) */
</style>
<meta name="google" content="notranslate">
""", unsafe_allow_html=True)'''

pattern = re.compile(r'st\.markdown\("""\s*<style>.*?<meta name="google" content="notranslate">\s*""", unsafe_allow_html=True\)', re.DOTALL)
new_content = re.sub(pattern, novo_css, content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print("CSS para esconder menu adicionado!")
