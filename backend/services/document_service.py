from pathlib import Path

from services.bm25_service import (
    load_chunks,
    save_chunks,
    build_index
)

from services.ingestion_service import rebuild_vectorstore

from services.metadata_service import (
    get_indexed_files,
    save_metadata
)


def delete_document(filename: str):

    # -------------------------
    # Delete uploaded PDF
    # -------------------------

    pdf_path = Path("uploads") / filename

    if pdf_path.exists():
        pdf_path.unlink()

    # -------------------------
    # Remove chunks
    # -------------------------

    chunks = load_chunks()

    remaining_chunks = [
        chunk
        for chunk in chunks
        if chunk.metadata.get("filename") != filename
    ]

    save_chunks(remaining_chunks)

    # -------------------------
    # Rebuild BM25
    # -------------------------

    build_index()

    # -------------------------
    # Rebuild FAISS
    # -------------------------

    rebuild_vectorstore(remaining_chunks)

    # -------------------------
    # Update metadata
    # -------------------------

    files = get_indexed_files()

    files = [
        file
        for file in files
        if file["filename"] != filename
    ]

    save_metadata(files)

    return {
        "message": "Document deleted successfully.",
        "filename": filename
    }