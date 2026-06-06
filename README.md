# LLM Observability Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/Krishna89287/llm-observability-platform/daily-commit.yml?style=flat-square&label=Daily+Build)](https://github.com/Krishna89287/llm-observability-platform/actions)
[![GitHub stars](https://img.shields.io/github/stars/Krishna89287/llm-observability-platform?style=flat-square)](https://github.com/Krishna89287/llm-observability-platform)

Production observability for LLM applications — cost, latency, quality, hallucination tracking

**Stack:** Python · Prometheus · Grafana · OpenTelemetry · FastAPI · PostgreSQL


## Architecture

```
LLM Application
    │
    ▼
┌─────────────────────────────────┐
│          LLM Monitor             │
│   Records every API call        │
│   Cost · Latency · Tokens       │
└─────────────────────────────────┘
    │
    ├─────────────┬──────────────┐
    ▼             ▼              ▼
┌────────┐  ┌─────────┐  ┌──────────┐
│  Cost  │  │ Quality │  │ Tracer   │
│ Calc   │  │ Scorer  │  │ OpenTel  │
│GPT/Claud│  │Coherence│  │Spans·    │
│Pricing │  │Safety   │  │Events    │
└────────┘  └─────────┘  └──────────┘
    │
    ▼
┌─────────────────────────────────┐
│        Alert Engine              │
│  Latency > 5s → Alert          │
│  Cost > $0.10 → Alert          │
│  Quality < 0.7 → Alert         │
└─────────────────────────────────┘
    │
    ▼
Prometheus → Grafana Dashboard
```



## Demo

```
$ python monitoring/llm_monitor.py

LLMMonitor initialized
CostCalculator loaded: 6 providers

Recording 5 LLM calls...
✅ gpt-4 | 1200ms | $0.0042 | quality=0.91
✅ claude-3-sonnet | 890ms | $0.0018 | quality=0.88
✅ gpt-3.5-turbo | 340ms | $0.0003 | quality=0.79
⚠️  gpt-4 | 5240ms | $0.0089 | ALERT: HIGH LATENCY
✅ claude-3-haiku | 280ms | $0.0002 | quality=0.82

Dashboard Metrics:
  total_calls: 5
  total_cost_usd: $0.0154
  avg_latency_ms: 1590ms
  p99_latency_ms: 5240ms
  active_alerts: 1
  model_breakdown:
    gpt-4: 2 calls, $0.0131
    claude-3-sonnet: 1 call, $0.0018
    claude-3-haiku: 1 call, $0.0002
```


## Quick Start

```bash
git clone https://github.com/Krishna89287/llm-observability-platform.git
cd llm-observability-platform
pip install -r requirements.txt
cp .env.example .env
make run
```

## Running Tests

```bash
make test
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Built by [Krishna Gove](https://github.com/Krishna89287) · [LinkedIn](https://www.linkedin.com/in/krishna-reddy-327463222)
