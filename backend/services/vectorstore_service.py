from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embedding_model = None


def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    return embedding_model


def get_vectorstore():

    vectorstore_path = Path("vectorstore")

    if not vectorstore_path.exists():
        return None

    embedding = get_embedding_model()

    return FAISS.load_local(
        str(vectorstore_path),
        embedding,
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

    results = db.similarity_search_with_score(
        query,
        k=25
    )

    docs = []

    for doc, score in results:

        filename = doc.metadata.get("filename")

        if documents and filename not in documents:
            continue

        doc.metadata["vector_score"] = float(score)
        docs.append(doc)

        if len(docs) >= k:
            break

    return docs