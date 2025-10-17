from typing import List
import tiktoken

_enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(_enc.encode(text))

def chunk_text(text: str, max_tokens: int = 900, overlap: int = 150) -> List[str]:
    tokens = _enc.encode(text)
    chunks, i = [], 0
    step = max_tokens - overlap
    while i < len(tokens):
        chunk = tokens[i:i+max_tokens]
        chunks.append(_enc.decode(chunk))
        i += step
    return chunks
