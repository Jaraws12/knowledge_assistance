from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def get_vectorstore():

    vectorstore_path = Path("vectorstore")

    if not vectorstore_path.exists():
        return None

    return FAISS.load_local(
        str(vectorstore_path),
        embedding_model,
        allow_dangerous_deserialization=True
    )


def similarity_search(
    query: str,
    documents: list[str] = None,
    k: int = 5
):

    db = get_vectorstore()

    if db is None:
        return []

    # Retrieve extra results because we'll filter afterwards
    results = db.similarity_search_with_score(
        query,
        k=25
    )

    docs = []

    for doc, score in results:

        filename = doc.metadata.get("filename")

        # If document filter is provided,
        # ignore documents that are not selected.
        if documents and filename not in documents:
            continue

        doc.metadata["vector_score"] = float(score)
        docs.append(doc)

        if len(docs) >= k:
            break

    return docs