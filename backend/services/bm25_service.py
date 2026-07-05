import os
import pickle

from rank_bm25 import BM25Okapi

CHUNK_FILE = "metadata/chunks.pkl"

bm25 = None
documents = []


def load_chunks():

    if not os.path.exists(CHUNK_FILE):
        return []

    if os.path.getsize(CHUNK_FILE) == 0:
        return []

    try:
        with open(CHUNK_FILE, "rb") as f:
            return pickle.load(f)
    except (EOFError, pickle.UnpicklingError):
        return []


def save_chunks(chunks):

    with open(CHUNK_FILE, "wb") as f:
        pickle.dump(chunks, f)


def build_index():

    global bm25
    global documents

    documents = load_chunks()

    if len(documents) == 0:
        bm25 = None
        return

    corpus = [
        doc.page_content.split()
        for doc in documents
    ]

    bm25 = BM25Okapi(corpus)


def bm25_search(
    query: str,
    documents_filter: list[str] = None,
    k: int = 5
):
    """
    Search documents using BM25.
    Optionally restrict the search to selected documents.
    """

    global bm25
    global documents

    if bm25 is None:
        return []

    query_tokens = query.split()

    scores = bm25.get_scores(query_tokens)

    ranked = sorted(
        zip(scores, documents),
        key=lambda x: x[0],
        reverse=True
    )

    results = []

    for score, doc in ranked:

        filename = doc.metadata.get("filename")

        # Skip documents that are not selected
        if documents_filter and filename not in documents_filter:
            continue

        doc.metadata["bm25_score"] = float(score)

        results.append(doc)

        if len(results) >= k:
            break

    return results