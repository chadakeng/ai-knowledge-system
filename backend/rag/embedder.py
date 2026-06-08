import os
from langchain_ollama import OllamaEmbeddings

EMBED_MODEL = "nomic-embed-text"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def embed_chunks(chunks: list[str]) -> list[list[float]]:
    embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_HOST)
    return embeddings.embed_documents(chunks)
