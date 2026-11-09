import pytest 
from app.engines.vector_store import VectorStoreManager

def test_vector_store_add_and_search(tmp_path):
    test_db_dir = str(tmp_path/"test-chroma")

    manager = VectorStoreManager(
        persist_directory=test_db_dir,
        collection_name="test-resumes"
    )
    chunks = [
        "Senior Python Engineer specializing in FastAPI and PostgreSQL.",
        "UI Designer proficient in Figma, CSS, and HTML.",
    ]
    metadatas = [
        {"candidate_name": "Alice", "chunk_index": 0},
        {"candidate_name": "Charlie", "chunk_index": 0},
    ]
    ids = ["c1_chunk0","c2_chunk0"]

    manager.add_resume_chunks(chunks=chunks, metadatas=metadatas, ids=ids)

    results = manager.search_similar_chunks(
        query_text="Looking for a Python FastAPI developer",
        n_results= 1
    )

    top_doc = results["documents"][0][0]
    top_metadata = results["candidate_name"][0][0]

    assert "FastAPI" in top_doc
    assert top_metadata["candidate_name"] == "Alice"