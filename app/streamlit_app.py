"""
streamlit_app.py
Highly Aesthetic, Stable Chat UI with White & Pink Glassmorphism theme.
"""

import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))
from rag.query import answer_question

# 1. Page Configuration
st.set_page_config(
    page_title="Health Policy AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for Stable & Aesthetic White/Pink Glassmorphism
st.markdown("""
<style>
    /* Global App Background - Smooth White to Soft Blush Pink */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%);
        background-attachment: fixed;
    }
    
    /* Base text colors - Dark Black for high contrast readability */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #111111 !important;
        font-size: 16px;
        line-height: 1.7;
    }
    
    /* Main Headers - Aesthetic Pink Accent */
    h1, h2, h3, h4 {
        color: #e91e63 !important; 
        font-family: 'Helvetica Neue', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }

    /* Sidebar styling with stable Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(233, 30, 99, 0.15);
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] p {
        color: #222222 !important;
        font-weight: 500;
    }

    /* Chat Messages - Elevated Glass Bubbles */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(233, 30, 99, 0.08) !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
    }

    /* Chat Input Box - Floating Glass Pill */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 30px !important;
        border: 1px solid rgba(233, 30, 99, 0.25) !important;
        box-shadow: 0 10px 40px rgba(233, 30, 99, 0.12) !important;
        padding: 0.2rem 1rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Chat Input Text */
    .stChatInputContainer textarea {
        color: #111111 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #ff4081 0%, #e91e63 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3) !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(233, 30, 99, 0.4) !important;
    }
    .stButton>button p {
        color: #ffffff !important; /* Keep button text white */
    }
    
    /* Expander / Sources */
    .streamlit-expanderHeader p {
        color: #e91e63 !important;
        font-weight: 700;
    }
    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(233, 30, 99, 0.2);
        border-radius: 12px;
        margin-top: 0.5rem;
    }
    [data-testid="stExpanderDetails"] p {
        color: #444444 !important; /* Slightly softer black for source text */
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar UI 
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>✨ System Core</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("#### ⚙️ Architecture")
    st.markdown(
        """
        - **LLM:** Gemini 3.5 Flash
        - **Embed:** Gemini-Embedding-2
        - **Vector:** ChromaDB
        """
    )
    
    st.divider()
    
    st.markdown("#### 📄 Knowledge Base")
    st.markdown("✅ CMS Summary of Benefits")
    st.markdown("✅ Niva Bupa Policy Wording")
    
    st.divider()
    
    if st.button("✨ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 4. Main Chat Interface
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>Health Insurance AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #e91e63 !important; font-weight: 600; font-size: 1.1em; margin-bottom: 3rem;'>Secure, grounded answers from your policy documents.</p>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "✨"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📄 View Sources"):
                for s in msg["sources"]:
                    st.markdown(f"**{s['source']}** — Page {s['page']}")

# Handle new question
question = st.chat_input("Ask about your coverage, limits, or claims...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="👤"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Searching documents..."):
            try:
                result = answer_question(question)
                st.markdown(result["answer"])
                
                # Format sources nicely
                if result["sources"]:
                    with st.expander("📄 View Sources"):
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
