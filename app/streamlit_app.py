"""
streamlit_app.py
Premium chat UI with White & Pink Glassmorphism theme.
"""

import sys
from pathlib import Path
import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))
from rag.query import answer_question

# 1. Page Configuration
st.set_page_config(
    page_title="Health Policy AI",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for White & Pink Glassmorphism
st.markdown("""
<style>
    /* Global App Background - Soft White to Pink Gradient */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #ffe4e1 100%);
        background-attachment: fixed;
    }
    
    /* Sidebar styling with Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.5) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.6);
    }

    /* Main Chat Container wrapping */
    .block-container {
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(255, 182, 193, 0.3);
        padding: 3rem !important;
        margin-top: 3rem;
        margin-bottom: 3rem;
    }

    /* Header styling */
    h1 {
        color: #d1477a !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        text-align: center;
        color: #e884a1;
        font-size: 1.1em;
        margin-bottom: 2rem;
        font-weight: 500;
    }

    /* Chat Messages - Individual Bubbles */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.7) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 4px 15px rgba(255, 182, 193, 0.15) !important;
        padding: 1.2rem !important;
        margin-bottom: 1rem !important;
    }

    /* Chat Input Box */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 4px 20px rgba(255, 182, 193, 0.2) !important;
        padding-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #ffb6c1 0%, #ffc0cb 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 10px rgba(255, 182, 193, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(255, 182, 193, 0.6) !important;
    }
    
    /* Expander / Sources */
    .streamlit-expanderHeader {
        background: transparent !important;
        color: #d1477a !important;
        font-weight: 600;
    }
    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar UI 
with st.sidebar:
    st.markdown("<h2 style='color: #d1477a; text-align: center;'>🌸 System Core</h2>", unsafe_allow_html=True)
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
    st.caption("✅ CMS Summary of Benefits")
    st.caption("✅ Niva Bupa Policy Wording")
    
    st.divider()
    
    if st.button("✨ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 4. Main Chat Interface
st.markdown("<h1>Health Insurance AI</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Secure, grounded answers from your policy documents.</p>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🌸"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📄 View Sources"):
                for s in msg["sources"]:
                    st.caption(f"**{s['source']}** — Page {s['page']}")

# Handle new question
question = st.chat_input("Ask about your coverage, limits, or claims...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="👤"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="🌸"):
        with st.spinner("Searching documents..."):
            try:
                result = answer_question(question)
                st.markdown(result["answer"])
                
                # Format sources nicely
                if result["sources"]:
                    with st.expander("📄 View Sources"):
                        for s in result["sources"]:
                            st.caption(f"**{s['source']}** — Page {s['page']}")
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "sources": result["sources"],
                })
            except Exception as e:
                error_msg = f"Error: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
