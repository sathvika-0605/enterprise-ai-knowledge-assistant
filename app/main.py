from pathlib import Path

from document_loader import load_pdf
from chunker import chunk_documents
from vector_store import add_documents


# Location of enterprise documents
data_folder = Path("data/documents/raw")


# Find all PDFs
pdf_files = list(data_folder.glob("*.pdf"))

print(f"Found {len(pdf_files)} PDF files.")


# Load all pages
all_documents = []

for pdf_file in pdf_files:

    print(f"\nLoading: {pdf_file.name}")

    pages = load_pdf(str(pdf_file))

    print(f"Pages loaded: {len(pages)}")

    all_documents.extend(pages)


print(f"\nTotal pages loaded: {len(all_documents)}")


# Create chunks
chunks = chunk_documents(all_documents)

print(f"Total chunks created: {len(chunks)}")


# Store chunks in ChromaDB
print("\nCreating embeddings and storing documents...")

number_added = add_documents(chunks)

print(f"Successfully stored {number_added} chunks in ChromaDB.")

print("\nDocument ingestion completed successfully!")