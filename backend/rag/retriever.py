import os
from sqlalchemy.orm import Session
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from db.models import Chunk

EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2"
TOP_K = 5
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def retrieve_and_answer(question: str, document_id: int, db: Session) -> str:
    embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_HOST)
    question_vector = embeddings.embed_query(question)

    chunks = (
        db.query(Chunk)
        .filter(Chunk.document_id == document_id)
        .order_by(Chunk.embedding.cosine_distance(question_vector))
        .limit(TOP_K)
        .all()
    )

    if not chunks:
        return "No relevant content found for this document."

    context = "\n\n".join(chunk.content for chunk in chunks)

    llm = OllamaLLM(model=LLM_MODEL, base_url=OLLAMA_HOST)
    prompt = f"""Answer the question using only the context below. If the answer isn't in the context, say so.

Context:
{context}

Question: {question}

Answer:"""

    return llm.invoke(prompt)
