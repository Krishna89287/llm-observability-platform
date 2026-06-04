# LLM Observability Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://python.org)
[![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-1.24-blue?style=flat-square)](https://opentelemetry.io)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/Krishna89287/llm-observability-platform/ci.yml?style=flat-square)](https://github.com/Krishna89287/llm-observability-platform/actions)

Production observability for LLM applications. Tracks latency, cost, quality, and hallucinations in real time — before your users notice.

## The Problem

Most teams ship AI without monitoring. When something goes wrong:
- A model starts hallucinating on certain queries
- Costs spike 10x due to a prompt change
- Latency degrades after a provider update

You find out from users. This platform catches it first.

## Features

- **Cost tracking** — per-request cost across GPT-4, Claude, Gemini with real pricing
- **Latency monitoring** — p50, p95, p99 histograms per model
- **Quality scoring** — automated coherence, completeness, safety scoring
- **Distributed tracing** — trace every LLM call, tool use, and retrieval hop
- **Alerting** — automatic alerts for high latency, high cost, quality drops
- **Prometheus metrics** — standard metrics for Grafana dashboards

## Quick Start

```bash
git clone https://github.com/Krishna89287/llm-observability-platform.git
cd llm-observability-platform
pip install -r requirements.txt
cp .env.example .env
python monitoring/llm_monitor.py
```

## Usage

### Monitor LLM Calls

```python
from monitoring.llm_monitor import LLMMonitor

monitor = LLMMonitor()

# Record every LLM call
trace = monitor.record_call(
    model="gpt-4",
    prompt="Explain Kubernetes networking",
    response="Kubernetes networking uses...",
    latency_ms=1250,
    prompt_tokens=15,
    completion_tokens=120
)

print(f"Trace ID: {trace.trace_id}")
print(f"Cost: ${trace.cost_usd:.6f}")
```

### Get Dashboard Metrics

```python
metrics = monitor.get_dashboard_metrics()

print(f"Total calls: {metrics['total_calls']}")
print(f"Total cost: ${metrics['total_cost_usd']}")
print(f"Avg latency: {metrics['avg_latency_ms']:.1f}ms")
print(f"P99 latency: {metrics['p99_latency_ms']:.1f}ms")
print(f"Active alerts: {metrics['active_alerts']}")
print(f"Model breakdown: {metrics['model_breakdown']}")
```

### Calculate Costs

```python
from monitoring.llm_monitor import CostCalculator

calc = CostCalculator()

gpt4_cost = calc.calculate_cost("gpt-4", prompt_tokens=1000, completion_tokens=500)
claude_cost = calc.calculate_cost("claude-3-sonnet", prompt_tokens=1000, completion_tokens=500)
haiku_cost = calc.calculate_cost("claude-3-haiku", prompt_tokens=1000, completion_tokens=500)

print(f"GPT-4: ${gpt4_cost:.4f}")
print(f"Claude Sonnet: ${claude_cost:.4f}")
print(f"Claude Haiku: ${haiku_cost:.4f}")
```

### Trace Distributed LLM Workflows

```python
from tracing.tracer import LLMTracer

tracer = LLMTracer(service_name="my-rag-app")

# Trace a full RAG workflow
retrieval_span = tracer.start_span("retrieval")
retrieval_span.set_attribute("query", "user question")
retrieval_span.set_attribute("num_docs", 5)
retrieval_span.end()

llm_span = tracer.trace_llm_call(
    model="gpt-4",
    prompt="Context: ... Question: ...",
    response="Based on the context...",
    latency_ms=1800
)

summary = tracer.get_trace_summary(llm_span.trace_id)
print(f"Total duration: {summary['total_duration_ms']:.1f}ms")
```

### Score Response Quality

```python
from evaluation.quality_scorer import QualityScorer

scorer = QualityScorer()

result = scorer.score_response(
    question="What is vLLM and why is it fast?",
    response="vLLM uses PagedAttention for efficient memory management, delivering high throughput LLM inference."
)

print(f"Overall: {result['overall']}")
print(f"Coherence: {result['coherence']}")
print(f"Completeness: {result['completeness']}")
print(f"Safety: {result['safety']}")
print(f"Passed: {result['passed']}")
```

## Alert Configuration

Default alert thresholds in `.env`:

| Alert | Default | Description |
|---|---|---|
| `ALERT_LATENCY_THRESHOLD_MS` | 5000 | Alert if latency exceeds 5 seconds |
| `ALERT_COST_THRESHOLD_USD` | 0.10 | Alert if single call costs over $0.10 |

## Project Structure

```
llm-observability-platform/
├── monitoring/
│   └── llm_monitor.py          # Core monitor with cost tracking and alerting
├── tracing/
│   └── tracer.py               # Distributed tracing for LLM workflows
├── evaluation/
│   └── quality_scorer.py       # Automated response quality scoring
├── tests/
│   └── test_monitoring.py
├── .env.example
├── requirements.txt
├── Makefile
└── README.md
```

## Running Tests

```bash
make test
```

## License

MIT — see [LICENSE](LICENSE)
