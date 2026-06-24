import os
import streamlit as st
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# -----------------------------
# LOAD ENVIRONMENT VARIABLES
# -----------------------------
load_dotenv()

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Employee Handbook AI Assistant",
    page_icon="📘",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------
st.title(" Enterprise Semantic Search(Q&A Engine) 👩🏻‍💻")

st.markdown("""
Ask questions about:

- Leave Policy
- Working Hours
- Attendance Rules


Feel free to know more about the company.
""")

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.header("📘 Project Information")

    st.success("Enterprise RAG System")

    st.markdown("""
### Tech Stack ⚙️

- Streamlit
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Gemini 2.5 Flash

### Features 🔎

- Semantic Search
- Context-Aware Answers
- Employee Handbook Q&A
- Source Retrieval
""")

# -----------------------------
# LOAD SYSTEM
# -----------------------------
@st.cache_resource
def load_system():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory="vector_db",
        embedding_function=embeddings
    )

    api_key = os.getenv("GOOGLE_API_KEY")

    llm = None

    if api_key:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=api_key
        )

    return db, llm


db, llm = load_system()

# -----------------------------
# CHAT HISTORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# -----------------------------
# CHAT INPUT
# -----------------------------
query = st.chat_input(
    "Ask a question about the employee handbook..."
)

# -----------------------------
# QUESTION ANSWERING
# -----------------------------
if query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):

        with st.spinner("🔍 Searching handbook..."):

            docs = db.similarity_search(query, k=3)

            unique_docs = []
            seen = set()

            for doc in docs:

                text = doc.page_content.strip()

                if text not in seen:
                    seen.add(text)
                    unique_docs.append(doc)

            context = "\n\n".join(
                [doc.page_content for doc in unique_docs]
            )

            prompt = f"""
You are an Employee Handbook Assistant.

Answer ONLY using the handbook context below.

Rules:
- Be professional.
- Be concise.
- Use bullet points when appropriate.
- Do not repeat information.
- If the answer is not available, say so.

Context:
{context}

Question:
{query}

Answer:
"""

            try:

                if llm:
                    response = llm.invoke(prompt)
                    answer = response.content
                else:
                    answer = context

            except Exception:
                answer = context

        st.write(answer)

        with st.expander("📄 Sources Used"):

            for i, doc in enumerate(unique_docs, start=1):

                st.markdown(f"**Source {i}**")
                st.write(doc.page_content[:500])
                st.markdown("---")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )