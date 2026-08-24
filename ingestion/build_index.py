"""
build_index.py
Takes chunk records from extract.py, embeds them with Gemini's embedding
model, and stores them in a local persistent ChromaDB collection.

Run this once (or whenever data/ changes) to (re)build the vector index:
    python ingestion/build_index.py
"""

import os
import sys
from pathlib import Path

import chromadb
import google.generativeai as genai
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent))
from extract import process_all_documents

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"
COLLECTION_NAME = "insurance_policies"
EMBED_MODEL = "gemini-embedding-2-preview"
EMBED_BATCH_SIZE = 20


import time

def get_embeddings(texts: list[str]) -> list[list[float]]:
    """Call Gemini's embedding API for a batch of texts."""
    embeddings = []
    for i in range(0, len(texts), EMBED_BATCH_SIZE):
        batch = texts[i:i + EMBED_BATCH_SIZE]
        
        while True:
            try:
                result = genai.embed_content(
                model=EMBED_MODEL,
                content=batch,
            )
                break
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    print("  Rate limit hit, sleeping for 20 seconds...")
                    time.sleep(20)
                else:
                    raise e
                    
        embeddings.extend(result["embedding"])
        print(f"  embedded {min(i + EMBED_BATCH_SIZE, len(texts))}/{len(texts)}")
        time.sleep(2) # small delay to prevent rapid bursting
    return embeddings


def build_index():
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY not set. Create a .env file with:\n"
            "GEMINI_API_KEY=your_key_here"
        )

    genai.configure(api_key=GEMINI_API_KEY)

    print("Step 1: Extracting and chunking PDFs...")
    records = process_all_documents()
    if not records:
        print("No records to index. Add PDFs to data/ first.")
        return

    print("\nStep 2: Generating embeddings via Gemini...")
    texts = [r["text"] for r in records]
    embeddings = get_embeddings(texts)

    print("\nStep 3: Writing to ChromaDB...")
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Fresh collection each build to avoid stale/duplicate chunks
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(COLLECTION_NAME)

    collection.add(
        ids=[r["chunk_id"] for r in records],
        embeddings=embeddings,
        documents=texts,
        metadatas=[{"source": r["source"], "page": r["page"]} for r in records],
    )

    print(f"\nDone. Indexed {len(records)} chunks into '{COLLECTION_NAME}' at {CHROMA_DIR}")


if __name__ == "__main__":
    build_index()
