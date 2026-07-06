import json

from services.vectorstore_service import similarity_search
from services.bm25_service import bm25_search
from services.reranker_service import rerank
from services.llm_service import generate_answer
from services.llm_service import stream_answer

from services.message_service import (
    add_message,
    get_messages
)


def retrieve_context(
    question: str,
    documents: list = None,
    top_k: int = 5
):
    """
    Hybrid Retrieval Pipeline
    - Vector Search
    - BM25 Search
    - Cross Encoder Reranking

    Returns:
        context (str)
        sources (list)
    """

    # -----------------------------
    # Hybrid Retrieval
    # -----------------------------
    vector_results = similarity_search(
        question,
        documents=documents,
        k=10
    )

    bm25_results = bm25_search(
        question,
        documents_filter=documents,
        k=10
    )

    # -----------------------------
    # Merge results
    # -----------------------------
    combined = {}

    for doc in vector_results:
        combined[doc.page_content] = doc

    for doc in bm25_results:
        combined[doc.page_content] = doc

    results = list(combined.values())

    # -----------------------------
    # Cross Encoder Reranking
    # -----------------------------
    results = rerank(
        question,
        results,
        top_k=top_k
    )

    # -----------------------------
    # Build Context
    # -----------------------------
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

    return context, sources


def ask_question(
    db,
    chat_id: int,
    question: str,
    documents: list
):

    # -----------------------------
    # Save User Message
    # -----------------------------
    add_message(
        db,
        chat_id,
        "user",
        question
    )

    # -----------------------------
    # Retrieve Context
    # -----------------------------
    context, sources = retrieve_context(
        question,
        documents
    )

    # -----------------------------
    # Load Chat History
    # -----------------------------
    messages = get_messages(
        db,
        chat_id
    )

    history = [
        {
            "role": message.role,
            "content": message.content
        }
        for message in messages
    ]

    # -----------------------------
    # Generate Answer
    # -----------------------------
    answer = generate_answer(
        question=question,
        context=context,
        history=history
    )

    # -----------------------------
    # Save Assistant Message
    # -----------------------------
    add_message(
        db,
        chat_id,
        "assistant",
        answer
    )

    return {
        "answer": answer,
        "sources": sources
    }


def stream_question(
    db,
    chat_id: int,
    question: str,
    documents: list = None
):
    """
    Stream answer while using the exact same
    retrieval pipeline as ask_question().
    """

    # -----------------------------
    # Save User Message
    # -----------------------------
    add_message(
        db,
        chat_id,
        "user",
        question
    )

    # -----------------------------
    # Retrieve Context
    # -----------------------------
    context, sources = retrieve_context(
        question,
        documents
    )

    # -----------------------------
    # Load Chat History
    # -----------------------------
    messages = get_messages(
        db,
        chat_id
    )

    history = [
        {
            "role": message.role,
            "content": message.content
        }
        for message in messages
    ]

    # -----------------------------
    # Stream Response
    # -----------------------------
    full_answer = ""

    for token in stream_answer(
        question=question,
        context=context,
        history=history
    ):
        full_answer += token
        yield token

    # -----------------------------
    # Save Assistant Message
    # -----------------------------
    add_message(
        db,
        chat_id,
        "assistant",
        full_answer
    )

    # -----------------------------
    # Send Sources
    # -----------------------------
    yield "\n<END_SOURCES>\n"
    yield json.dumps(sources)