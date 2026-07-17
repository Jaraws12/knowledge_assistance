from sentence_transformers import CrossEncoder

reranker = None


def get_reranker():
    global reranker

    if reranker is None:
        reranker = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    return reranker


def rerank(query, documents, top_k=5):

    if not documents:
        return []

    model = get_reranker()

    pairs = [
        (query, doc.page_content)
        for doc in documents
    ]

    scores = model.predict(pairs)

    ranked = sorted(
        zip(scores, documents),
        key=lambda x: x[0],
        reverse=True
    )

    results = []

    for score, doc in ranked[:top_k]:
        doc.metadata["rerank_score"] = float(score)
        results.append(doc)

    return results