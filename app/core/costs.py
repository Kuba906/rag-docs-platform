from dataclasses import dataclass

PRICES = {
    "text-embedding-3-large": {"input": 0.00002},
    "gpt-4o-mini": {"input": 0.000005, "output": 0.000015},
}

@dataclass
class Cost:
    input_tokens: int
    output_tokens: int
    usd: float

def estimate_cost(model: str, in_tok: int, out_tok: int = 0) -> Cost:
    p = PRICES.get(model, {"input": 0.0, "output": 0.0})
    usd = in_tok * p.get("input", 0) + out_tok * p.get("output", 0)
    return Cost(in_tok, out_tok, round(usd, 6))
