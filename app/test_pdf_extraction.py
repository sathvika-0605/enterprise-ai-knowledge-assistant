from document_loader import load_pdf

pdf_path = "data/documents/raw/Handbook.pdf"

pages = load_pdf(pdf_path)

print("Total pages:", len(pages))

for page in pages:
    if "[TABLE" in page["text"]:
        print("\n====================================")
        print("SOURCE:", page["source"])
        print("PAGE:", page["page"])
        print("====================================")
        print(page["text"])