"""
query.py
Given a user question, retrieves the most relevant policy chunks from
ChromaDB and asks Gemini to answer grounded strictly in that context.
"""

import os
from pathlib import Path

import chromadb
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"
COLLECTION_NAME = "insurance_policies"
EMBED_MODEL = "models/gemini-embedding-2"
CHAT_MODEL = "gemini-3.5-flash"
TOP_K = 5

SYSTEM_PROMPT = """You are an assistant that answers questions about health insurance \
policy documents. Answer ONLY using the provided context excerpts below. \
If the answer isn't in the context, say clearly that the documents don't cover it \
— do not guess or use outside knowledge. \
When you answer, mention which document(s) and page(s) the information came from. \
Keep answers concise and in plain language a policyholder would understand."""


def _get_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_collection(COLLECTION_NAME)


def retrieve(question: str, top_k: int = TOP_K):
    """Embed the question and fetch the top_k most relevant chunks."""
    genai.configure(api_key=GEMINI_API_KEY)

    query_embedding = genai.embed_content(
        model=EMBED_MODEL,
        content=question,
        task_type="retrieval_query",
    )["embedding"]

    collection = _get_collection()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text": doc,
            "source": meta["source"],
            "page": meta["page"],
            "distance": dist,
        })
    return chunks


def build_context(chunks):
    """Format retrieved chunks into a labeled context block for the prompt."""
    parts = []
    for c in chunks:
        parts.append(f"[{c['source']}, page {c['page']}]\n{c['text']}")
    return "\n\n---\n\n".join(parts)


def answer_question(question: str, top_k: int = TOP_K):
    """Full RAG pipeline: retrieve -> build context -> generate grounded answer."""
    chunks = retrieve(question, top_k=top_k)

    if not chunks:
        return {
            "answer": "No indexed documents found. Run ingestion/build_index.py first.",
            "sources": [],
        }

    context = build_context(chunks)
    model = genai.GenerativeModel(CHAT_MODEL, system_instruction=SYSTEM_PROMPT)

    prompt = f"""Context excerpts from policy documents:

{context}

---

Question: {question}

Answer based only on the context above."""

    response = model.generate_content(prompt)

    return {
        "answer": response.text,
        "sources": [{"source": c["source"], "page": c["page"]} for c in chunks],
    }


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "What is the deductible for this plan?"
    result = answer_question(q)
    print("\nQ:", q)
    print("\nA:", result["answer"])
    print("\nSources:")
    for s in result["sources"]:
        print(f"  - {s['source']} (page {s['page']})")
