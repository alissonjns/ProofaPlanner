# 📚 ProfaPlanner - Assistente Pedagógico BNCC

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Gemini_AI-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge)

O **ProfaPlanner** é uma aplicação web construída em Python desenvolvida para automatizar e facilitar o planejamento pedagógico de professores da Educação Infantil. O sistema resolve o problema real do cruzamento de atividades práticas com os códigos alfanuméricos exigidos pela **BNCC (Base Nacional Comum Curricular)**.

## 🚀 Funcionalidades Principais

- **Motor de Busca BNCC**: Filtra e encontra objetivos de aprendizagem específicos por faixa etária (Bebês e Crianças Bem Pequenas) e campos de experiência.
- **Geração Automatizada de Documentos**: Exporta Sequências Didáticas completas diretamente para **Word (.docx)** e **PDF** com formatação profissional.
- **Chatbot Integrado (ProfaBot)**: Uma assistente virtual alimentada pela API do **Google Gemini (IA Generativa)** para tirar dúvidas sobre a BNCC e sugerir atividades.
- **Relatórios de Alunos**: Sistema de tracking para acompanhamento do desenvolvimento de cada criança.
- **Interface Premium (UI/UX)**: Desenvolvida com Streamlit e customizada com CSS avançado (Glassmorphism e componentes modernos).

## 🛠️ Stack Tecnológico

- **Backend**: Python 3.12
- **Frontend / UI**: Streamlit + Custom CSS
- **IA Generativa**: `google-generativeai` (Gemini 1.5 Flash)
- **Manipulação de Dados**: `pandas`
- **Geração de Documentos**: `python-docx` (Word) e `reportlab` (PDF)
- **Segurança**: `python-dotenv` para injeção de variáveis de ambiente.

## ⚙️ Como executar o projeto localmente

1. Clone o repositório:
```bash
git clone https://github.com/SEU_USUARIO/ProfaPlanner.git
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as chaves de API:
Crie um arquivo `.env` na raiz do projeto e adicione sua chave do Google AI Studio:
```env
GEMINI_API_KEY=sua_chave_aqui
```

5. Rode a aplicação:
```bash
streamlit run app.py
```

## 📜 Licença

Este projeto é licenciado sob a **GNU General Public License v3.0 (GPLv3)**. Sinta-se livre para usar, estudar e modificar o código. Caso decida distribuir ou comercializar uma versão modificada, o código-fonte deve permanecer aberto sob a mesma licença.
