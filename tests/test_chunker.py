from app.engines.chunker import chunk_text

def test_chunk_text_empty():
    assert chunk_text("") == []
    assert chunk_text("  \n\t  ") == []

def test_chunk_text_short():
    sample = "short resume text."
    chunks = chunk_text(sample, chunk_size=500, chunk_overlap=50)

    assert len(chunks) == 1
    assert chunks[0] == sample

def test_chunk_text_overlap():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    chunks = chunk_text(alphabet, chunk_size=10, chunk_overlap=2)
    assert len(chunks) > 1
    assert chunks[0] == "ABCDEFGHIJ"
    assert chunks[1] == "IJKLMNOPQR"
    assert chunks[0][-2:] == chunks[1][:2]