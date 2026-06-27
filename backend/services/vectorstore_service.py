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


def similarity_search(query: str, k: int = 5):

    db = get_vectorstore()

    if db is None:
        return []

    results = db.similarity_search_with_score(
    query,
    k=k
)
    docs = []
    for doc, score in results:
        doc.metadata["vector_score"] = float(score)
        docs.append(doc)
    return docs    
    