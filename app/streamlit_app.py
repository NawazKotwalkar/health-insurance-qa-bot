"""
streamlit_app.py
Single container UI matching the user's design perfectly.
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

# 2. CSS Injection
st.markdown("""
<style>
    /* Hide the default Streamlit sidebar toggle and top bar */
    [data-testid="collapsedControl"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    
    /* Global App Background */
    .stApp {
        background-color: #f4f5f7;
    }
    
    /* Ensure the main column doesn't exceed a readable width */
    .block-container {
        max-width: 900px !important;
        padding-top: 2rem !important;
    }

    /* Heading Outside the Box */
    .outside-heading {
        color: #8a1936;
        font-size: 2rem;
        font-weight: 800;
        font-family: 'Helvetica Neue', sans-serif;
        margin-bottom: 0.2rem;
    }
    .outside-subtitle {
        color: #71717a;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Target the single Native Streamlit Container */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid #e2e2e2 !important;
        padding: 1.5rem 1.5rem 1rem 1.5rem !important; /* Less padding on the bottom */
    }

    /* Chat Messages - Plain text, no bubbles */
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin-bottom: 1rem !important;
    }
    .stChatMessage .stMarkdown p {
        color: #111111 !important;
        font-size: 15px;
        line-height: 1.6;
    }
    
    /* Custom Avatar Styling to match the dark square in the image */
    .stChatMessage:has(.assistant-avatar) [data-testid="stChatAvatar"] {
        background-color: #13141a !important;
        border-radius: 6px !important;
        border: none !important;
    }

    /* The Dark Charcoal Chat Input Box */
    .stChatInputContainer {
        background-color: #2b2c36 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.2rem 1rem !important;
        margin-top: auto !important; /* Push to bottom of flex container */
        margin-bottom: 0 !important;
    }

    div[data-testid="stChatInput"] {
        padding-bottom: 0 !important;
        margin-top: auto !important; /* Force to bottom of container */
    }

    .stChatInputContainer textarea {
        color: #e4e4e7 !important;
        background: transparent !important;
    }
    .stChatInputContainer button {
        background-color: transparent !important;
        color: #e4e4e7 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader p {
        color: #2b2c36 !important;
        font-weight: 600;
    }
    [data-testid="stExpander"] {
        background: #fdfdfd;
        border: 1px solid #eaeaea;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header OUTSIDE the box
st.markdown("""
<div class="outside-heading">Insurance Policy RAG</div>
<div class="outside-subtitle">Retrieval-Augmented Generation pipeline using Gemini & ChromaDB.</div>
""", unsafe_allow_html=True)

# 4. ONE Single Container for everything
# Using height creates a scrollable area, and natively pins chat_input to the bottom!
main_card = st.container(height=550)

with main_card:
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "👋 Hello! I am the RAG Assistant. Ask me anything about the indexed CMS or Niva Bupa policy documents."
        })

    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            # Inject a hidden span so we can target the avatar with CSS
            st.markdown("<span class='assistant-avatar'></span>", unsafe_allow_html=True)
            avatar = "🧬"
        else:
            avatar = "👤"
            
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("View Sources"):
                    for s in msg["sources"]:
                        st.markdown(f"**{s['source']}** — Page {s['page']}")

    # Chat Input natively sits at the bottom of the container
    question = st.chat_input("Ask about your coverage, limits, or claims...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user", avatar="👤"):
            st.markdown(question)

        # Assistant response
        st.markdown("<span class='assistant-avatar'></span>", unsafe_allow_html=True)
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
