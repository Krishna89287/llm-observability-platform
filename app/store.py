"""In-memory trace store. In production this would be a database or an OTel
backend; here it keeps the last traces so the dashboard works out of the box."""
from collections import deque
from statistics import mean
from app.pricing import cost

TRACES = deque(maxlen=5000)


def record(t):
    t["cost_usd"] = cost(t["model"], t["input_tokens"], t["output_tokens"])
    TRACES.append(t)
    return t


def dashboard():
    if not TRACES:
        return {"calls": 0}
    lat = [t["latency_ms"] for t in TRACES]
    lat_sorted = sorted(lat)
    p = lambda q: lat_sorted[min(len(lat_sorted) - 1, int(q * len(lat_sorted)))]
    return {
        "calls": len(TRACES),
        "total_cost_usd": round(sum(t["cost_usd"] for t in TRACES), 4),
        "avg_latency_ms": round(mean(lat), 1),
        "p95_latency_ms": p(0.95),
        "total_tokens": sum(t["input_tokens"] + t["output_tokens"] for t in TRACES),
        "avg_faithfulness": round(mean([t.get("faithfulness", 0) for t in TRACES]), 3),
        "by_model": _by_model(),
    }


def _by_model():
    out = {}
    for t in TRACES:
        m = out.setdefault(t["model"], {"calls": 0, "cost_usd": 0.0})
        m["calls"] += 1
        m["cost_usd"] = round(m["cost_usd"] + t["cost_usd"], 4)
    return out
