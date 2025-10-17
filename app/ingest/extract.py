import io, pdfplumber
from bs4 import BeautifulSoup
import docx

def extract_text(data: bytes, filename: str) -> str:
    fn = filename.lower()
    if fn.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            return "\n".join((p.extract_text() or "") for p in pdf.pages)
    if fn.endswith(".docx"):
        d = docx.Document(io.BytesIO(data))
        return "\n".join(p.text for p in d.paragraphs)
    if fn.endswith(".html") or fn.endswith(".htm"):
        soup = BeautifulSoup(data, "lxml")
        return soup.get_text(" ")
    return data.decode("utf-8", errors="ignore")
