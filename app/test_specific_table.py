from document_loader import load_pdf


pdf_path = "data/documents/raw/Handbook.pdf"

pages = load_pdf(pdf_path)

print("\n" + "=" * 70)
print("SPECIFIC TABLE EXTRACTION TEST")
print("=" * 70)

for page in pages:

    if page["page"] == 6:

        print(f"\nPAGE: {page['page']}")
        print(f"SOURCE: {page['source']}")

        print("\n" + "-" * 70)
        print(page["text"])
        print("-" * 70)