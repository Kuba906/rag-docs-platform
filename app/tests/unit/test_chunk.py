from ingest.chunk import chunk_text, count_tokens

def test_chunking_overlap():
    text = "Ala ma kota. " * 200
    chunks = chunk_text(text, max_tokens=50, overlap=10)
    assert len(chunks) > 1
    assert all(count_tokens(c) <= 50 for c in chunks)
