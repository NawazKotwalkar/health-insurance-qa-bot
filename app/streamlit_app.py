"""
streamlit_app.py
Completely restructured UI layout to perfectly match the mockup.
No native sidebar is used. The entire layout is a custom floating card.
"""

import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))
from rag.query import answer_question

# 1. Page Configuration
st.set_page_config(
    page_title="Health Insurance AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide the default sidebar completely
)

# 2. Structural CSS Injection
st.markdown("""
<style>
    /* Hide the default Streamlit sidebar toggle and top bar */
    [data-testid="collapsedControl"] { display: none; }
    header { visibility: hidden; }
    
    /* Global App Background - matches the light gray/white abstract bg */
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
        font-size: 3.5rem;
        font-weight: 800;
        font-family: 'Helvetica Neue', sans-serif;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #be2959;
        font-size: 1.3rem;
        font-weight: 500;
    }

    /* Target the inner Horizontal Block that holds our 2 panes to make it a unified Card */
    [data-testid="column"]:nth-of-type(2) [data-testid="stHorizontalBlock"] {
        background-color: #ffffff;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        overflow: hidden; /* Ensure inner columns don't break the border radius */
        border: 1px solid #eaeaea;
    }

    /* Left Pane (Pink Panel) */
    [data-testid="column"]:nth-of-type(2) [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(1) {
        background-color: #fcedf2;
        padding: 2.5rem 2rem !important;
        border-right: 1px solid #f6dce5;
    }
    
    /* Right Pane (White Chat Area) */
    [data-testid="column"]:nth-of-type(2) [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(2) {
        background-color: #ffffff;
        padding: 2.5rem !important;
    }

    /* Left Panel Typography */
    [data-testid="column"]:nth-of-type(2) [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(1) h1, 
    [data-testid="column"]:nth-of-type(2) [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(1) h2, 
    [data-testid="column"]:nth-of-type(2) [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(1) h3 {
        color: #0b1120 !important;
        font-weight: 700 !important;
        margin-bottom: 1rem;
    }
    [data-testid="column"]:nth-of-type(2) [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-of-type(1) p {
        color: #111111 !important;
        line-height: 1.8;
    }

    /* Chat Messages - Plain text, no bubbles */
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin-bottom: 1.5rem !important;
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
        padding: 0.5rem !important;
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

    /* Hide the bottom 'Made with Streamlit' footer */
    footer {visibility: hidden;}
    
    /* Adjust expander styling */
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

# 3. Top Header Section
st.markdown("""
<div class="main-header-container">
    <div class="main-title">Health Insurance AI</div>
    <div class="sub-title">Secure, grounded answers from your policy documents.</div>
</div>
""", unsafe_allow_html=True)

# 4. The Master Card Layout using Columns (1:2.5 ratio)
# To ensure the card is centered and restricted in width, we put it inside an outer container
outer_spacer1, card_col, outer_spacer2 = st.columns([1, 8, 1])

with card_col:
    # Inside the card_col, we create the dual-pane layout
    left_pane, right_pane = st.columns([1, 2.2], gap="large")

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
        
        st.markdown("<hr style='background-color: #f6dce5; height: 1px; border: none; margin: 2rem 0;'>", unsafe_allow_html=True)
        
        st.markdown("#### 📄 Knowledge Base")
        st.markdown("✅ CMS Summary of Benefits")
        st.markdown("✅ Niva Bupa Policy Wording")

    # --- RIGHT PANE: CHAT INTERFACE ---
    with right_pane:
        # Chat history wrapper
        chat_container = st.container(height=500, border=False)
        
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

        # Chat Input at the bottom of the right pane
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
