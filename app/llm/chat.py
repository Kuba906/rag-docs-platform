from typing import List
from openai import AsyncAzureOpenAI
from core.config import settings
from core.costs import estimate_cost

async def _client() -> AsyncAzureOpenAI:
    return AsyncAzureOpenAI(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_key=settings.AZURE_OPENAI_API_KEY,
        api_version="2024-07-01-preview",
    )

async def answer_with_context(question: str, ctx: List[dict]) -> tuple[str, list[dict], dict]:
    context_text = "\n\n".join(f"[{c['file_id']} p.{c.get('page', '?')}] {c['text']}" for c in ctx)
    cli = await _client()
    msgs = [
        {"role": "system", "content": "Odpowiadaj tylko na podstawie kontekstu. Cytuj źródła."},
        {"role": "user", "content": f"Kontekst:\n{context_text}\n---\nPytanie: {question}"},
    ]
    res = await cli.chat.completions.create(model=settings.AZURE_OPENAI_DEPLOYMENT_CHAT, messages=msgs, temperature=0.2)
    txt = res.choices[0].message.content
    usage = res.usage or None
    cost = {"usd": 0}
    if usage:
        c = estimate_cost(settings.AZURE_OPENAI_DEPLOYMENT_CHAT, usage.prompt_tokens, usage.completion_tokens)
        cost = c.__dict__
    cites = [{"file_id": c["file_id"], "page": c.get("page"), "snippet": c["text"][:160]} for c in ctx]
    return txt, cites, cost
