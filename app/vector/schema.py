from pydantic import BaseModel

class DocChunk(BaseModel):
    id: str
    tenant_id: str
    file_id: str
    page: int | None = None
    section: str | None = None
    text: str
    vector: list[float] | None = None
    source: str | None = None
