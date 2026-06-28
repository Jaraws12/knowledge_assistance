from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

from services.retrieval_service import ask_question
from services.ingestion_service import ingest_pdf
from services.metadata_service import get_indexed_files
from services.bm25_service import build_index
from services.memory_service import clear_history
from fastapi.middleware.cors import CORSMiddleware
from services.chunk_service import get_chunk
from fastapi.staticfiles import StaticFiles

app = FastAPI()
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
    session_id: str
    question: str

class ClearChatRequest(BaseModel):
    session_id: str

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


@app.post("/ask")
async def ask(req: QuestionRequest):

    return ask_question(
        question=req.question,
        session_id=req.session_id
    )


@app.post("/clear-chat")
async def clear_chat(req: ClearChatRequest):

    clear_history(req.session_id)

    return {
        "message": "Chat history cleared.",
        "session_id": req.session_id
    }    

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