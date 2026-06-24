from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

print("🔄 Loading system...")

# ---------------- LOAD EMBEDDINGS ----------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ---------------- LOAD VECTOR DB ----------------
db = Chroma(
    persist_directory="vector_db",
    embedding_function=embeddings
)

# ---------------- LOAD LLM ----------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

print("✅ System loaded successfully!")

# ---------------- CHAT LOOP ----------------
while True:
    query = input("\nAsk question (type 'exit'): ")

    if query.lower() == "exit":
        break

    print("\n🔍 Searching documents...")
    docs = db.similarity_search(query, k=3)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
Answer only using the context below.

Context:
{context}

Question:
{query}

Answer:
"""

    print("\n🤖 Generating answer...")

    try:
        response = llm.invoke(prompt)
        print("\n🧠 Answer:\n", response.content)

    except Exception as e:
        print("\n⚠️ Gemini failed, using fallback")
        print("\n🧠 Answer:\n", context)

    print("\n📄 Sources:")
    for i, doc in enumerate(docs, 1):
        print(f"\nSource {i}:")
        print(doc.page_content[:300])