"""
streamlit_app.py
Responsive, robust layout matching the mockup design.
"""

import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))
from rag.query import answer_question

# 1. Page Configuration (Centered layout natively restricts width, which we expand slightly)
st.set_page_config(
    page_title="Health Insurance AI",
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
    
    /* Expand the centered block container to card width and style it */
    .block-container {
        max-width: 1100px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Center Title and Subtitle */
    .main-header-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-title {
        color: #0b1120;
        font-size: 3.2rem;
        font-weight: 800;
        font-family: 'Helvetica Neue', sans-serif;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #be2959;
        font-size: 1.2rem;
        font-weight: 500;
    }

    /* Target the Horizontal Block that holds the left/right panes */
    /* We use a universal selector for the horizontal block directly inside the main vertical block */
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="column"]) {
        background-color: #ffffff;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        border: 1px solid #eaeaea;
        overflow: hidden;
    }

    /* Left Pane (Pink Panel) */
    div[data-testid="column"]:nth-of-type(1) {
        background-color: #fcedf2 !important;
        padding: 2rem 2rem 100% 2rem !important; /* Huge bottom padding to stretch background */
        margin-bottom: -100% !important; /* Offset padding */
        border-right: 1px solid #f6dce5;
    }
    
    /* Right Pane (White Chat Area) */
    div[data-testid="column"]:nth-of-type(2) {
        background-color: #ffffff !important;
        padding: 2rem 2rem 100% 2rem !important; 
        margin-bottom: -100% !important;
    }

    /* Ensure text in the pink panel is dark */
    div[data-testid="column"]:nth-of-type(1) h1, 
    div[data-testid="column"]:nth-of-type(1) h2, 
    div[data-testid="column"]:nth-of-type(1) h3, 
    div[data-testid="column"]:nth-of-type(1) h4 {
        color: #0b1120 !important;
        font-weight: 700 !important;
        margin-bottom: 1rem;
    }
    div[data-testid="column"]:nth-of-type(1) p {
        color: #111111 !important;
        line-height: 1.8;
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

    /* Responsive fix for mobile (when columns stack) */
    @media (max-width: 768px) {
        div[data-testid="column"]:nth-of-type(1),
        div[data-testid="column"]:nth-of-type(2) {
            padding: 2rem !important; 
            margin-bottom: 0 !important;
            border-right: none !important;
        }
        .main-title { font-size: 2.2rem; }
    }
</style>
""", unsafe_allow_html=True)

# 3. Top Header Section
st.markdown("""
<div class="main-header-container">
    <div class="main-title">Health Insurance AI</div>
    <div class="sub-title">Secure, grounded answers from your policy documents.</div>
</div>
""", unsafe_allow_html=True)

# 4. The Master Card Layout using Native Columns
left_pane, right_pane = st.columns([1, 2.2], gap="small")

# --- LEFT PANE: SYSTEM SETTINGS ---
with left_pane:
    st.markdown("## System Settings")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("#### ✨ System Core")
    st.markdown("#### ⚙️ Architecture")
    st.markdown(
        """
        **LLM:** Gemini 3.5 Flash  
        **Embed:** Gemini-Embedding-2  
        **Vector:** ChromaDB  
        """
    )
    
    st.markdown("<hr style='background-color: #f6dce5; height: 1px; border: none; margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    st.markdown("#### 📄 Knowledge Base")
    st.markdown("✅ CMS Summary of Benefits")
    st.markdown("✅ Niva Bupa Policy Wording")

# --- RIGHT PANE: CHAT INTERFACE ---
with right_pane:
    # Use a fixed-height container for scrollable chat history
    chat_container = st.container(height=450, border=False)
    
    with chat_container:
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "👋 Hello! I am your Health Insurance AI Assistant. Ask me anything about your coverage, limits, or claims from your Niva Bupa and CMS policy documents."
            })

        for msg in st.session_state.messages:
            avatar = "👤" if msg["role"] == "user" else "🧬"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])
                if msg.get("sources"):
                    with st.expander("View Sources"):
                        for s in msg["sources"]:
                            st.markdown(f"**{s['source']}** — Page {s['page']}")

    # Chat Input directly below the chat container
    question = st.chat_input("Ask about your coverage, limits, or claims...")
    
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with chat_container:
            with st.chat_message("user", avatar="👤"):
                st.markdown(question)

            with st.chat_message("assistant", avatar="🧬"):
                with st.spinner("Searching documents..."):
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
