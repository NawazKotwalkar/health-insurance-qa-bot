# Insurance Policy RAG Assistant

An end-to-end Retrieval-Augmented Generation (RAG) system designed to answer natural language questions grounded in complex health insurance policy documents. 

This project demonstrates practical GenAI and LLM engineering skills, specifically around document ingestion, text embedding, semantic vector search, and LLM context-window management. It features a completely custom, highly polished UI built entirely in Streamlit.

## Architecture

The pipeline consists of four main components:
1. **Extraction (`ingestion/extract.py`)**: Reads PDF policy documents (like a CMS Summary of Benefits and Coverage or full policy wordings), extracts text page-by-page, and splits it into overlapping chunks.
2. **Indexing (`ingestion/build_index.py`)**: Sends chunks to Google's Gemini API to generate vector embeddings (`models/gemini-embedding-2`), and stores them in a local persistent ChromaDB vector database.
3. **Retrieval & Generation (`rag/query.py`)**: Embeds user questions, performs a semantic similarity search against ChromaDB to retrieve the top 5 most relevant policy chunks, and passes them as context to a Gemini LLM (`gemini-3.5-flash`) to generate a grounded answer with page citations.
4. **User Interface (`app/streamlit_app.py`)**: A Streamlit chat UI that wraps the retrieval and generation pipeline into an interactive chatbot experience. The UI features a heavy-CSS structural overhaul, leveraging Tailwind-inspired glassmorphism, custom typography, animated gradient backgrounds, and an isolated chat container to emulate a premium SaaS web application.

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/insurance-policy-rag.git
   cd insurance-policy-rag
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   Create a `.env` file in the root directory and insert your Gemini API Key.
   ```env
   GEMINI_API_KEY="your_api_key_here"
   ```
   *Get a free API key at [Google AI Studio](https://aistudio.google.com/)*

4. **Build the Vector Index:**
   Run the ingestion script to process the PDFs in the `data/` folder and build the `chroma_db` database.
   ```bash
   python ingestion/build_index.py
   ```

5. **Run the Application:**
   Launch the Streamlit chat interface.
   ```bash
   streamlit run app/streamlit_app.py
   ```

## Example Queries
* "What is the overall deductible?"
* "What is the waiting period for critical illness coverage?"
* "Are maternity benefits covered?"

## Built With
* [Gemini API](https://ai.google.dev/) - LLM and Text Embeddings
* [ChromaDB](https://www.trychroma.com/) - Vector Database
* [Streamlit](https://streamlit.io/) - Web Interface
* [PyPDF](https://pypdf.readthedocs.io/) - Document Parsing
