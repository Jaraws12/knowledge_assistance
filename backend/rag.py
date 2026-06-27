from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# Load embedding model once
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS once
db = FAISS.load_local(
    "vectorstore",
    embedding_model,
    allow_dangerous_deserialization=True
)

# Load Gemini once
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)


def ask_question(question: str):

    results = db.similarity_search(
        question,
        k=3
    )

    context = ""

    sources = []
    seen = set()

    for doc in results:

        filename = doc.metadata.get("filename") or doc.metadata.get("source")
        page = doc.metadata.get("page", 0)
        chunk = doc.metadata.get("chunk_id")

        context += f"""
SOURCE
Document: {filename}
Page: {page}

CONTENT:
{doc.page_content}

-------------------------
"""

        # Avoid duplicate citations from the same page
        key = (filename, page)

        if key not in seen:

            seen.add(key)

            sources.append({
                "filename": filename,
                "page": page,
                "chunk": chunk,
                "excerpt": doc.page_content[:250] + "..."
                if len(doc.page_content) > 250
                else doc.page_content
            })

    prompt = f"""
You are a helpful assistant.

Answer ONLY from the provided context.

If the answer is not present in the context, reply exactly:

"I couldn't find that information in the uploaded documents."

Do not make up facts.
Do not mention page numbers.
Do not mention sources.

Context:

{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content.strip(),
        "sources": sources
    }

# Only for testing
if __name__ == "__main__":

    result = ask_question("What is Swaraj's CGPA?")

    print(result["answer"])

    print("\nSources:\n")

    for source in result["sources"]:
        print(source)