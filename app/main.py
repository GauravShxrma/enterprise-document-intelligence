import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import evaluation

load_dotenv()
# Suppress HuggingFace tokenizer parallelism warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

app = FastAPI(
    title="Enterprise Document Intelligence & Resume RAG Engine",
    version="1.0.0"
)

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API endpoints
app.include_router(evaluation.router, prefix="/api/v1", tags=["Evaluation"])

# Mount static frontend directory (serves index.html, css/, js/)
frontend_dir = Path(__file__).parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "resume-rag-engine"}