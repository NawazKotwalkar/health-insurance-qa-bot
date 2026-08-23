"""
streamlit_app.py
Precise match to the user's uploaded chatbox UI.
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
        background-color: #f4f5f7;
    }
    
    /* Heading Outside the Box */
    .outside-heading {
        color: #8a1936;
        font-size: 1.5rem;
        font-weight: 700;
        font-family: 'Helvetica Neue', sans-serif;
        margin-top: 1rem;
        margin-bottom: 0.2rem;
    }
    .outside-subtitle {
        color: #a0a0a0;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }

    /* Target the specific container using the marker class */
    div[data-testid="stVerticalBlock"]:has(.main-card-marker) {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid #e2e2e2;
        padding: 2rem 2rem 2.5rem 2rem !important;
    }

    /* Chat Messages - Plain text, no bubbles */
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin-bottom: 1.2rem !important;
    }
    .stChatMessage .stMarkdown p {
        color: #111111 !important;
        font-size: 15px;
        line-height: 1.5;
    }
    
    /* Custom Avatar Styling to match the dark square in the image */
    .stChatMessage:has(.assistant-avatar) [data-testid="stChatAvatar"] {
        background-color: #13141a !important;
        border-radius: 6px !important;
        border: none !important;
    }

    /* The Dark Charcoal Chat Input Box */
    /* Force it to stay INSIDE the white card */
    .stChatInputContainer {
        position: relative !important;
        bottom: 0 !important;
        background-color: #2b2c36 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.2rem 1rem !important;
        margin-top: 1.5rem !important;
        box-shadow: none !important;
    }
    
    /* Extra wrapper reset to ensure position relative works */
    div[data-testid="stChatInput"] {
        position: static !important;
        padding-bottom: 0 !important;
    }

    .stChatInputContainer textarea {
        color: #8b8d96 !important;
        background: transparent !important;
    }
    .stChatInputContainer button {
        background-color: transparent !important;
        color: #8b8d96 !important;
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

# 3. Header OUTSIDE the box (partially visible in the screenshot)
st.markdown("""
<div class="outside-heading">Insurance Policy RAG</div>
<div class="outside-subtitle">Retrieval-Augmented Generation pipeline using Gemini & ChromaDB.</div>
""", unsafe_allow_html=True)

# 4. The White Box Container
with st.container():
    # Invisible marker to allow CSS targeting of this exact container
    st.markdown("<div class='main-card-marker'></div>", unsafe_allow_html=True)
    
    # Scrollable Chat History
    chat_container = st.container(height=450, border=False)

    with chat_container:
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

    # Chat Input exactly below the chat container inside the white box
    question = st.chat_input("Ask about your coverage, limits, or claims...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with chat_container:
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
