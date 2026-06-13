from fastapi.testclient import TestClient
from app.main import app
c = TestClient(app)


def test_health():
    assert c.get("/health").status_code == 200


def test_trace_and_dashboard():
    c.post("/trace", json={"model": "gpt-4o", "input_tokens": 500, "output_tokens": 200, "latency_ms": 800, "faithfulness": 0.9})
    c.post("/trace", json={"model": "llama-3.3-70b", "input_tokens": 400, "output_tokens": 150, "latency_ms": 300, "faithfulness": 0.8})
    d = c.get("/dashboard").json()
    assert d["calls"] >= 2
    assert d["total_cost_usd"] > 0
    assert "gpt-4o" in d["by_model"]
