"""
streamlit_app.py
Simple, repo-oriented chat UI matching the white/pink aesthetic.
"""

import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))
from rag.query import answer_question

# 1. Page Configuration
st.set_page_config(
    page_title="Insurance Policy RAG",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Structural CSS Injection
st.markdown("""
<style>
    /* Hide the default Streamlit sidebar toggle and top bar */
    [data-testid="collapsedControl"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    
    /* Global App Background */
    .stApp {
        background-color: #f7f9fc;
    }
    
    /* Center Title and Subtitle */
    .main-header-container {
        text-align: center;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    .main-title {
        color: #0b1120;
        font-size: 3rem;
        font-weight: 800;
        font-family: 'Helvetica Neue', sans-serif;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        color: #be2959;
        font-size: 1.2rem;
        font-weight: 500;
    }

    /* Wrap the main chat interface in a sleek white card */
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stVerticalBlock"]) {
        background-color: #ffffff;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        border: 1px solid #eaeaea;
        padding: 2rem;
        max-width: 900px;
        margin: 0 auto;
    }

    /* Chat Messages - Plain text, no bubbles */
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 1rem 0 0 !important;
        margin-bottom: 1.2rem !important;
    }
    .stChatMessage .stMarkdown p {
        color: #0b1120 !important;
        font-size: 16px;
        line-height: 1.6;
    }

    /* The Pink Chat Input Box */
    .stChatInputContainer {
        background-color: #fcd5e3 !important;
        border: 2px solid #ed9ebc !important;
        border-radius: 12px !important;
        padding: 0.2rem 1rem !important;
        margin-top: 1rem !important;
    }
    .stChatInputContainer textarea {
        color: #0b1120 !important;
        background: transparent !important;
    }
    .stChatInputContainer button {
        background-color: #ef476f !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader p {
        color: #be2959 !important;
        font-weight: 600;
    }
    [data-testid="stExpander"] {
        background: #fdfdfd;
        border: 1px solid #eaeaea;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Top Header Section (Repo Oriented)
st.markdown("""
<div class="main-header-container">
    <div class="main-title">Insurance Policy RAG</div>
    <div class="sub-title">Retrieval-Augmented Generation pipeline using Gemini & ChromaDB.</div>
</div>
""", unsafe_allow_html=True)

# 4. Single Chat Container (No Sidebar/Left Panel)
chat_container = st.container(height=500, border=False)

with chat_container:
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "👋 Hello! I am the RAG Assistant. Ask me anything about the indexed CMS or Niva Bupa policy documents."
        })

    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "🧬"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("View Sources"):
                    for s in msg["sources"]:
                        st.markdown(f"**{s['source']}** — Page {s['page']}")

# Chat Input at the bottom
question = st.chat_input("Query the vector database...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with chat_container:
        with st.chat_message("user", avatar="👤"):
            st.markdown(question)

        with st.chat_message("assistant", avatar="🧬"):
            with st.spinner("Retrieving contexts..."):
                try:
                    result = answer_question(question)
                    st.markdown(result["answer"])
                    
                    if result["sources"]:
                        with st.expander("View Sources"):
                            for s in result["sources"]:
                                st.markdown(f"**{s['source']}** — Page {s['page']}")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": result["sources"],
                    })
                except Exception as e:
                    error_msg = f"Error: {e}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
