import os
import tempfile
import chromadb
from chromadb.utils import embedding_functions

# Force ONNX model and Chroma cache to Vercel's writable /tmp directory
os.environ["CHROMA_CACHE_DIR"] = tempfile.gettempdir()
os.environ["ONNXRUNTIME_CACHE_DIR"] = tempfile.gettempdir()

# Native ONNX embedding function (no PyTorch or sentence-transformers required)
default_ef = embedding_functions.DefaultEmbeddingFunction()

class VectorStoreManager:
    def __init__(self, collection_name: str = "resumes"):
        # EphemeralClient operates in-memory to prevent read-only filesystem errors
        self.client = chromadb.EphemeralClient()
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=default_ef
        )

    def add_resume_chunks(self, chunks: list[str], metadatas: list[dict], ids: list[str]) -> None:
        if not chunks:
            return

        # ChromaDB generates embeddings automatically using embedding_function
        self.collection.add(
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )

    def search_similar_chunks(self, query_text: str, n_results: int = 5, where: dict | None = None) -> dict:
        query_kwargs = {
            "query_texts": [query_text],
            "n_results": n_results
        }
        if where:
            query_kwargs["where"] = where

        results = self.collection.query(**query_kwargs)
        return results