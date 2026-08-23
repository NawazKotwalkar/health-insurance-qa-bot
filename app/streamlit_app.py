"""
streamlit_app.py
Heavy CSS, Tailwind-inspired ultra-premium UI.
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

# 2. Heavy CSS / Tailwind-Inspired Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide the default Streamlit sidebar toggle and top bar */
    [data-testid="collapsedControl"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    
    /* Elegant Custom Scrollbar */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
    
    /* Heavy CSS: Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #f8fafc, #f1f5f9, #e2e8f0, #f8fafc);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .block-container {
        max-width: 950px !important;
        padding-top: 3rem !important;
    }

    /* Heavy CSS: Tailwind-style Gradient Text for Title */
    .outside-heading {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .outside-subtitle {
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 2.5rem;
        text-align: center;
        letter-spacing: -0.01em;
    }
    
    /* Highlight word in subtitle */
    .highlight-badge {
        background: linear-gradient(to right, #ec4899, #8b5cf6);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px; /* tailwind rounded-full */
        font-size: 0.85rem;
        font-weight: 600;
        vertical-align: middle;
        margin-left: 0.5rem;
    }

    /* Heavy CSS: Glassmorphism / Elevated Card */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -4px rgba(0, 0, 0, 0.05), inset 0 0 0 1px rgba(255,255,255,0.5) !important;
        border: 1px solid rgba(226, 232, 240, 0.8) !important;
        padding: 2rem !important;
    }

    /* Heavy CSS: Chat Message Entry Animation */
    @keyframes slideUpFade {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Chat Messages Restyling */
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0.5rem !important;
        margin-bottom: 1.5rem !important;
        animation: slideUpFade 0.4s ease-out forwards;
    }
    
    /* User Message Bubble (Tailwind style) */
    .stChatMessage:not(:has(.assistant-avatar)) {
        background-color: #f8fafc !important;
        border-radius: 16px;
        border: 1px solid #f1f5f9 !important;
        padding: 1rem 1.5rem !important;
    }

    .stChatMessage .stMarkdown p {
        color: #334155 !important; /* text-slate-700 */
        font-size: 16px;
        line-height: 1.7;
    }
    
    /* Premium Avatars */
    .stChatMessage:has(.assistant-avatar) [data-testid="stChatAvatar"] {
        background: linear-gradient(135deg, #0f172a, #1e293b) !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .stChatMessage:not(:has(.assistant-avatar)) [data-testid="stChatAvatar"] {
        background: #e2e8f0 !important;
        color: #475569 !important;
    }

    /* Heavy CSS: Floating Chat Input Box (Tailwind dark mode style) */
    .stChatInputContainer {
        background-color: #0f172a !important; /* bg-slate-900 */
        border: 1px solid #1e293b !important; /* border-slate-800 */
        border-radius: 16px !important; /* rounded-2xl */
        padding: 0.5rem 1.2rem !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease;
    }
    
    /* Input hover/focus effects */
    .stChatInputContainer:hover {
        box-shadow: 0 25px 30px -5px rgba(0, 0, 0, 0.15);
        border-color: #334155 !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #8b5cf6 !important; /* violet-500 ring */
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
    }

    div[data-testid="stChatInput"] {
        padding-bottom: 0 !important;
        margin-top: auto !important;
    }

    .stChatInputContainer textarea {
        color: #f8fafc !important; /* text-slate-50 */
        font-size: 16px !important;
    }
    
    /* Stylish Send Button */
    .stChatInputContainer button {
        background: #334155 !important;
        color: #f8fafc !important;
        border-radius: 10px !important;
        transition: background-color 0.2s;
    }
    .stChatInputContainer button:hover {
        background: #475569 !important;
    }
    
    /* Tailored Expander */
    .streamlit-expanderHeader p {
        color: #64748b !important;
        font-weight: 600;
        font-size: 0.9rem;
    }
    [data-testid="stExpander"] {
        background: #f8fafc;
        border: 1px dashed #cbd5e1;
        border-radius: 12px;
        transition: all 0.2s ease;
    }
    [data-testid="stExpander"]:hover {
        border-color: #94a3b8;
        background: #f1f5f9;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header OUTSIDE the box with Tailwind style badges
st.markdown("""
<div class="outside-heading">Insurance Policy RAG</div>
<div class="outside-subtitle">
    Retrieval-Augmented Generation pipeline <span class="highlight-badge">Gemini + ChromaDB</span>
</div>
""", unsafe_allow_html=True)

# 4. The White Box Container
main_card = st.container(border=True)

with main_card:
    chat_container = st.container(height=500, border=False)

    with chat_container:
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "👋 Hello! I am the RAG Assistant. Ask me anything about the indexed CMS or Niva Bupa policy documents."
            })

        for msg in st.session_state.messages:
            if msg["role"] == "assistant":
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

    # Chat Input 
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
