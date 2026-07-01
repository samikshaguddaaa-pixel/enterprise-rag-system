# Enterprise Semantic Search & Q&A Engine🏢

An AI-powered Enterprise Question Answering system that uses Retrieval-Augmented Generation (RAG) to provide accurate, context-aware answers from pre-indexed enterprise documents.

The application combines semantic search with Large Language Models (LLMs) to retrieve relevant information and generate natural language responses.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Project Overview 📖

Traditional keyword-based document search often fails to understand the actual meaning of a user's question. This project solves that problem using Retrieval-Augmented Generation (RAG), enabling users to ask questions in natural language and receive intelligent answers based on enterprise documents.

The system uses pre-indexed PDF documents stored in a Chroma vector database. When a user submits a query, the application retrieves the most relevant document chunks and provides them to Gemini 2.5 Flash to generate an accurate response.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Features 📌

- AI-powered semantic document search
- Retrieval-Augmented Generation (RAG)
- Natural language question answering
- Pre-indexed knowledge base using ChromaDB
- Fast similarity search using embeddings
- Streamlit-based interactive user interface
- Gemini 2.5 Flash integration
- Fallback response when the Gemini API is unavailable

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Tech Stack 🛠️

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| Streamlit | Web Application |
| LangChain | RAG Pipeline |
| ChromaDB | Vector Database |
| Hugging Face Embeddings | Text Embeddings |
| Gemini 2.5 Flash | Large Language Model |


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## System Workflow 🔄

### 1. Knowledge Base Preparation 📚

1. Load enterprise PDF documents.
2. Extract text from PDFs.
3. Split text into smaller chunks.
4. Generate embeddings using Hugging Face.
5. Store embeddings in ChromaDB.



### 2. Query Processing 🔍

1. User enters a question.
2. The query is converted into an embedding.
3. ChromaDB performs semantic similarity search.
4. The most relevant document chunks are retrieved.
5. Retrieved context and user query are sent to Gemini 2.5 Flash.
6. Gemini generates a context-aware answer.
7. The final response is displayed in the Streamlit interface.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Sample Questions 💬

- What is the leave policy?
- How many casual leaves are provided?
- What are the workplace safety guidelines?
- How is the attendance system?
- What are the employee responsibilities?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Future Enhancements 🚀

- Support multiple document uploads
- Role-based access control
- Chat history
- Source citation for answers
- Multi-language support
- Cloud database integration

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Author 👩‍💻

**Samiksha Gudda**

B.Tech – Computer Science & Engineering (AI & ML)

Joy University

## Project Under
## TANSAM (Tamil Nadu Smart and Advanced Manufacturing Centre) 

Project Title: Enterprise Semantic Search & Q&A Engine

**Developed during my AI/ML Internship at TANSAM**

An AI-powered Enterprise Question Answering system that uses Retrieval-Augmented Generation (RAG) to provide accurate, context-aware answers from pre-indexed enterprise documents.

