from fastapi import FastAPI

app = FastAPI(
    title="AI Knowledge System",
    description="RAG-based document Q&A",
    version="0.1.0"
)

@app.get("/")
def health_check():
    return {"status": "running", "message": "AI Knowledge System is live"}