"""Approximate per-1K-token prices (USD) for common models, used to estimate cost
from token counts. Update as provider pricing changes."""
PRICES = {
    "gpt-4o": {"in": 0.0025, "out": 0.01},
    "llama-3.3-70b": {"in": 0.0006, "out": 0.0008},
    "claude-sonnet": {"in": 0.003, "out": 0.015},
    "default": {"in": 0.001, "out": 0.002},
}


def cost(model, in_tok, out_tok):
    p = PRICES.get(model, PRICES["default"])
    return round((in_tok / 1000) * p["in"] + (out_tok / 1000) * p["out"], 6)
