import streamlit as st
import requests


# =========================================================
# CONFIGURATION
# =========================================================

API_URL = "http://127.0.0.1:8000"


# =========================================================
# KNOWLEDGE BASE INFORMATION
# =========================================================

# Current V2 knowledge base:
# 3 documents
# 43 pages
# 117 chunks
#
# ChromaDB is accessed by the FastAPI backend.
# Streamlit only communicates with FastAPI.

chunk_count = 117


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Enterprise AI Knowledge Assistant",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* -----------------------------------------------------
       Main container
       ----------------------------------------------------- */

    .block-container {
        max-width: 1200px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }


    /* -----------------------------------------------------
       Header
       ----------------------------------------------------- */

    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-top: 0.5rem;
        margin-bottom: 0.4rem;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 2rem;
    }


    /* -----------------------------------------------------
       Section titles
       ----------------------------------------------------- */

    .section-title {
        font-size: 1.35rem;
        font-weight: 650;
        margin-top: 1.4rem;
        margin-bottom: 0.7rem;
    }


    /* -----------------------------------------------------
       Answer
       ----------------------------------------------------- */

    .answer-box {
        background-color: #f8fafc;
        border: 1px solid #dbe4ee;
        border-radius: 12px;
        padding: 1.4rem;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }


    /* -----------------------------------------------------
       Grounded status
       ----------------------------------------------------- */

    .grounded-box {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 1rem;
        color: #166534;
        font-weight: 600;
    }


    .not-grounded-box {
        background-color: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 1rem;
        color: #9a3412;
        font-weight: 600;
    }


    /* -----------------------------------------------------
       Sources
       ----------------------------------------------------- */

    .source-box {
        background-color: #ffffff;
        border: 1px solid #dbe4ee;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.7rem;
    }

    .source-file {
        font-weight: 650;
        font-size: 1rem;
    }

    .source-details {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }


    /* -----------------------------------------------------
       Suggested questions
       ----------------------------------------------------- */

    .suggestion-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.8rem;
        margin-top: 0.5rem;
        color: #475569;
    }


    /* -----------------------------------------------------
       Footer
       ----------------------------------------------------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "## 🏢 Enterprise AI"
    )

    st.markdown(
        "### Knowledge Assistant"
    )

    st.divider()

    st.markdown(
        "### ⚙️ System"
    )

    st.markdown(
        """
        **Retrieval:** Hybrid Search  
        **Vector Store:** ChromaDB  
        **Keyword Search:** BM25  
        **Re-ranker:** Cross-Encoder  
        **LLM:** Llama 3.2 3B  
        **Embeddings:** all-MiniLM-L6-v2
        """
    )

    st.divider()

    st.markdown(
        "### 📚 Knowledge Base"
    )

    st.markdown(
        f"""
        **Documents:** 3  
        **Pages:** 43  
        **Chunks:** {chunk_count}
        """
    )

    st.divider()

    st.markdown(
        "### 💡 Example Questions"
    )

    st.markdown(
        """
        • How many Casual/Sick Leave days are employees entitled to?

        • Is WFH allowed as a standard practice?

        • How many days of WFH are allowed for caregiving?

        • How many weeks of maternity benefit are provided?

        • How many employees are required for EPF provisions?
        """
    )

    st.divider()

    st.caption(
        "RAG Assistant v2"
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="main-title">
        🏢 Enterprise AI Knowledge Assistant
    </div>

    <div class="subtitle">
        Ask questions and get answers from enterprise documents
        using Retrieval-Augmented Generation
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# QUESTION SECTION
# =========================================================

st.markdown(
    '<div class="section-title">💬 Ask your question</div>',
    unsafe_allow_html=True
)


question = st.text_area(
    "Question",
    placeholder=(
        "Example: How many Privilege Leave days "
        "are employees entitled to?"
    ),
    height=120,
    label_visibility="collapsed"
)


# =========================================================
# BUTTONS
# =========================================================

col1, col2 = st.columns([5, 1])


with col1:

    ask_button = st.button(
        "🔍 Ask Question",
        use_container_width=True
    )


with col2:

    clear_button = st.button(
        "🗑️ Clear",
        use_container_width=True
    )


if clear_button:

    st.rerun()


# =========================================================
# SUGGESTED QUESTIONS
# =========================================================

st.markdown(
    '<div class="section-title">💡 Suggested Questions</div>',
    unsafe_allow_html=True
)


suggestions = [
    "How many Casual/Sick Leave days are employees entitled to annually?",
    "Is WFH allowed as a standard practice?",
    "How many days can employees get to care for an immediate family member?",
    "How many weeks of maternity benefit are provided?",
]


for suggestion in suggestions:

    st.markdown(
        f"""
        <div class="suggestion-box">
            {suggestion}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PROCESS QUESTION
# =========================================================

if ask_button:

    if not question.strip():

        st.warning(
            "Please enter a question before asking."
        )

    else:

        with st.spinner(
            "Searching enterprise documents and generating answer..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "question": question
                    },
                    timeout=180
                )


                # =================================================
                # SUCCESS
                # =================================================

                if response.status_code == 200:

                    data = response.json()


                    # -------------------------------------------------
                    # Answer
                    # -------------------------------------------------

                    st.markdown(
                        '<div class="section-title">📝 Answer</div>',
                        unsafe_allow_html=True
                    )


                    st.markdown(
                        '<div class="answer-box">',
                        unsafe_allow_html=True
                    )


                    st.write(
                        data.get(
                            "answer",
                            "No answer was returned."
                        )
                    )


                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )


                    # -------------------------------------------------
                    # Grounding status
                    # -------------------------------------------------

                    grounded = data.get(
                        "grounded",
                        False
                    )


                    if grounded:

                        st.markdown(
                            """
                            <div class="grounded-box">
                                ✅ Answer grounded in the provided documents
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            """
                            <div class="not-grounded-box">
                                ⚠️ The answer could not be supported by
                                the provided documents
                            </div>
                            """,
                            unsafe_allow_html=True
                        )


                    # -------------------------------------------------
                    # Sources
                    # -------------------------------------------------

                    if grounded:

                        st.markdown(
                            '<div class="section-title">📚 Sources</div>',
                            unsafe_allow_html=True
                        )


                        sources = data.get(
                            "sources",
                            []
                        )


                        # ---------------------------------------------
                        # Remove duplicate source + page combinations
                        # ---------------------------------------------

                        unique_sources = []

                        seen_sources = set()


                        for source in sources:

                            source_name = source.get(
                                "source",
                                "Unknown"
                            )

                            page = source.get(
                                "page",
                                "Unknown"
                            )

                            key = (
                                source_name,
                                page
                            )


                            if key not in seen_sources:

                                unique_sources.append(
                                    source
                                )

                                seen_sources.add(
                                    key
                                )


                        # ---------------------------------------------
                        # Display sources
                        # ---------------------------------------------

                        if unique_sources:

                            for source in unique_sources:

                                source_name = source.get(
                                    "source",
                                    "Unknown"
                                )

                                page = source.get(
                                    "page",
                                    "Unknown"
                                )

                                section = source.get(
                                    "section",
                                    ""
                                )


                                st.markdown(
                                    '<div class="source-box">',
                                    unsafe_allow_html=True
                                )


                                st.markdown(
                                    f"""
                                    <div class="source-file">
                                        📄 {source_name}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )


                                st.markdown(
                                    f"""
                                    <div class="source-details">
                                        Page: {page}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )


                                if section:

                                    st.markdown(
                                        f"""
                                        <div class="source-details">
                                            Section: {section}
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )


                                st.markdown(
                                    '</div>',
                                    unsafe_allow_html=True
                                )


                        else:

                            st.info(
                                "No supporting sources were returned."
                            )


                    else:

                        st.info(
                            "Sources are hidden because the answer "
                            "was not supported by the provided documents."
                        )


                # =================================================
                # BACKEND ERROR
                # =================================================

                else:

                    try:

                        error_data = response.json()

                        error_message = error_data.get(
                            "detail",
                            "An error occurred."
                        )

                    except Exception:

                        error_message = (
                            "An error occurred while "
                            "processing your question."
                        )


                    st.error(
                        f"Backend error: {error_message}"
                    )


            # =====================================================
            # CONNECTION ERROR
            # =====================================================

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the FastAPI backend."
                )

                st.info(
                    "Please start the FastAPI application using:"
                )

                st.code(
                    "uvicorn app.api:app --reload"
                )


            # =====================================================
            # TIMEOUT
            # =====================================================

            except requests.exceptions.Timeout:

                st.error(
                    "The request took too long to complete."
                )

                st.info(
                    "The local Llama model may still be processing "
                    "the request. Please try again."
                )


            # =====================================================
            # OTHER ERROR
            # =====================================================

            except Exception as error:

                st.error(
                    f"Unexpected error: {error}"
                )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Enterprise AI Knowledge Assistant
        • RAG Assistant v2
        • Hybrid Search
        • Cross-Encoder Re-ranking
        • Grounded Answers
    </div>
    """,
    unsafe_allow_html=True
)