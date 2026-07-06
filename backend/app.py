import database
from typing import List

from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from services.retrieval_service import (
    ask_question,
    stream_question
)
from services.chat_service import (
    create_chat,
    get_all_chats,
    get_chat,
    delete_chat,
    rename_chat
)
from services.message_service import get_messages
from services.ingestion_service import ingest_pdf
from services.metadata_service import get_indexed_files
from services.bm25_service import build_index

from fastapi.middleware.cors import CORSMiddleware
from services.chunk_service import get_chunk
from fastapi.staticfiles import StaticFiles
from services.document_service import delete_document
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from models.chat import Chat
from models.message import Message


app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build BM25 index when the server starts
@app.on_event("startup")
async def startup_event():
    build_index()
    print("✅ BM25 Index Loaded")



class QuestionRequest(BaseModel):
    chat_id: int
    question: str
    documents: List[str] = []



@app.get("/")
def home():
    return {
        "message": "Knowledge Assistant API is running 🚀"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile):

    # ingestion_service already handles:
    # - saving the file
    # - duplicate checking
    # - FAISS update
    # - BM25 update
    # - metadata update
    return await ingest_pdf(file)


@app.get("/documents")
def list_documents():
    return {
        "documents": get_indexed_files()
    }


@app.delete("/documents/{filename}")
async def delete_file(filename: str):

    return delete_document(filename)

@app.post("/ask")
async def ask(
    req: QuestionRequest,
    db: Session = Depends(get_db)
):

    return ask_question(
        db=db,
        chat_id=req.chat_id,
        question=req.question,
        documents=req.documents
    )


@app.post("/ask-stream")
async def ask_stream(
    req: QuestionRequest,
    db: Session = Depends(get_db)
):

    return StreamingResponse(
        stream_question(
            db=db,
            chat_id=req.chat_id,
            question=req.question,
            documents=req.documents
        ),
        media_type="text/plain"
    )



@app.get("/chunk")
def read_chunk(
    filename: str,
    page: int,
    chunk: int
):

    result = get_chunk(
        filename,
        page,
        chunk
    )

    if result is None:
        return {
            "error": "Chunk not found"
        }

    return result    


class RenameChatRequest(BaseModel):
    title: str



@app.post("/chats")
def new_chat(
    db: Session = Depends(get_db)
):

    chat = create_chat(db)

    return {
        "id": chat.id,
        "title": chat.title,
        "created_at": chat.created_at
    }    



@app.get("/chats")
def list_chats(
    db: Session = Depends(get_db)
):

    chats = get_all_chats(db)

    return [
        {
            "id": chat.id,
            "title": chat.title,
            "created_at": chat.created_at
        }
        for chat in chats
    ]   
    
    
@app.get("/chats/{chat_id}")
def load_chat(
    chat_id: int,
    db: Session = Depends(get_db)
):

    chat = get_chat(db, chat_id)

    if chat is None:
        return {
            "error": "Chat not found"
        }

    return {
        "id": chat.id,
        "title": chat.title,
        "created_at": chat.created_at
    }


@app.patch("/chats/{chat_id}")
def update_chat(
    chat_id: int,
    req: RenameChatRequest,
    db: Session = Depends(get_db)
):

    chat = rename_chat(
        db,
        chat_id,
        req.title
    )

    if chat is None:
        return {
            "error": "Chat not found"
        }

    return {
        "message": "Chat renamed.",
        "chat": {
            "id": chat.id,
            "title": chat.title
        }
    }    



@app.delete("/chats/{chat_id}")
def remove_chat(
    chat_id: int,
    db: Session = Depends(get_db)
):

    chat = delete_chat(
        db,
        chat_id
    )

    if chat is None:
        return {
            "error": "Chat not found"
        }

    return {
        "message": "Chat deleted."
    }    



@app.get("/chats/{chat_id}/messages")
def load_messages(
    chat_id: int,
    db: Session = Depends(get_db)
):

    messages = get_messages(
        db,
        chat_id
    )

    return [
        {
            "id": message.id,
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at
        }
        for message in messages
    ]    