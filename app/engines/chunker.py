def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    cleaned_text = text.strip()
    if not cleaned_text:
        return []
    
    if len(cleaned_text) <= chunk_size:
        return [cleaned_text]

    chunks = []
    step = chunk_size - chunk_overlap

    for start in range(0,len(cleaned_text),step):
        chunk = cleaned_text[start : start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
    return chunks