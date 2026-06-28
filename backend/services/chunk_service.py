from services.bm25_service import load_chunks


def get_chunk(filename: str, page: int, chunk: int):
    """
    Return the exact chunk that matches
    filename + page + chunk_id.
    """

    documents = load_chunks()

    for doc in documents:

        metadata = doc.metadata

        if (
            metadata.get("filename") == filename
            and metadata.get("page") == page
            and metadata.get("chunk_id") == chunk
        ):

            return {
                "filename": filename,
                "page": page,
                "chunk": chunk,
                "content": doc.page_content
            }

    return None