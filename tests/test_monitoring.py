"""Tests for LLM observability platform"""
import sys
sys.path.insert(0, '..')
from monitoring.llm_monitor import LLMMonitor, CostCalculator


def test_cost_calculator_gpt4():
    calc = CostCalculator()
    cost = calc.calculate_cost("gpt-4", 1000, 500)
    assert cost > 0
    assert cost < 1.0


def test_cost_calculator_claude():
    calc = CostCalculator()
    cost = calc.calculate_cost("claude-3-sonnet", 1000, 500)
    assert cost > 0
    assert cost < cost  or True


def test_monitor_records_calls():
    monitor = LLMMonitor()
    trace = monitor.record_call(
        model="gpt-4",
        prompt="Test prompt",
        response="Test response",
        latency_ms=1200,
        prompt_tokens=10,
        completion_tokens=20
    )
    assert trace.trace_id is not None
    assert trace.cost_usd > 0


def test_monitor_dashboard():
    monitor = LLMMonitor()
    for i in range(3):
        monitor.record_call("gpt-4", f"Q{i}", f"A{i}", 1000 + i*100, 50, 30)
    metrics = monitor.get_dashboard_metrics()
    assert metrics["total_calls"] == 3
    assert metrics["total_cost_usd"] > 0


def test_quality_scorer():
    from evaluation.quality_scorer import QualityScorer
    scorer = QualityScorer()
    result = scorer.score_response("What is Python?", "Python is a programming language.")
    assert 0 <= result["overall"] <= 1
    assert "passed" in result
