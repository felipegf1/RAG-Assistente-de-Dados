import streamlit as st
from main import perguntar  

st.set_page_config(page_title="RAG Assistente de Dados", page_icon="⚡")

st.title("RAG Assistente de Dados")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if prompt := st.chat_input("Faça sua pergunta..."):
    # 1. Mostrar pergunta no histórico
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Gerar resposta
    with st.chat_message("assistant"):
        with st.spinner("Consultando..."):
            try:
                resposta = perguntar(prompt) 
                st.markdown(resposta)
                st.session_state.messages.append(
                    {"role": "assistant", "content": resposta}
                )
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
