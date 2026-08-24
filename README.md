<div align="center">

# 🧬 Health Insurance AI QA Bot

### *Ask your policy anything. Get answers grounded in the actual document — not AI guesswork.*

![Python](https://img.shields.io/badge/Python-3.10+-be185d?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-ec4899?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-LLM-9d174d?style=for-the-badge&logo=google&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-fbcfe8?style=for-the-badge)

</div>

---

## 1. What Is This Project?

The **Health Insurance AI QA Bot** is an intelligent, context-aware chatbot designed to accurately answer complex questions about specific health insurance policies. Instead of relying on general knowledge (which often leads to AI hallucinations), the bot uses a technique called **Retrieval-Augmented Generation (RAG)** to search through the actual text of uploaded insurance policy PDFs and generate answers strictly based on the official documentation.

## 2. The Problem: Why Build This?

Health insurance policy wordings and Summary of Benefits and Coverage (SBC) documents are notoriously difficult to navigate. They are typically dense, highly technical, and run for dozens or hundreds of pages.

- 🧾 **The Consumer Problem** — Customers struggle to find simple answers to critical questions like *"Is maternity covered?"*, *"What is the waiting period for pre-existing conditions?"*, or *"Do I have dental coverage?"*
- 💸 **The Business Problem** — Insurance companies spend millions of dollars on customer support call centers simply to read policy documents to confused customers.
- 🔍 **The Search Problem** — Traditional "Ctrl+F" keyword search fails because a user might search for "pregnancy" while the document uses the term "maternity."

By leveraging AI embeddings, this project solves the vocabulary mismatch problem and instantly synthesizes human-readable answers from massive documents.

## 3. Who Is This For?

| Audience | Use Case |
|---|---|
| 🙋 **Policyholders (Consumers)** | Instantly understand coverage, limits, and exclusions without waiting on hold for support |
| 🎧 **Customer Support Representatives** | Use the bot as an internal "co-pilot" to rapidly retrieve policy clauses during a live call |
| 💼 **Insurance Sales Agents** | Quickly compare policy nuances to answer client questions accurately before closing a sale |

## 4. Tech Stack

Built to be lightweight, modular, and highly performant using modern Data Science tools:

- **Frontend UI** — [Streamlit](https://streamlit.io/), upgraded with custom Tailwind-inspired CSS, glassmorphism design, and a mobile-first responsive layout
- **Large Language Model** — [Google Gemini](https://aistudio.google.com/), used for both reasoning and text generation
- **Embeddings** — Google Gemini Embedding API, used to convert text into semantic vectors
- **Vector Database** — [ChromaDB](https://www.trychroma.com/), an open-source, local, SQLite-based vector database for rapid semantic search
- **Data Processing** — `pypdf`, for extracting raw text from PDF documents
- **Deployment** — Streamlit Community Cloud, for serverless, public hosting

## 5. How It Works

The project follows a clean, modular, three-phase architecture:

### 🔹 Phase 1 — Data Ingestion & Chunking (`ingestion/extract.py`)
AI models cannot ingest hundreds of pages at once efficiently. This ETL pipeline reads raw PDFs, strips out bad formatting, and splits the text into smaller, overlapping "chunks" of about 800 characters. The overlap ensures sentences aren't cut off abruptly, preserving context.

### 🔹 Phase 2 — Vectorization & Storage (`ingestion/build_index.py`)
Each chunk is passed to Google Gemini's Embedding model, which converts it into a high-dimensional vector representing its *meaning*. These vectors are saved locally into ChromaDB.

### 🔹 Phase 3 — Retrieval & Generation (`rag/query.py`)
When a user asks a question:
1. **Embed** — the question is converted into a vector
2. **Retrieve** — ChromaDB performs a nearest-neighbor search to find the 5 chunks closest in meaning to the question
3. **Generate** — the retrieved chunks are injected into a strict prompt template alongside the question; Gemini answers only from that context and cites the source page

### 🔹 Phase 4 — The Premium User Experience (`app/streamlit_app.py`)
Custom CSS replaces Streamlit's default boxy UI with a premium, mobile-responsive glassmorphism interface in a pink gradient theme (`#ec4899` → `#be185d`) — built mobile-first so it holds up on a phone, not just a laptop demo.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# add your Gemini API key to .env (get one at https://aistudio.google.com/apikey)
python ingestion/build_index.py
streamlit run app/streamlit_app.py
```

## Data

Two real, publicly available insurance documents are included in `data/`:

- **CMS Summary of Benefits and Coverage (SBC)** — a plain-language sample cost/coverage summary
- **Niva Bupa Health Assurance Policy Wording** — a full policy contract (definitions, benefits, critical illness list, exclusions, claims procedure)

---

<div align="center">
<sub>Built with 🩷 as a demonstration of practical Retrieval-Augmented Generation.</sub>
</div>