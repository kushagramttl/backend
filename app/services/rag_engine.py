# app/rag_engine.py
"""
Retrieval-Augmented Generation helper for the Stock-info backend.

• Loads all documents from ragdb.news at startup.
• Builds a FAISS index for dense-vector search.
• Exposes generate_rag_response(query) that returns an
  answer grounded in the retrieved context, with citation numbers.
"""

import os
from typing import List, Dict

import numpy as np
from qdrant_client import QdrantClient
from bson import ObjectId
from sentence_transformers import SentenceTransformer
from llama_cpp import llama_tokenize

from app.services.llama_engine import generate_response, llm

# ------------------------------------------------------------------
# Embedding model
# ------------------------------------------------------------------
embedder = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(host="qdrant", port=6333)


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------
def truncate_to_tokens(text: str, limit: int = 400) -> str:
    """
    Return the prefix of *text* that fits within *limit* tokens
    according to llama-cpp’s tokenizer.
    """
    # encode returns list[llama_token] with .byte_offset attr
    encoded = text.encode("utf-8")                       # bytes ✔
    tokens  = llm.tokenize(encoded, add_bos=False)       # list[int]

    if len(tokens) <= limit:
        return text

    truncated_tokens = tokens[:limit]
    truncated_bytes  = llm.detokenize(truncated_tokens)  # bytes → bytes
    return truncated_bytes.decode("utf-8", errors="ignore")

def _retrieve(query: str, k: int = 20) -> List[Dict[str, str]]:
    """Return top-k documents with text and url."""
    vector = embedder.encode(query).tolist()

    results = qdrant.search(
        collection_name="news",
        query_vector=vector,
        limit=k
    )

    return [
        {
            "text": r.payload["text"],
            "url": r.payload["url"]
        }
        for r in results
    ]

# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------
def generate_rag_response(query: str) -> str:
    """
    Return an LLM answer that references retrieved news articles
    with numbered citations [1], [2], …
    """
    print("The query received from controller is: ", query)
    passages = _retrieve(query, k=3)
    if not passages:
        return "I couldn't find relevant news articles in the database."

    context_blocks = []
    for i, p in enumerate(passages, start=1):
        snippet = truncate_to_tokens(p["text"], limit=800)
        context_blocks.append(f"[{i}] {p['url']}\n{snippet}\n")

    context = "\n".join(context_blocks)

    prompt = (
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        "Answer (based on the above articles]):"
    )

    print("🧠 PROMPT SENT TO LLM:\n", prompt[:1000], "\n---END---")

    return generate_response(prompt)
