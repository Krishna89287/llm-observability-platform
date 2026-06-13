from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from app.store import record, dashboard

app = FastAPI(title="LLM Observability Platform", version="1.0.0",
              description="Logs LLM call traces and exposes a dashboard of cost, latency, tokens and answer quality, plus Prometheus metrics.")

CALLS = Counter("llm_calls_total", "LLM calls", ["model"])
LAT = Histogram("llm_latency_ms", "LLM latency in ms")


class Trace(BaseModel):
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    faithfulness: Optional[float] = 0.0


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/trace")
def trace(t: Trace):
    rec = record(t.model_dump())
    CALLS.labels(t.model).inc()
    LAT.observe(t.latency_ms)
    return {"recorded": True, "cost_usd": rec["cost_usd"]}


@app.get("/dashboard")
def dash():
    return dashboard()


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
