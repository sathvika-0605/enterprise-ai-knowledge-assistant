import streamlit as st
import requests


# Page configuration
st.set_page_config(
    page_title="Enterprise AI Knowledge Assistant",
    page_icon="🏢",
    layout="centered"
)


# Application title
st.title("🏢 Enterprise AI Knowledge Assistant")

st.write(
    "Ask questions about company policies and documents."
)


# Question input
question = st.text_area(
    "Ask your question",
    placeholder="Example: How many Privilege Leave days are employees entitled?",
    height=100
)


# Ask button
if st.button("🔍 Ask Question"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching company documents..."):

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={
                        "question": question
                    }
                )

                if response.status_code == 200:

                    data = response.json()

                    st.subheader("Answer")

                    st.write(data["answer"])


                    st.subheader("Sources")

                    for source in data["sources"]:

                        st.write(
                            f"📄 {source['source']} | Page {source['page']}"
                        )

                else:

                    st.error(
                        f"Backend error: {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the FastAPI backend. "
                    "Please make sure the backend is running."
                )