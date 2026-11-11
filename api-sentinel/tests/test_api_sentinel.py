import pytest
from api_sentinel import validate_url, summarize_results

def test_rejects_invalid_scheme():
    with pytest.raises(ValueError):
        validate_url("file:///etc/passwd")

def test_accepts_http_url():
    assert validate_url("https://example.com") == "https://example.com"

def test_summary_calculates_success_and_failure():
    results = [
        {"success": True, "latency_ms": 10.0},
        {"success": False, "latency_ms": 30.0},
    ]
    summary = summarize_results(results)
    assert summary["total"] == 2
    assert summary["success_rate"] == 50
    assert summary["failures"] == 1
    assert summary["p50_ms"] == 20
