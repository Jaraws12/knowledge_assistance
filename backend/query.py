from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vectorstore",
    embedding_model,
    allow_dangerous_deserialization=True
)
query="what is this document about?"

results = db.similarity_search(
    query,
    k=3
)

for doc in results:
    print("=" * 50)
    print(doc.metadata)
    print(doc.page_content[:500])