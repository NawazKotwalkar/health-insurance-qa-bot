"""
streamlit_app.py
Heavy CSS, Tailwind-inspired ultra-premium UI. Mobile-first responsive layout.
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

# 2. Heavy CSS / Tailwind-Inspired Styling — mobile-first base, desktop as enhancement
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    html, body {
        overflow-x: hidden;
    }

    [data-testid="collapsedControl"] { display: none !important; }
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

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

    /* ---- MOBILE-FIRST BASE (applies to all sizes, phones included) ---- */
    .block-container {
        max-width: 950px !important;
        padding-top: 1rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-bottom: 1rem !important;
    }

    .outside-heading {
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 0.35rem;
        background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        line-height: 1.15;
        word-wrap: break-word;
    }
    .outside-subtitle {
        color: #9d174d !important;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1.25rem;
        text-align: center;
        letter-spacing: -0.01em;
        padding: 0 0.5rem;
    }

    .highlight-badge {
        background: linear-gradient(to right, #be185d, #9d174d);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        vertical-align: middle;
        margin-left: 0.4rem;
        display: inline-block;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(236, 72, 153, 0.05), 0 4px 6px -4px rgba(236, 72, 153, 0.05), inset 0 0 0 1px rgba(255,255,255,0.5) !important;
        border: 1px solid rgba(252, 231, 243, 0.8) !important;
        padding: 0.85rem !important;
    }

    @keyframes slideUpFade {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stChatMessage {
        background: #fdf2f8 !important;
        border: 1px solid #fce7f3 !important;
        border-radius: 14px !important;
        box-shadow: 0 2px 5px rgba(236, 72, 153, 0.02) !important;
        padding: 0.75rem 1rem !important;
        margin-bottom: 1rem !important;
        animation: slideUpFade 0.4s ease-out forwards;
        max-width: 100% !important;
        overflow-wrap: break-word;
    }

    .stChatMessage .stMarkdown,
    .stChatMessage .stMarkdown p,
    .stChatMessage .stMarkdown ul,
    .stChatMessage .stMarkdown ol,
    .stChatMessage .stMarkdown li,
    .stChatMessage .stMarkdown span,
    .stChatMessage .stMarkdown strong,
    .stChatMessage .stMarkdown em,
    .stChatMessage .stMarkdown blockquote,
    .stChatMessage .stMarkdown table,
    .stChatMessage .stMarkdown td,
    .stChatMessage .stMarkdown th,
    .stChatMessage .stMarkdown a {
        color: #000000 !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        word-break: break-word;
    }

    /* Tables inside answers need to scroll horizontally on phones instead of overflowing */
    .stChatMessage .stMarkdown table {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
        max-width: 100%;
    }

    .stChatMessage:has(.assistant-avatar) [data-testid="stChatAvatar"] {
        background: linear-gradient(135deg, #ec4899, #be185d) !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 4px 6px -1px rgba(236,72,153,0.2);
    }
    .stChatMessage:not(:has(.assistant-avatar)) [data-testid="stChatAvatar"] {
        background: #fbcfe8 !important;
        color: #831843 !important;
    }

    .stChatInputContainer {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 14px !important;
        padding: 0.4rem 0.9rem !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease;
    }

    .stChatInputContainer:hover {
        box-shadow: 0 25px 30px -5px rgba(236, 72, 153, 0.15);
        border-color: #ec4899 !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #ec4899 !important;
        box-shadow: 0 0 0 2px rgba(236, 72, 153, 0.2) !important;
    }

    div[data-testid="stChatInput"] {
        padding-bottom: 0 !important;
        margin-top: auto !important;
    }

    .stChatInputContainer textarea {
        color: #f8fafc !important;
        font-size: 16px !important; /* 16px prevents iOS Safari auto-zoom on focus */
    }

    /* Touch-friendly send button — minimum 44x44px tap target per mobile guidelines */
    .stChatInputContainer button {
        background: #334155 !important;
        color: #f8fafc !important;
        border-radius: 10px !important;
        transition: background-color 0.2s;
        min-width: 44px !important;
        min-height: 44px !important;
    }
    .stChatInputContainer button:hover {
        background: #ec4899 !important;
    }

    .streamlit-expanderHeader p {
        color: #be185d !important;
        font-weight: 600;
        font-size: 0.85rem;
    }
    [data-testid="stExpander"] {
        background: #fdf2f8;
        border: 1px dashed #fbcfe8;
        border-radius: 12px;
        transition: all 0.2s ease;
    }
    [data-testid="stExpander"]:hover {
        border-color: #ec4899;
        background: #fce7f3;
    }

    /* ---- DESKTOP / LARGER SCREENS: progressive enhancement above phone baseline ---- */
    @media (min-width: 640px) {
        .block-container {
            padding-top: 2rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }
        .outside-heading {
            font-size: 2.4rem;
        }
        .outside-subtitle {
            font-size: 1rem;
            margin-bottom: 1.75rem;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 20px;
            padding: 1.5rem !important;
        }
        .stChatMessage {
            padding: 1rem 1.5rem !important;
            border-radius: 16px !important;
        }
        .stChatMessage .stMarkdown, .stChatMessage .stMarkdown p {
            font-size: 16px !important;
        }
        .stChatInputContainer {
            padding: 0.5rem 1.2rem !important;
            border-radius: 16px !important;
        }
    }

    @media (min-width: 1024px) {
        .outside-heading {
            font-size: 3rem;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 24px;
            padding: 2rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# 3. Header OUTSIDE the box with Tailwind style badges
st.markdown("""
<div class="outside-heading">Insurance Policy RAG</div>
<div class="outside-subtitle">
    Retrieval-Augmented Generation pipeline
</div>
""", unsafe_allow_html=True)

# 4. The White Box Container — chat area height adapts via CSS vh unit instead of a fixed pixel value
main_card = st.container(border=True)

with main_card:
    chat_container = st.container(height=420, border=False)

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