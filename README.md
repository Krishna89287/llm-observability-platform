# llm-observability-platform

> Know what your LLMs are doing and what they're costing

[![Python](https://img.shields.io/badge/python-3.11+-blue?style=flat-square)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Build](https://img.shields.io/github/actions/workflow/status/Krishna89287/llm-observability-platform/daily-commit.yml?style=flat-square)](https://github.com/Krishna89287/llm-observability-platform/actions)

Average latency is a lie. It looks fine right up until P99 is 12 seconds and users are refreshing the page.

This platform tracks the three metrics that actually matter for LLM applications: cost per request broken down by model, P99 latency rather than average, and response quality scores for every request. When something crosses a threshold you find out immediately rather than from a support ticket.

All metrics feed into Prometheus so they sit alongside the rest of your infrastructure observability.

## What it looks like running

![demo](docs/demo.svg)

## Getting started

```bash
git clone https://github.com/Krishna89287/llm-observability-platform
cd llm-observability-platform
pip install -r requirements.txt
cp .env.example .env
python monitoring/platform.py
```

**Stack:** Python · Prometheus · Grafana · OpenTelemetry · Langfuse · FastAPI

---

Built by [Krishna Gove](https://github.com/Krishna89287) — working on AI and cloud infrastructure in Munich.
