import streamlit as st
import pandas as pd
import json
from api_sentinel import run_api_test, summarize_results
from database import init_db, save_run, list_runs

st.set_page_config(page_title="API Sentinel", page_icon="🛰️", layout="wide")
init_db()
st.title("🛰️ API Sentinel")
st.caption("HTTP endpoint reliability and latency inspection")
with st.form("run"):
    a,b = st.columns([3,1])
    url = a.text_input("Endpoint URL", "https://httpbin.org/get")
    method = b.selectbox("Method", ["GET","POST","PUT","PATCH","DELETE"])
    headers_text = st.text_area("Headers (JSON)", '{"Accept":"application/json"}')
    body_text = st.text_area("JSON body (optional)", "")
    count = st.slider("Requests", 1, 20, 5)
    timeout = st.slider("Timeout (seconds)", 1, 30, 10)
    go = st.form_submit_button("Run test", type="primary")
if go:
    try:
        headers = json.loads(headers_text or "{}")
        if not isinstance(headers, dict): raise ValueError("Headers must be a JSON object")
        body = json.loads(body_text) if body_text.strip() else None
        with st.spinner("Testing endpoint..."):
            results = run_api_test(url, method, headers, body, count, timeout)
        summary = summarize_results(results)
        save_run(url, method, summary)
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Success rate", f'{summary["success_rate"]:.1f}%')
        c2.metric("p50", f'{summary["p50_ms"]:.1f} ms')
        c3.metric("p95", f'{summary["p95_ms"]:.1f} ms')
        c4.metric("Failures", summary["failures"])
        frame = pd.DataFrame(results)
        st.dataframe(frame, use_container_width=True, hide_index=True)
        st.download_button("Download CSV", frame.to_csv(index=False), "api_sentinel_results.csv", "text/csv")
    except Exception as e:
        st.error(str(e))
st.divider()
st.subheader("Recent test history")
history = list_runs()
if history: st.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True)
else: st.caption("No tests recorded yet.")
st.warning("Only test APIs you own or are authorized to test. This is not a load-testing tool.")
