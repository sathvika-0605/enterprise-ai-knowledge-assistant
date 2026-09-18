\# 🏢 Enterprise AI Knowledge Assistant



A RAG-based Enterprise AI Knowledge Assistant that allows users to ask questions about company policy documents and receive answers based only on the relevant information retrieved from those documents.



The system uses \*\*Retrieval-Augmented Generation (RAG)\*\* with \*\*ChromaDB\*\* for semantic document retrieval and \*\*Llama 3.2 3B\*\* running locally through \*\*Ollama\*\* for answer generation.



\---



\## 📌 Project Overview



Enterprise organizations maintain large numbers of documents such as:



\- Leave policies

\- Work-from-home policies

\- HR policies

\- Standard Operating Procedures (SOPs)

\- Company guidelines



Finding specific information manually from these documents can be time-consuming.



This project provides a question-answering system where users can ask questions in natural language and retrieve relevant information from enterprise documents.



The system retrieves relevant document chunks first and then provides them as context to the LLM for generating a grounded answer.



\---



\## 🎯 Problem Statement



Employees may need to search through multiple company documents to find answers to policy-related questions.



For example:



> "How many Privilege Leave days are employees entitled to?"



Instead of manually searching through PDFs, the user can ask the question directly to the Enterprise AI Knowledge Assistant.



\---



\## 💡 Solution



The application follows a \*\*Retrieval-Augmented Generation (RAG)\*\* architecture.



The system:



1\. Loads enterprise PDF documents.

2\. Extracts text from the PDFs.

3\. Splits the text into smaller chunks.

4\. Converts the chunks into embeddings.

5\. Stores the embeddings in ChromaDB.

6\. Converts the user's question into an embedding.

7\. Retrieves the most relevant document chunks.

8\. Sends the retrieved context to Llama 3.2 3B.

9\. Generates an answer based on the retrieved information.

10\. Displays the answer and document sources to the user.



\---



\## 🏗️ Architecture



```text

&#x20;                   Enterprise PDFs

&#x20;                         │

&#x20;                         ▼

&#x20;                    PyPDF

&#x20;                         │

&#x20;                         ▼

&#x20;                  Text Extraction

&#x20;                         │

&#x20;                         ▼

&#x20;             Recursive Text Splitter

&#x20;                   (LangChain)

&#x20;                         │

&#x20;                         ▼

&#x20;                      Chunks

&#x20;                         │

&#x20;                         ▼

&#x20;            Sentence Transformers

&#x20;                 all-MiniLM-L6-v2

&#x20;                         │

&#x20;                         ▼

&#x20;                    Embeddings

&#x20;                         │

&#x20;                         ▼

&#x20;                    ChromaDB

&#x20;                         │

&#x20;                         │

&#x20;                   User Question

&#x20;                         │

&#x20;                         ▼

&#x20;                   Streamlit UI

&#x20;                         │

&#x20;                         ▼

&#x20;                    FastAPI

&#x20;                         │

&#x20;                         ▼

&#x20;                Question Embedding

&#x20;                         │

&#x20;                         ▼

&#x20;                 ChromaDB Search

&#x20;                         │

&#x20;                         ▼

&#x20;                Top Relevant Chunks

&#x20;                         │

&#x20;                         ▼

&#x20;                 Context Building

&#x20;                         │

&#x20;                         ▼

&#x20;               Ollama / Llama 3.2 3B

&#x20;                         │

&#x20;                         ▼

&#x20;                   Final Answer

&#x20;                         │

&#x20;                         ▼

&#x20;                FastAPI JSON Response

&#x20;                         │

&#x20;                         ▼

&#x20;                   Streamlit UI

