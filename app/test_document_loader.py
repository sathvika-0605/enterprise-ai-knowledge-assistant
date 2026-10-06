from document_loader import load_pdf


pdf_path = "data/documents/raw/Handbook.pdf"


pages = load_pdf(pdf_path)


print("\n" + "=" * 70)
print("PDF LOADER TEST")
print("=" * 70)

print(
    f"Total pages extracted: {len(pages)}"
)


for page in pages:

    print("\n" + "-" * 70)

    print(
        f"Page: {page['page']}"
    )

    print(
        f"Source: {page['source']}"
    )

    print("\nTEXT:")

    print(
        page["text"][:3000]
    )

    print("\n" + "-" * 70)