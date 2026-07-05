from services.llm_service import stream_answer

context = """
Python is a programming language.
"""

question = "What is Python?"

for token in stream_answer(question, context):
    print(token, end="", flush=True)