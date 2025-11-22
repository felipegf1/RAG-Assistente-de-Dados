# 🤖 Gemini RAG Assistant

Este projeto é um assistente virtual baseado em RAG (Retrieval-Augmented Generation) que permite conversar com documentos PDF técnicos. 

O diferencial deste sistema é o uso de **Query Translation**: o usuário pode perguntar em Português, o sistema traduz internamente para Inglês para buscar nos documentos técnicos (geralmente em inglês), e a resposta final é gerada de volta em Português.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-v0.3-green)
![Gemini](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-orange)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)

## 🏗️ Arquitetura do Projeto

O sistema foi desenvolvido seguindo o padrão de arquitetura limpa, separando a interface da lógica de negócio. O fluxo de dados funciona da seguinte maneira:

1.  **Input do Usuário:** Pergunta em PT-BR.
2.  **Agente Tradutor:** Um LLM especializado traduz a query para Inglês (melhorando a semântica para busca vetorial).
3.  **Vector Search (ChromaDB):** Busca os trechos (chunks) mais relevantes nos PDFs indexados.
4.  **Agente de Resposta:** O LLM (Gemini 1.5 Flash) recebe o contexto em inglês e gera a explicação final em PT-BR.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Orquestração:** LangChain
* **LLM & Embeddings:** Google Gemini (`gemini-2.5-flash` e `text-embedding-004`)
* **Banco Vetorial:** ChromaDB
* **Interface:** Streamlit
* **Processamento de Arquivos:** PyPDF

## 📂 Estrutura de Pastas

```bash
.
├── dados/                # Pasta onde ficam os PDFs para ingestão
├── db/                   # Banco de dados vetorial (persistido localmente)
├── src/                  # Código fonte da inteligência (Backend)
│   ├── ingestao.py       # Script para ler PDFs e criar o banco
│   └── rag_engine.py     # Classe que gerencia a lógica de RAG e tradução
├── app.py                # Interface do usuário (Streamlit)
├── requirements.txt      # Dependências do projeto
└── .env                  # Variáveis de ambiente (API KEYS)