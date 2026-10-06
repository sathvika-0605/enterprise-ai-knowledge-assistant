from pathlib import Path

import pymupdf
import pdfplumber


# =========================================================
# Helper: Check whether two bounding boxes overlap
# =========================================================

def boxes_overlap(box1, box2):
    """
    Check whether two rectangles overlap.

    box format:
    (x0, y0, x1, y1)
    """

    x0_1, y0_1, x1_1, y1_1 = box1
    x0_2, y0_2, x1_2, y1_2 = box2

    if x1_1 <= x0_2:
        return False

    if x0_1 >= x1_2:
        return False

    if y1_1 <= y0_2:
        return False

    if y0_1 >= y1_2:
        return False

    return True


# =========================================================
# Helper: Extract tables from a PDF page
# =========================================================

def extract_tables_from_page(pdf_page):
    """
    Extract tables from one page using pdfplumber.

    Returns tables as structured text.
    """

    tables_text = []

    try:

        tables = pdf_page.find_tables()

        for table_index, table in enumerate(
            tables,
            start=1
        ):

            rows = table.extract()

            if not rows:
                continue

            clean_rows = []

            for row in rows:

                if not row:
                    continue

                cleaned_row = []

                for cell in row:

                    if cell is None:
                        cell = ""

                    cell = str(cell)

                    cell = cell.replace(
                        "\n",
                        " "
                    )

                    cell = " ".join(
                        cell.split()
                    )

                    cleaned_row.append(cell)

                clean_rows.append(
                    cleaned_row
                )

            if not clean_rows:
                continue

            tables_text.append(
                f"\n[TABLE {table_index}]\n"
            )

            for row in clean_rows:

                tables_text.append(
                    " | ".join(row)
                )

            tables_text.append(
                "[END TABLE]\n"
            )

    except Exception as error:

        print(
            f"Table extraction warning: {error}"
        )

    return "\n".join(tables_text)


# =========================================================
# Helper: Extract text blocks
# =========================================================

def extract_text_blocks(
    pymupdf_page,
    table_bboxes
):
    """
    Extract text blocks using PyMuPDF.

    Table areas are excluded because tables are extracted
    separately using pdfplumber.
    """

    blocks = pymupdf_page.get_text(
        "blocks"
    )

    text_blocks = []

    for block in blocks:

        if len(block) < 7:
            continue

        x0, y0, x1, y1, text, block_number, block_type = block[:7]

        # Skip image blocks
        if block_type == 1:
            continue

        if not text:
            continue

        text = text.strip()

        if not text:
            continue

        block_bbox = (
            x0,
            y0,
            x1,
            y1
        )

        # Skip blocks that belong to tables
        inside_table = False

        for table_bbox in table_bboxes:

            if boxes_overlap(
                block_bbox,
                table_bbox
            ):

                inside_table = True
                break

        if inside_table:
            continue

        text_blocks.append(
            {
                "x0": x0,
                "y0": y0,
                "x1": x1,
                "y1": y1,
                "text": text,
            }
        )

    return text_blocks


# =========================================================
# Helper: Arrange text blocks
# =========================================================

def arrange_text_blocks(
    blocks,
    page_width
):
    """
    Arrange text blocks in a better reading order.

    Handles:
    - normal single-column pages
    - simple two-column layouts
    - full-width headings
    """

    if not blocks:
        return []

    # -----------------------------------------------------
    # Identify possible column positions
    # -----------------------------------------------------

    x_positions = sorted(
        block["x0"]
        for block in blocks
    )

    # -----------------------------------------------------
    # Detect a possible large gap between columns
    # -----------------------------------------------------

    column_split = None

    if len(x_positions) >= 4:

        gaps = []

        for index in range(
            len(x_positions) - 1
        ):

            gap = (
                x_positions[index + 1]
                - x_positions[index]
            )

            gaps.append(
                (
                    gap,
                    index
                )
            )

        largest_gap, gap_index = max(
            gaps,
            key=lambda item: item[0]
        )

        # A large horizontal gap may indicate
        # two columns.
        if largest_gap > page_width * 0.15:

            left_values = x_positions[
                :gap_index + 1
            ]

            right_values = x_positions[
                gap_index + 1:
            ]

            if left_values and right_values:

                left_max = max(
                    left_values
                )

                right_min = min(
                    right_values
                )

                if right_min > left_max:

                    column_split = (
                        left_max + right_min
                    ) / 2

    # -----------------------------------------------------
    # If two columns detected
    # -----------------------------------------------------

    if column_split is not None:

        left_column = []
        right_column = []
        full_width = []

        for block in blocks:

            block_width = (
                block["x1"]
                - block["x0"]
            )

            # Blocks covering most of the page
            # are treated as full-width content.
            if block_width > page_width * 0.70:

                full_width.append(
                    block
                )

            elif block["x0"] < column_split:

                left_column.append(
                    block
                )

            else:

                right_column.append(
                    block
                )

        left_column.sort(
            key=lambda block: (
                block["y0"],
                block["x0"]
            )
        )

        right_column.sort(
            key=lambda block: (
                block["y0"],
                block["x0"]
            )
        )

        full_width.sort(
            key=lambda block: (
                block["y0"],
                block["x0"]
            )
        )

        # For simple layouts, combine full-width
        # headings with the column content based
        # on their vertical position.
        ordered_blocks = []

        for block in full_width:

            ordered_blocks.append(
                block
            )

        ordered_blocks.extend(
            left_column
        )

        ordered_blocks.extend(
            right_column
        )

        return ordered_blocks

    # -----------------------------------------------------
    # Normal single-column page
    # -----------------------------------------------------

    blocks.sort(
        key=lambda block: (
            block["y0"],
            block["x0"]
        )
    )

    return blocks


# =========================================================
# Main PDF Loader
# =========================================================

def load_pdf(file_path: str):

    source = Path(file_path).name

    pages = []

    # -----------------------------------------------------
    # Open PDF using both libraries
    # -----------------------------------------------------

    pymupdf_document = pymupdf.open(
        file_path
    )

    plumber_document = pdfplumber.open(
        file_path
    )

    try:

        for page_number, pymupdf_page in enumerate(
            pymupdf_document,
            start=1
        ):

            # =================================================
            # 1. Get page dimensions
            # =================================================

            page_width = pymupdf_page.rect.width

            # =================================================
            # 2. Detect tables
            # =================================================

            plumber_page = plumber_document.pages[
                page_number - 1
            ]

            table_bboxes = []

            try:

                tables = plumber_page.find_tables()

                for table in tables:

                    if table.bbox:

                        table_bboxes.append(
                            tuple(table.bbox)
                        )

            except Exception as error:

                print(
                    f"Table detection warning on page "
                    f"{page_number}: {error}"
                )

            # =================================================
            # 3. Extract normal text blocks
            # =================================================

            text_blocks = extract_text_blocks(
                pymupdf_page,
                table_bboxes
            )

            # =================================================
            # 4. Arrange blocks
            # =================================================

            ordered_blocks = arrange_text_blocks(
                text_blocks,
                page_width
            )

            # =================================================
            # 5. Combine text blocks
            # =================================================

            text_parts = []

            for block in ordered_blocks:

                block_text = block["text"]

                block_text = block_text.strip()

                if block_text:

                    text_parts.append(
                        block_text
                    )

            normal_text = "\n\n".join(
                text_parts
            )

            # =================================================
            # 6. Extract tables
            # =================================================

            table_text = extract_tables_from_page(
                plumber_page
            )

            # =================================================
            # 7. Combine page content
            # =================================================

            page_content = normal_text.strip()

            if table_text.strip():

                if page_content:

                    page_content += (
                        "\n\n"
                        + table_text.strip()
                    )

                else:

                    page_content = (
                        table_text.strip()
                    )

            # =================================================
            # 8. Store page
            # =================================================

            if page_content:

                pages.append(
                    {
                        "text": page_content,
                        "page": page_number,
                        "source": source,
                    }
                )

    finally:

        plumber_document.close()

        pymupdf_document.close()

    return pages