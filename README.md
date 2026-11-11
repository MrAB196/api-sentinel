# API Sentinel

A standalone Streamlit application for small-batch HTTP endpoint reliability checks.

## Features
- GET, POST, PUT, PATCH and DELETE requests
- JSON headers and optional JSON request body
- 1–20 requests per test with configurable timeout
- Per-request status, latency, response size and error
- Success rate and p50/p95/p99 latency summaries
- Local SQLite test history and CSV export

## Windows setup
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Tests
```powershell
pytest -q
```

## Safety and limitations
Only test endpoints you own or are authorized to test. This is not a load-testing or security-testing product. Small sample counts make percentiles indicative only. It does not follow redirects. For public deployment, add authentication, rate limiting, SSRF defenses, secret management and stronger network controls.

## GitHub
```powershell
git init
git add .
git commit -m "Build API Sentinel"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/api-sentinel.git
git push -u origin main
```
