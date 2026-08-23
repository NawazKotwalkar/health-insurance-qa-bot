"""
streamlit_app.py
Unified chatbox UI with heading, chat, and clear button inside a single container.
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
    
    /* The Unified Main Card */
    .main-card {
        background-color: #ffffff;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        border: 1px solid #eaeaea;
        padding: 2rem;
        max-width: 900px;
        margin: 2rem auto;
    }

    /* Target Streamlit's block container to act as the main card wrapper */
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stVerticalBlock"]) {
        background-color: #ffffff;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        border: 1px solid #eaeaea;
        padding: 2.5rem !important;
        max-width: 900px;
        margin: 0 auto;
    }

    /* Heading inside the card */
    .card-title {
        color: #0b1120;
        font-size: 2.5rem;
        font-weight: 800;
        font-family: 'Helvetica Neue', sans-serif;
        margin-bottom: 0.2rem;
    }
    .card-subtitle {
        color: #be2959;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 2rem;
    }

    /* Clear Button styling */
    .stButton>button {
        background-color: #f6dce5 !important;
        color: #be2959 !important;
        border: 1px solid #ed9ebc !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        float: right;
        margin-top: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #fcd5e3 !important;
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
        margin-top: 1.5rem !important;
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

# 3. Everything is now inside one unified block

# Header row with title and clear button
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
    <div>
        <div class="card-title">Insurance Policy RAG</div>
        <div class="card-subtitle">Retrieval-Augmented Generation pipeline using Gemini & ChromaDB.</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.divider()

# 4. Chat Container
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
