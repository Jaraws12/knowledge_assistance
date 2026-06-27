from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)


def generate_answer(
    question: str,
    context: str,
    history: list
):
    """
    Generates an answer using:
    1. Conversation history
    2. Retrieved document context
    """

    # ----------------------------
    # Convert history into text
    # ----------------------------

    conversation = ""

    for message in history:

        role = message["role"].capitalize()

        conversation += (
            f"{role}: {message['content']}\n"
        )

    # ----------------------------
    # Prompt
    # ----------------------------

    prompt = f"""
You are a helpful AI assistant.

Your job is to answer ONLY using the retrieved context.

If the answer is not available in the context, reply exactly:

"I couldn't find that information in the uploaded documents."

--------------------------------------------------
Previous Conversation

{conversation}

--------------------------------------------------
Retrieved Context

{context}

--------------------------------------------------
Current Question

{question}

--------------------------------------------------

Rules:

1. Use the previous conversation to resolve references like:
   - he
   - she
   - it
   - they
   - this project
   - that document
   - those skills

2. Answer ONLY from the retrieved context.

3. Never hallucinate.

4. If context is insufficient, say you couldn't find it.

5. Do NOT mention page numbers.

6. Do NOT mention document names.

7. Keep the answer concise and natural.
"""

    response = llm.invoke(prompt)

    return response.content.strip()