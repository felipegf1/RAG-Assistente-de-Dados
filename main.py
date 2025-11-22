# pip install python-dotenv langchain langchain-openai langchain-community langchain-chroma chromadb openai pypdf
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser # <--- NOVA IMPORTAÇÃO
from dotenv import load_dotenv
import os
#rodar pip freeze > requirements.txt
load_dotenv()

CAMINHO_DB = "db"

# --- NOVO TEMPLATE PARA O AGENTE TRADUTOR ---
TEMPLATE_TRADUCAO = """
Translate the following text to English. Return only the translation, nothing else.
Text: {texto_original}
"""

PROMPT_TEMPLATE = """
# ROLE
Você é um Assistente Técnico Especialista em Python. Sua função é responder dúvidas de usuários com base estritamente na documentação fornecida.

# INSTRUÇÕES DE RESPOSTA
1. **Fonte da Verdade:** Utilize APENAS as informações contidas na seção `### CONTEXTO` abaixo. Ignore seu conhecimento prévio sobre Python se a informação não estiver presente no texto fornecido.
2. **Idioma:** Responda SEMPRE em Português do Brasil (PT-BR).
3. **Tradução:** O contexto está em inglês. Você deve traduzir a explicação para português, mas MANTENHA termos técnicos de código (ex: nomes de funções, classes, bibliotecas, erros) no original em inglês ou conforme padrão da comunidade técnica.
4. **Meta-comentários:** NÃO mencione que o texto original estava em inglês. Aja como se a fonte fosse nativa.
5. **Fallback:** Se a resposta não puder ser encontrada ou deduzida unicamente do contexto fornecido, responda apenas: "Desculpe, a documentação fornecida não contém informações suficientes para responder a essa pergunta."

# DADOS DE ENTRADA

### CONTEXTO (RAG):
{base_conhecimento}

### PERGUNTA DO USUÁRIO:
{pergunta}

# RESPOSTA:
"""

def perguntar():
    pergunta = input("Escreva sua pergunta: ")

    # ======================================================
    # ETAPA NOVA: AGENTE DE TRADUÇÃO (PT -> EN)
    # ======================================================
    print("Traduzindo para melhorar a busca...")
    llm_tradutor = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    prompt_tradutor = ChatPromptTemplate.from_template(TEMPLATE_TRADUCAO)
    
    # Chain: Prompt -> LLM -> String Limpa
    chain_traducao = prompt_tradutor | llm_tradutor | StrOutputParser()
    
    pergunta_ingles = chain_traducao.invoke({"texto_original": pergunta})
    print(f"Termo traduzido: {pergunta_ingles}")
    # ======================================================

    # 1. Carregar o modelo de Embedding 
    funcao_embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    # 2. Carregar o banco
    db = Chroma(persist_directory=CAMINHO_DB, embedding_function=funcao_embedding)

    # 3. Busca por similaridade (USANDO A PERGUNTA EM INGLÊS AGORA)
    resultados = db.similarity_search_with_relevance_scores(pergunta_ingles, k=4)
    
    if len(resultados) == 0 or resultados[0][1] < 0.5:
        print(f"Não encontrei informações relevantes.")
        return
    
    # Extrair o texto dos chunks encontrados
    textos_resultado = [resultado[0].page_content for resultado in resultados]
    base_conhecimento = "\n\n----\n\n".join(textos_resultado)

    # 4. Preparar o Prompt (MANTÉM A PERGUNTA ORIGINAL EM PT PARA A RESPOSTA)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.invoke({"pergunta": pergunta, "base_conhecimento": base_conhecimento})

    # 5. Chamar o LLM (Gemini) para gerar a resposta final
    modelo = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    response = modelo.invoke(prompt)
    print("\n--- Resposta da IA ---\n")
    print(response.content)

if __name__ == "__main__":
    perguntar()