import streamlit as st
from utils.state import init_state, new_trace_id, log_event
from utils.components import app_header, audit_badge, json_view, table

st.set_page_config(page_title="Ranking agent", page_icon="🏅", layout="wide")
init_state()
app_header("Ranking agent", "Assemble context, memory, and tools to produce rankings")

st.markdown("### Inputs")
ctx = st.selectbox("Context", [c["name"] for c in st.session_state["contexts"]] or ["(none)"])
schema = st.selectbox("Criteria schema", [s["schema_name"] for s in st.session_state["criteria_schemas"]] or ["(none)"])
use_memory = st.checkbox("Use simple memory", value=True)
use_qdrant = st.checkbox("Use Qdrant tool", value=True)
model = st.text_input("Chat model", st.session_state["settings"]["gemini_model"])

st.markdown("### Candidate items")
source = st.selectbox("Candidate source", ["clean_posts", "qdrant_stage"])
limit = st.number_input("Candidate limit", min_value=1, max_value=100, value=10)
if st.button("Load candidates"):
    items = st.session_state.get(source, [])[:limit]
    st.session_state["rank_inputs"] = items
table(st.session_state.get("rank_inputs", []), columns=None, label="Candidates")

st.markdown("### Run ranking (mock)")
if st.button("Run"):
    trace_id = new_trace_id("rank")
    inputs = st.session_state.get("rank_inputs", [])
    results = [{"item": i, "score": round(0.5 + idx*0.03, 3)} for idx, i in enumerate(inputs)]
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    st.session_state["rank_results"] = results
    audit_badge(trace_id)
    log_event("ranking.completed", data={"count": len(results), "model": model}, trace_id=trace_id)
table(st.session_state.get("rank_results", []), columns=None, label="Ranked results")

st.markdown("### Export")
if st.button("Prepare TXT"):
    res = st.session_state.get("rank_results", [])
    lines = [f"{i+1}. score={r['score']} | title={r['item'].get('title','')}" for i, r in enumerate(res)]
    txt = "Top candidates:\n" + "\n".join(lines)
    st.session_state["last_report_txt"] = txt
    st.success("Prepared TXT for report.")
    json_view({"preview": txt[:300] + ("..." if len(txt)>300 else "")}, label="Report preview")