"""
streamlit_app.py
Simple chat UI for asking questions about the indexed insurance policy
documents. Run with:
    streamlit run app/streamlit_app.py
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))
from rag.query import answer_question

st.set_page_config(page_title="Insurance Policy Assistant", page_icon="🏥")

st.title("🏥 Insurance Policy RAG Assistant")
st.caption(
    "Ask questions about the indexed health insurance policy documents. "
    "Answers are grounded strictly in the uploaded policy text."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.write(f"- {s['source']} (page {s['page']})")

question = st.chat_input("Ask about deductibles, coverage, exclusions, claims...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching policy documents..."):
            try:
                result = answer_question(question)
                st.markdown(result["answer"])
                if result["sources"]:
                    with st.expander("Sources"):
                        for s in result["sources"]:
                            st.write(f"- {s['source']} (page {s['page']})")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"],
                })
            except Exception as e:
                error_msg = f"Error: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

with st.sidebar:
    st.header("About")
    st.write(
        "This assistant uses Retrieval-Augmented Generation (RAG) to answer "
        "questions grounded in real health insurance policy documents "
        "(Summary of Benefits & Coverage, full policy wordings)."
    )
    st.write("**Stack:** Gemini API · ChromaDB · Streamlit")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()
