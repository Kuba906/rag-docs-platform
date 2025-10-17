from fastapi.testclient import TestClient
from app.main import app

def test_ask_minimal(monkeypatch):
    client = TestClient(app)
    import app.llm.embeddings as emb
    monkeypatch.setattr(emb, "embed_chunks", lambda x: [[0.0]*1536])
    import app.vector.qdrant_client as vc
    class H: 
        payload={"file_id":"x","page":1,"text":"foo bar"}; score=0.9
    monkeypatch.setattr(vc, "search", lambda v,t,top_k=4: [H()])
    import app.llm.chat as chat
    async def fake_answer(q, ctx):
        return "odp", [{"file_id":"x","page":1,"snippet":"foo"}], {"usd":0.0}
    monkeypatch.setattr(chat, "answer_with_context", fake_answer)
    r = client.post("/ask", json={"question":"Co to jest?"})
    assert r.status_code == 200
