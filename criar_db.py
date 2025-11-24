from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os 

load_dotenv()

PASTA_BASE = "base_dados"
PASTA_DB = "db"

def criar_db():

    if not os.path.exists(PASTA_BASE):
        os.makedirs(PASTA_BASE)
        print(f"A pasta '{PASTA_BASE}' não existia e foi criada. Coloque seus PDFs nela e execute o script novamente.")
        return

    documentos = carregar_documentos()

    if not documentos:
        print("Nenhum documento encontrado. O banco não foi criado.")
        return

    chunks = dividir_chunks(documentos)
    vetorizar_chunks(chunks)

def carregar_documentos():
    print("Carregando documentos...")
    carregador = PyPDFDirectoryLoader(PASTA_BASE, glob="*.pdf")
    documentos = carregador.load()
    return documentos

def dividir_chunks(documentos):
    separador_documentos = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        length_function=len,
    )
    chunks = separador_documentos.split_documents(documentos)
    return chunks

def vetorizar_chunks(chunks):
    print("Gerando embeddings e salvando no ChromaDB...")

    embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    os.makedirs(PASTA_DB, exist_ok=True)

    db = Chroma.from_documents(
        documents=chunks, 
        embedding=embedding_model, 
        persist_directory=PASTA_DB
    )
    
    print(f"Banco de Dados criado com sucesso na pasta '{PASTA_DB}'")

if __name__ == "__main__": 
    criar_db()
