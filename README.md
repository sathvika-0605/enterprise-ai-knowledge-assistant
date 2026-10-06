# 🏢 Enterprise AI Knowledge Assistant

A production-oriented **Retrieval-Augmented Generation (RAG)** based Enterprise AI Knowledge Assistant that allows users to ask natural-language questions about enterprise documents and receive answers grounded only in the retrieved document content.

The system combines:

- Recursive document chunking
- Metadata-based document organization
- Semantic vector search using ChromaDB
- BM25 keyword search
- Hybrid retrieval with Reciprocal Rank Fusion (RRF)
- Cross-Encoder re-ranking
- Local Llama 3.2 3B through Ollama
- Grounding / hallucination checking
- Source and page citations
- FastAPI backend
- Streamlit frontend
- PDF table extraction
- Evaluation using a 15-question golden dataset

---

## 📌 Project Overview

Enterprise organizations maintain large numbers of documents such as:

- Leave policies
- Work-from-home policies
- Employee handbooks
- HR policies
- Standard Operating Procedures (SOPs)
- Company guidelines
- Compliance documents

Finding specific information manually from large documents can be time-consuming.

The Enterprise AI Knowledge Assistant provides a conversational interface where users can ask questions in natural language and retrieve relevant information from enterprise documents.

The system retrieves relevant document content first and then provides the retrieved context to a local Large Language Model (LLM) to generate a grounded answer.

---

## 🎯 Problem Statement

Employees may need to search through multiple enterprise documents to find specific information.

For example:

> "How many Privilege Leave days are employees entitled to?"

Instead of manually searching through PDFs, users can ask the question directly to the Enterprise AI Knowledge Assistant.

The system identifies relevant document content, ranks the most useful information, generates an answer, and provides the supporting document source and page.

---

# 💡 Solution

The application follows an enhanced **RAG architecture**.

The overall process is:

1. Load enterprise PDF documents.
2. Extract text and tables from the PDFs.
3. Detect document sections and metadata.
4. Split documents using recursive chunking.
5. Generate embeddings for the chunks.
6. Store embeddings and metadata in ChromaDB.
7. Build a BM25 keyword index.
8. Convert the user's question into a retrieval query.
9. Perform semantic vector search.
10. Perform BM25 keyword search.
11. Combine the retrieval results using Reciprocal Rank Fusion (RRF).
12. Re-rank the retrieved chunks using a Cross-Encoder.
13. Build the context from the highest-ranked chunks.
14. Send the context and question to Llama 3.2 3B.
15. Generate an answer using only the retrieved context.
16. Check whether the answer is grounded in the retrieved evidence.
17. Return the answer and supporting source information.
18. Display the result through the Streamlit UI.

---

# 🏗️ System Architecture

```text
                         Enterprise PDFs
                                │
                                ▼
                    ┌──────────────────────┐
                    │   PDF Document       │
                    │      Loader          │
                    └──────────────────────┘
                                │
                     ┌──────────┴──────────┐
                     │                     │
                     ▼                     ▼
              Text Extraction       Table Extraction
              (PyMuPDF)             (pdfplumber)
                     │                     │
                     └──────────┬──────────┘
                                │
                                ▼
                    Document / Section Metadata
                                │
                                ▼
                    Recursive Text Chunking
                                │
                                ▼
                     Chunked Documents
                                │
                                ▼
                  Sentence Transformer
                   all-MiniLM-L6-v2
                                │
                                ▼
                         ChromaDB
                     Vector Database
                                │
                                │
                     ┌──────────┴──────────┐
                     │                     │
                     │    User Question    │
                     │                     │
                     └──────────┬──────────┘
                                │
                                ▼
                         Streamlit UI
                                │
                                ▼
                           FastAPI
                                │
                                ▼
                    ┌──────────────────────┐
                    │   Hybrid Retrieval  │
                    └──────────────────────┘
                         │            │
                         ▼            ▼
                  Vector Search     BM25
                  ChromaDB         Keyword
                         │            │
                         └─────┬──────┘
                               │
                               ▼
                    Reciprocal Rank Fusion
                             (RRF)
                               │
                               ▼
                      Candidate Documents
                               │
                               ▼
                    Cross-Encoder Re-ranker
                               │
                               ▼
                     Top Relevant Chunks
                               │
                               ▼
                       Context Builder
                               │
                               ▼
                      Llama 3.2 3B
                         via Ollama
                               │
                               ▼
                        Generated Answer
                               │
                               ▼
                     Grounding Checker
                               │
                     ┌─────────┴─────────┐
                     │                   │
                  Supported          Not Supported
                     │                   │
                     ▼                   ▼
              Final Answer          Safe Fallback
                     │
                     ▼
              Source + Page
                 Citations
                     │
                     ▼
                Streamlit UI