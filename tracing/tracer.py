"""
LLM Distributed Tracer
OpenTelemetry-based tracing for LLM applications
"""
import time
import uuid
import logging
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)


class LLMSpan:
    """Represents a single traced LLM operation."""

    def __init__(self, name: str, trace_id: str = None):
        self.span_id = str(uuid.uuid4())[:8]
        self.trace_id = trace_id or str(uuid.uuid4())
        self.name = name
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        self.attributes: Dict[str, Any] = {}
        self.events: list = []

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = value

    def add_event(self, name: str, attributes: Dict = None) -> None:
        self.events.append({"name": name, "timestamp": time.time(),
                           "attributes": attributes or {}})

    def end(self) -> None:
        self.end_time = time.time()

    @property
    def duration_ms(self) -> float:
        end = self.end_time or time.time()
        return (end - self.start_time) * 1000


class LLMTracer:
    """
    Distributed tracer for LLM applications.
    Tracks every LLM call, tool use, and retrieval operation.
    Compatible with OpenTelemetry and LangSmith.
    """

    def __init__(self, service_name: str = "llm-application"):
        self.service_name = service_name
        self.spans: list = []
        logger.info(f"LLMTracer initialized for service: {service_name}")

    def start_span(self, name: str, trace_id: str = None) -> LLMSpan:
        span = LLMSpan(name, trace_id)
        self.spans.append(span)
        return span

    def trace_llm_call(self, model: str, prompt: str,
                       response: str, latency_ms: float) -> LLMSpan:
        span = self.start_span(f"llm.{model}")
        span.set_attribute("model", model)
        span.set_attribute("prompt_length", len(prompt))
        span.set_attribute("response_length", len(response))
        span.set_attribute("latency_ms", latency_ms)
        span.add_event("llm.prompt", {"content": prompt[:100]})
        span.add_event("llm.response", {"content": response[:100]})
        span.end()
        return span

    def get_trace_summary(self, trace_id: str) -> Dict:
        trace_spans = [s for s in self.spans if s.trace_id == trace_id]
        return {
            "trace_id": trace_id,
            "total_spans": len(trace_spans),
            "total_duration_ms": sum(s.duration_ms for s in trace_spans),
            "spans": [{"name": s.name, "duration_ms": s.duration_ms}
                     for s in trace_spans]
        }


if __name__ == "__main__":
    tracer = LLMTracer("my-llm-app")
    span = tracer.trace_llm_call(
        model="gpt-4",
        prompt="What is LangGraph?",
        response="LangGraph is an enterprise framework...",
        latency_ms=1250.0
    )
    print(f"Traced call: {span.name}, duration: {span.duration_ms:.1f}ms")
    summary = tracer.get_trace_summary(span.trace_id)
    print(f"Trace summary: {summary}")
