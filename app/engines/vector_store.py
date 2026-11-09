import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

class VectorStoreManager:
    def __init__(self, persist_directory: str = "storage/chroma", collection_name: str = "resumes"):
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.client = chromadb.PersistentClient(path = persist_directory)
        self.collection = self.client.get_or_create_collection(name = collection_name)
       

    def add_resume_chunks(self, chunks: list[str], metadatas: list[dict], ids: list[str]) -> None:
        if not chunks:
            return
        
        doc_embeddings = self.model.encode(chunks).tolist()

        self.collection.add(
            embeddings = doc_embeddings,
            documents = chunks,
            metadatas = metadatas,
            ids = ids
        )
        

    def search_similar_chunks(self, query_text: str, n_results: int = 5, where: dict | None = None) -> dict:
        query_kwargs = {
            "query_texts":[query_text],
            "n_results" : n_results
        }
        if where:
            query_kwargs["where"] = where

        results = self.collection.query(**query_kwargs)
        return results
        