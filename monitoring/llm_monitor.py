"""
LLM Observability Monitor
Real-time monitoring for LLM applications in production
"""
import time
import uuid
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class LLMTrace:
    trace_id: str
    model: str
    prompt: str
    response: str
    latency_ms: float
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    timestamp: float
    metadata: Dict = field(default_factory=dict)
    quality_score: Optional[float] = None
    hallucination_detected: bool = False


class CostCalculator:
    """Calculate LLM API costs for different providers and models."""

    PRICING = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "claude-3-opus": {"input": 0.015, "output": 0.075},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},
        "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
    }

    def calculate_cost(self, model: str, prompt_tokens: int,
                       completion_tokens: int) -> float:
        pricing = self.PRICING.get(model, {"input": 0.001, "output": 0.002})
        cost = (prompt_tokens / 1000 * pricing["input"] +
                completion_tokens / 1000 * pricing["output"])
        return round(cost, 6)


class LLMMonitor:
    """
    Production LLM monitoring system.
    Tracks every LLM call with full observability.
    """

    def __init__(self):
        self.traces: List[LLMTrace] = []
        self.cost_calculator = CostCalculator()
        self.alerts: List[Dict] = []
        self.thresholds = {
            "max_latency_ms": 5000,
            "max_cost_per_call": 0.10,
            "min_quality_score": 0.7,
            "hallucination_rate_threshold": 0.05
        }
        logger.info("LLMMonitor initialized")

    def record_call(self, model: str, prompt: str, response: str,
                    latency_ms: float, prompt_tokens: int,
                    completion_tokens: int, metadata: Dict = None) -> LLMTrace:
        cost = self.cost_calculator.calculate_cost(model, prompt_tokens, completion_tokens)

        trace = LLMTrace(
            trace_id=str(uuid.uuid4()),
            model=model,
            prompt=prompt[:500],
            response=response[:500],
            latency_ms=latency_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost_usd=cost,
            timestamp=time.time(),
            metadata=metadata or {}
        )

        self.traces.append(trace)
        self._check_alerts(trace)
        return trace

    def _check_alerts(self, trace: LLMTrace) -> None:
        if trace.latency_ms > self.thresholds["max_latency_ms"]:
            self._create_alert("HIGH_LATENCY", f"Latency {trace.latency_ms}ms exceeds threshold", trace)
        if trace.cost_usd > self.thresholds["max_cost_per_call"]:
            self._create_alert("HIGH_COST", f"Cost ${trace.cost_usd} exceeds threshold", trace)

    def _create_alert(self, alert_type: str, message: str, trace: LLMTrace) -> None:
        alert = {"type": alert_type, "message": message,
                 "trace_id": trace.trace_id, "timestamp": time.time()}
        self.alerts.append(alert)
        logger.warning(f"ALERT [{alert_type}]: {message}")

    def get_dashboard_metrics(self) -> Dict:
        if not self.traces:
            return {"error": "No traces recorded yet"}

        recent = [t for t in self.traces if time.time() - t.timestamp < 3600]
        total_cost = sum(t.cost_usd for t in self.traces)
        avg_latency = sum(t.latency_ms for t in self.traces) / len(self.traces)
        total_tokens = sum(t.prompt_tokens + t.completion_tokens for t in self.traces)

        model_stats = defaultdict(lambda: {"calls": 0, "cost": 0.0, "avg_latency": 0.0})
        for trace in self.traces:
            model_stats[trace.model]["calls"] += 1
            model_stats[trace.model]["cost"] += trace.cost_usd

        return {
            "total_calls": len(self.traces),
            "recent_calls_1h": len(recent),
            "total_cost_usd": round(total_cost, 4),
            "avg_latency_ms": round(avg_latency, 1),
            "total_tokens": total_tokens,
            "active_alerts": len(self.alerts),
            "model_breakdown": dict(model_stats),
            "p99_latency_ms": sorted([t.latency_ms for t in self.traces])[int(len(self.traces) * 0.99)] if len(self.traces) > 10 else avg_latency
        }


if __name__ == "__main__":
    monitor = LLMMonitor()

    for i in range(5):
        trace = monitor.record_call(
            model="gpt-4",
            prompt=f"Question {i}: What is LangGraph?",
            response=f"LangGraph is an enterprise framework for stateful agent workflows.",
            latency_ms=1200 + i * 100,
            prompt_tokens=50,
            completion_tokens=30
        )

    metrics = monitor.get_dashboard_metrics()
    print(json.dumps(metrics, indent=2))
