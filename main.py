# main.py
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()
 
CAMINHO_DB = "db"

TEMPLATE_TRADUCAO = """
Translate the following text to English. Return only the translation, nothing else.
Text: {texto_original}
"""

PROMPT_TEMPLATE = """
# ROLE
Você é um Assistente Técnico Especialista em Python. Sua função é responder dúvidas de usuários com base estritamente na documentação fornecida.

# INSTRUÇÕES DE RESPOSTA
1. **Fonte da Verdade:** Utilize APENAS as informações contidas na seção `### CONTEXTO` abaixo.
2. Responda SEMPRE em PT-BR.
3. Traduza o contexto para português, mantendo termos de código no original.
4. NÃO mencione que o texto original está em inglês.
5. Se não houver informação suficiente, responda:
"Desculpe, a documentação fornecida não contém informações suficientes para responder a essa pergunta."

### CONTEXTO (RAG):
{base_conhecimento}

### PERGUNTA DO USUÁRIO:
{pergunta}

# RESPOSTA:
"""

def perguntar(pergunta_usuario: str) -> str:
    # 1. Traduz pergunta
    llm_tradutor = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    prompt_tradutor = ChatPromptTemplate.from_template(TEMPLATE_TRADUCAO)
    chain_traducao = prompt_tradutor | llm_tradutor | StrOutputParser()

    pergunta_ingles = chain_traducao.invoke({"texto_original": pergunta_usuario})

    # 2. Embeddings + DB
    funcao_embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    db = Chroma(persist_directory=CAMINHO_DB, embedding_function=funcao_embedding)

    resultados = db.similarity_search_with_relevance_scores(pergunta_ingles, k=4)

    if len(resultados) == 0 or resultados[0][1] < 0.5:
        return "Desculpe, a documentação fornecida não contém informações suficientes para responder."

    textos_resultado = [resultado[0].page_content for resultado in resultados]
    base_conhecimento = "\n\n----\n\n".join(textos_resultado)

    # 3. Prompt final
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.invoke({
        "pergunta": pergunta_usuario,
        "base_conhecimento": base_conhecimento
    })

    # 4. Modelo final
    modelo = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    resposta_final = modelo.invoke(prompt)

    return resposta_final.content
