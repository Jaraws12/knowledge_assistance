from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import shutil
from fastapi import UploadFile

from services.metadata_service import (
    add_indexed_file,
    is_already_indexed
)
from services.bm25_service import (
    load_chunks,
    save_chunks,
    build_index
)

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


async def ingest_pdf(file: UploadFile):

    # Check duplicate
    if is_already_indexed(file.filename):
        return {
            "message": "Document already indexed.",
            "filename": file.filename
        }

    # Save uploaded file
    upload_path = f"uploads/{file.filename}"

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Chunk document
    chunks = ingest_document(upload_path)

    # Update FAISS
    update_vectorstore(chunks)

    # Update BM25
    existing_chunks = load_chunks()

    existing_chunks.extend(chunks)

    save_chunks(existing_chunks)

    build_index()

    # Update metadata
    add_indexed_file(
        file.filename,
        len(chunks)
    )

    return {
        "message": "Document indexed successfully.",
        "filename": file.filename,
        "chunks": len(chunks)
    }