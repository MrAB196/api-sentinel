import time
from urllib.parse import urlparse
import requests

def validate_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Enter a valid http:// or https:// URL.")
    return url

def run_api_test(url, method="GET", headers=None, body=None, count=5, timeout=10):
    validate_url(url)
    method = method.upper()
    if method not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
        raise ValueError("Unsupported HTTP method.")
    if not isinstance(count, int) or not 1 <= count <= 20:
        raise ValueError("Request count must be between 1 and 20.")
    if not isinstance(timeout, (int, float)) or not 1 <= timeout <= 30:
        raise ValueError("Timeout must be between 1 and 30 seconds.")
    results = []
    for index in range(1, count + 1):
        started = time.perf_counter()
        try:
            response = requests.request(
                method, url, headers=headers or {}, json=body,
                timeout=timeout, allow_redirects=False
            )
            elapsed = (time.perf_counter() - started) * 1000
            results.append({
                "request": index, "status": response.status_code,
                "latency_ms": round(elapsed, 2),
                "success": 200 <= response.status_code < 400,
                "content_bytes": len(response.content), "error": ""
            })
        except requests.RequestException as exc:
            elapsed = (time.perf_counter() - started) * 1000
            results.append({
                "request": index, "status": None, "latency_ms": round(elapsed, 2),
                "success": False, "content_bytes": 0, "error": str(exc)[:300]
            })
    return results

def percentile(values, p):
    if not values:
        return 0.0
    return float(__import__("numpy").percentile(values, p)) if len(values) > 1 else float(values[0])

def summarize_results(results):
    latencies = [r["latency_ms"] for r in results]
    total = len(results)
    successes = sum(bool(r["success"]) for r in results)
    return {
        "total": total,
        "successes": successes,
        "failures": total - successes,
        "success_rate": (successes / total * 100) if total else 0.0,
        "p50_ms": percentile(latencies, 50),
        "p95_ms": percentile(latencies, 95),
        "p99_ms": percentile(latencies, 99),
        "avg_ms": sum(latencies) / len(latencies) if latencies else 0.0
    }
