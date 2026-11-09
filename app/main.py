import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import evaluation

# Ensure model caches write to Vercel's ephemeral /tmp storage
os.environ["HF_HOME"] = tempfile.gettempdir()
os.environ["CHROMA_CACHE_DIR"] = tempfile.gettempdir()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

load_dotenv()

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

frontend_dir = Path(__file__).parent.parent / "frontend"

@app.get("/")
def read_root():
    index_path = frontend_dir / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"status": "active", "service": "TalentRank AI API", "docs": "/docs"}

if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "resume-rag-engine"}