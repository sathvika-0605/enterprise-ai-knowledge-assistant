from langchain_text_splitters import RecursiveCharacterTextSplitter


# Recursive text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


def is_section_heading(line):
    """
    Check whether a line looks like a section heading.
    """

    line = line.strip()

    if not line:
        return False

    # Ignore page numbers
    if line.isdigit():
        return False

    # Ignore very long lines
    if len(line) > 100:
        return False

    # Main chapter headings
    if line.startswith("Chapter "):
        return True

    # Annexure headings
    if line.startswith("Annexure "):
        return True

    # Section headings
    if line.startswith("Section "):
        return True

    # Part headings
    if line.startswith("Part "):
        return True

    # Numbered headings such as:
    # 3.1 Compliances
    # 3.2 Working Hours
    # 3.3 Register and Records
    if (
        len(line) >= 3
        and line[0].isdigit()
        and "." in line[:4]
    ):
        return True

    return False


def detect_section(text):
    """
    Detect a section heading from the beginning
    of a page.
    """

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    if not lines:
        return ""

    for index, line in enumerate(lines[:12]):

        # Ignore page numbers
        if line.isdigit():
            continue

        if is_section_heading(line):

            section = line

            # Handle headings that continue on the next line.
            # Example:
            # Chapter 2: Reforms Introduced
            # under Labour Codes
            if index + 1 < len(lines):
                next_line = lines[index + 1].strip()

                if (
                    next_line
                    and not is_section_heading(next_line)
                    and not next_line.isdigit()
                    and len(next_line) <= 100
                ):
                    # Only join if it looks like a continuation
                    # of the heading.
                    if (
                        line.startswith("Chapter ")
                        or line.startswith("Annexure ")
                        or line.startswith("Part ")
                    ):
                        section = f"{section} {next_line}"

            return section

    return ""


def get_document_type(source):
    """
    Identify the document type from the file name.
    """

    source_lower = source.lower()

    if "leave" in source_lower:
        return "leave_policy"

    if "wfh" in source_lower:
        return "wfh_policy"

    if "handbook" in source_lower:
        return "employee_handbook"

    return "general_document"


def is_contents_page(document):
    """
    Identify the Contents page so that chapter names
    listed there are not treated as the current section.
    """

    text = document["text"].lower()

    return "contents" in text[:500]


def chunk_documents(documents):
    """
    Split documents into chunks while preserving
    section information across pages.
    """

    chunks = []

    chunk_counter = 0

    # Keep track of the latest actual section.
    current_section = ""

    for document in documents:

        # -------------------------------------------------
        # 1. Detect section from the page before chunking
        # -------------------------------------------------

        if is_contents_page(document):

            # Contents pages list chapter names but are
            # not themselves document sections.
            detected_section = ""

        else:

            detected_section = detect_section(
                document["text"]
            )

        # Update the current section only when a real
        # section heading is found.
        if detected_section:
            current_section = detected_section

        # -------------------------------------------------
        # 2. Split page into smaller chunks
        # -------------------------------------------------

        split_texts = splitter.split_text(
            document["text"]
        )

        # Identify document type once per page.
        document_type = get_document_type(
            document["source"]
        )

        # -------------------------------------------------
        # 3. Add metadata to every chunk
        # -------------------------------------------------

        for chunk in split_texts:

            chunks.append(
                {
                    "text": chunk,
                    "source": document["source"],
                    "page": document["page"],
                    "section": current_section,
                    "document_type": document_type,
                    "chunk_id": f"chunk_{chunk_counter}",
                }
            )

            chunk_counter += 1

    return chunks