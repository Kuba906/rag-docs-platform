from fastapi.testclient import TestClient
from app.main import app

def test_ingest_txt(tmp_path):
    client = TestClient(app)
    p = tmp_path/"x.txt"
    p.write_text("hello world "*100)
    with p.open("rb") as f:
        r = client.post("/ingest", files={"file": ("x.txt", f, "text/plain")})
    assert r.status_code == 200
    assert r.json()["chunks"] > 0
