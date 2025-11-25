# 🤖 Gemini RAG – Assistente de Dados

Este projeto é um **assistente virtual baseado em RAG (Retrieval-Augmented Generation)** voltado para apoiar **estudos, análises e dúvidas técnicas na área de dados**.

Ele permite que você **converse em Português** com os conteúdos presentes em documentos PDF técnicos.  
O sistema traduz internamente a pergunta para inglês (onde a maioria da documentação técnica está escrita), realiza a busca vetorial e depois responde em PT-BR de forma natural e contextualizada.

---

<img width="1076" height="857" alt="Interface do Projeto" src="https://github.com/user-attachments/assets/fa180e41-3c72-455d-8ef5-5e18942e0543" />

---

## ✨ Funcionalidades

- Conversa em **PT-BR**, mas pesquisa em **inglês** para melhorar a precisão.
- Usa **Gemini 2.5 Flash** para traduzir consultas e gerar respostas inteligentes.
- Indexa PDFs técnicos via **ChromaDB + Embeddings**.
- Interface simples e rápida com **Streamlit**.
- Integração direta com documentos reais, ideal para estudo e consulta.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **LangChain**
- **Google Gemini 2.5 Flash**
- **Embeddings:** `models/text-embedding-004`
- **ChromaDB**
- **PyPDF**
- **Streamlit**

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para rodar o assistente **RAG** localmente.

---

### **1. Clone o repositório**

Clone o repositório e navegue até o diretório do projeto:

```bash
git clone [https://github.com/felipegf1/RAG-Assistente-de-Dados.git](https://github.com/felipegf1/RAG-Assistente-de-Dados.git)
cd RAG-Assistente-de-Dados
```

---

### **2. Crie o ambiente virtual**

Crie e ative um ambiente virtual para isolar as dependências do projeto:

```bash
python -m venv venv
```

**Ativação:**

```bash
# Linux / Mac
source venv/bin/activate      

# Windows
venv\Scripts\activate
```

---

### **3. Instale as dependências**

Instale todas as bibliotecas necessárias usando o `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### **4. Configure as variáveis de ambiente**

Primeiro, renomeie o arquivo de exemplo para `.env`:

```bash
# Linux/Mac
cp .env.example .env

# Windows
copy .env.example .env
```

Em seguida, abra o arquivo **`.env`** e insira sua **Google API Key**:

> **`.env`**
>
> ```
> GOOGLE_API_KEY="sua-api-key-aqui"
> ```

---

### **5. Gere o banco vetorial (ChromaDB)**

Execute o script para processar os dados e gerar o banco de dados vetorial:

```bash
python criar_db.py
```

Isso criará a pasta **`db/`** no diretório raiz do projeto.

---

### **6. Rodar o Assistente RAG (Streamlit)**

Execute o aplicativo Streamlit para iniciar o assistente:

```bash
streamlit run app.py
```

O assistente estará acessível no seu navegador.
