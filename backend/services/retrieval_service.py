from services.vectorstore_service import similarity_search
from services.bm25_service import bm25_search
from services.reranker_service import rerank
from services.llm_service import generate_answer
from services.memory_service import (
    add_message,
    get_history,
    clear_history
)


def ask_question(
    question: str,
    session_id: str
):

    # Retrieve more candidates
    add_message(session_id, "user", question)
    vector_results = similarity_search(question, k=10)
    bm25_results = bm25_search(question, k=10)

    # Merge results and remove duplicates
    combined = {}

    for doc in vector_results:
        combined[doc.page_content] = doc

    for doc in bm25_results:
        combined[doc.page_content] = doc

    results = list(combined.values())

    # -----------------------------
    # Cross-Encoder Reranking
    # -----------------------------
    results = rerank(
        question,
        results,
        top_k=5
    )

    context = ""
    sources = []
    seen = set()

    for doc in results:

        filename = doc.metadata.get("filename")
        page = doc.metadata.get("page")
        chunk = doc.metadata.get("chunk_id")

        context += f"""
SOURCE:
Document: {filename}
Page: {page}

CONTENT:
{doc.page_content}

------------------
"""

        key = (filename, page)

        if key not in seen:

            seen.add(key)

            sources.append({

    "filename": filename,

    "page": page,

    "chunk": chunk,

    "vector_score": doc.metadata.get("vector_score"),

    "bm25_score": doc.metadata.get("bm25_score"),

    "rerank_score": doc.metadata.get("rerank_score"),

    "excerpt": (
        doc.page_content[:350]
        if len(doc.page_content) > 350
        else doc.page_content
    )
})

    history = get_history(session_id)
    
    answer = generate_answer(question=question, context=context, history=history)
    add_message(
        session_id,
        "assistant",
        answer
    )

    return {
        "answer": answer,
        "sources": sources
    }