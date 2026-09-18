from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = []

    for document in documents:
        split_texts = splitter.split_text(document["text"])

        for chunk in split_texts:
            chunks.append(
                {
                    "text": chunk,
                    "source": document["source"],
                    "page": document["page"],
                }
            )

    return chunks