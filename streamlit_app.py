# streamlit_app.py
import os
import streamlit as st
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

st.set_page_config(page_title="Employee Handbook AI Assistant",
                   page_icon="📘", layout="wide")

st.title("Enterprise Semantic Search (Q&A Engine) 👩🏻‍💻")
st.markdown("""
Ask questions about:
- Leave Policy
- Working Hours
- Attendance Rules
""")

with st.sidebar:
    st.header("📘 Project Information")
    st.success("Enterprise RAG System (Gemini + Fallback)")
    st.markdown("""
### Tech Stack
- Streamlit
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Gemini 2.5 Flash
""")

@st.cache_resource
def load_system():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db = Chroma(
        persist_directory=os.path.join(base_dir, "vector_db"),
        embedding_function=embeddings,
    )

    api_key = st.secrets.get("GEMINI_API_KEY")

    llm = None
    if api_key:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0,
        )

    return db, llm

db, llm = load_system()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

query = st.chat_input("Ask a question about the handbook...")

if query:

    st.session_state.messages.append({"role":"user","content":query})

    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching handbook..."):

            q = query.lower()

            if "leave" in q:
                q += " vacation paid leave sick leave casual leave policy"
            elif "working" in q:
                q += " working hours office timing schedule"
            elif "attendance" in q:
                q += " attendance punctuality rules"

            results = db.similarity_search_with_score(q, k=5)

            unique_docs = []
            seen = set()

            for doc, score in results:
                text = doc.page_content.strip()
                if text not in seen:
                    seen.add(text)
                    unique_docs.append(doc)

            context = "\n\n".join(doc.page_content for doc in unique_docs)

            prompt = f"""
You are an Employee Handbook Assistant.

Use ONLY the handbook context below.

If the answer exists, summarize it in clear bullet points.
Do not invent information.

Context:
{context}

Question:
{query}

Answer:
"""

            if llm:
                try:
                    response = llm.invoke(prompt)
                    answer = response.content
                except Exception as e:
                    st.warning(f"Gemini unavailable. Using handbook fallback.\n\n{e}")
                    if unique_docs:
                        answer = "📘 **Answer from handbook:**\n\n"
                        for d in unique_docs[:2]:
                            answer += d.page_content[:500] + "\n\n"
                    else:
                        answer = "No relevant information found."
            else:
                if unique_docs:
                    answer = "📘 **Answer from handbook:**\n\n"
                    for d in unique_docs[:2]:
                        answer += d.page_content[:500] + "\n\n"
                else:
                    answer = "No relevant information found."

        st.write(answer)

        with st.expander("📄 Sources Used"):
            for i, doc in enumerate(unique_docs,1):
                st.markdown(f"**Source {i}**")
                st.write(doc.page_content[:500])
                st.markdown("---")

    st.session_state.messages.append({"role":"assistant","content":answer})
