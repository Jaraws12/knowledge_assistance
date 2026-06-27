from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from metadata_manager import add_indexed_file

# Load embedding model only once
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def ingest_document(pdf_path: str):
    """Load a PDF and convert it into chunks."""

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    filename = Path(pdf_path).name

    for idx, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = idx
        chunk.metadata["source"] = filename
        chunk.metadata["filename"] = filename
        chunk.metadata["page"] = chunk.metadata.get("page", 0) + 1

    return chunks


def update_vectorstore(chunks):
    """Create a new FAISS index or append to an existing one."""

    vectorstore_path = "vectorstore"

    if Path(vectorstore_path).exists():

        db = FAISS.load_local(
            vectorstore_path,
            embedding_model,
            allow_dangerous_deserialization=True
        )

        db.add_documents(chunks)

    else:

        db = FAISS.from_documents(
            chunks,
            embedding_model
        )

    db.save_local(vectorstore_path)


def ingest_pdf(pdf_path: str):

    filename = Path(pdf_path).name

    chunks = ingest_document(pdf_path)

    update_vectorstore(chunks)

    add_indexed_file(
        filename,
        len(chunks)
    )

    return len(chunks)