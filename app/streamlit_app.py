"""
streamlit_app.py
Custom UI matching the provided design mockup.
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
    initial_sidebar_state="expanded"
)

# 2. Custom CSS to match the design precisely
st.markdown("""
<style>
    /* Global App Background (Light Gray with subtle pattern feel) */
    .stApp {
        background-color: #f7f9fc;
    }
    
    /* Center the main headers to match the mockup */
    .top-header {
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        margin-top: 1rem;
    }
    .top-title {
        color: #0b1120;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .top-subtitle {
        color: #be2959;
        font-size: 1.4rem;
        font-weight: 500;
        margin-bottom: 3rem;
    }

    /* Target the main block container to act as the right-side of the white card */
    .block-container {
        background-color: #ffffff;
        border-radius: 0 20px 20px 0;
        box-shadow: 10px 10px 30px rgba(0,0,0,0.05);
        padding: 3rem !important;
        max-width: 1000px !important;
        margin-top: 2rem;
        margin-bottom: 2rem;
        border-top: 1px solid #eaeaea;
        border-right: 1px solid #eaeaea;
        border-bottom: 1px solid #eaeaea;
    }

    /* Sidebar to act as the left pink panel of the card */
    [data-testid="stSidebar"] {
        background-color: #fdeef3 !important; /* Soft pink */
        border-right: 1px solid #f6dce5 !important;
        box-shadow: -5px 10px 30px rgba(0,0,0,0.02);
    }
    
    /* Sidebar content typography */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #0b1120 !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] p {
        color: #0b1120 !important;
    }

    /* Chat Messages - NO bubbles, just plain text matching the mockup */
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* Make chat text dark black */
    .stChatMessage .stMarkdown p {
        color: #0b1120 !important;
        font-size: 16px;
        line-height: 1.6;
    }

    /* Chat Input Container - Pink Box like the mockup */
    .stChatInputContainer {
        background-color: #fcd5e3 !important;
        border: 2px solid #ed9ebc !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
        box-shadow: 0 4px 15px rgba(237, 158, 188, 0.2) !important;
    }
    
    .stChatInputContainer textarea {
        color: #0b1120 !important;
        background: transparent !important;
    }
    
    /* Style the send button inside the chat input */
    .stChatInputContainer button {
        background-color: #ef476f !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* Hide the default Streamlit top bar decorations */
    header {visibility: hidden;}
    
    /* Expander / Sources styling to match the clean look */
    .streamlit-expanderHeader p {
        color: #be2959 !important;
        font-weight: 600;
    }
    [data-testid="stExpander"] {
        background: transparent;
        border: 1px solid #eaeaea;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Top Headers (Outside the main container logic if possible, 
# but Streamlit forces it inside the block-container. We will just render them at the top)
st.markdown("<div class='top-header'><div class='top-title'>Health Insurance AI</div><div class='top-subtitle'>Secure, grounded answers from your policy documents.</div></div>", unsafe_allow_html=True)

# 4. Sidebar UI (The left pink panel)
with st.sidebar:
    st.markdown("<h2>System Settings</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("#### ✨ System Core")
    st.markdown("#### ⚙️ Architecture")
    st.markdown(
        """
        LLM: Gemini 3.5 Flash  
        Embed: Gemini-Embedding-2  
        Vector: ChromaDB  
        """
    )
    
    st.markdown("<br><hr style='background-color: #f6dce5; height: 1px; border: none;'><br>", unsafe_allow_html=True)
    
    st.markdown("#### 📄 Knowledge Base")
    st.markdown("✅ CMS Summary of Benefits")
    st.markdown("✅ Niva Bupa Policy Wording")

# 5. Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add the default greeting from the mockup
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "👋 Hello! I am your Health Insurance AI Assistant. Ask me anything about your coverage, limits, or claims from your Niva Bupa and CMS policy documents."
    })

# Display chat messages from history
for msg in st.session_state.messages:
    # Use specific emojis that look like the mockup's avatars
    avatar = "👤" if msg["role"] == "user" else "🧬"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("View Sources"):
                for s in msg["sources"]:
                    st.markdown(f"**{s['source']}** — Page {s['page']}")

# Handle new question
question = st.chat_input("Ask about your coverage, limits, or claims...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar="👤"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="🧬"):
        with st.spinner("Searching documents..."):
            try:
                result = answer_question(question)
                st.markdown(result["answer"])
                
                # Format sources nicely
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
