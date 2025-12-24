import streamlit as st
from utils.state import init_state, new_trace_id, log_event
from utils.components import app_header, json_view, table, audit_badge

st.set_page_config(page_title="Context provider", page_icon="🎛️", layout="wide")
init_state()
app_header("Context provider", "Design rich, varied scenarios and criteria")

st.markdown("### Context template")
with st.form("context_form"):
    name = st.text_input("Context name", "Model evaluation scenario A")
    description = st.text_area("Description", "Evaluate models on summarization of Reddit AI threads with code blocks.")
    variables = st.text_area("Variables (one per line)", "temperature=0.7\nlength=short\nstyle=technical")
    randomize = st.checkbox("Enable randomization", value=True)
    submit_ctx = st.form_submit_button("Save context")
    if submit_ctx:
        trace_id = new_trace_id("ctx")
        ctx = {
            "trace_id": trace_id,
            "name": name,
            "description": description,
            "variables": [v for v in variables.splitlines() if v.strip()],
            "randomize": randomize,
        }
        st.session_state["contexts"].append(ctx)
        audit_badge(trace_id)
        log_event("context.saved", data=ctx, trace_id=trace_id)
        st.success("Context saved.")

table(st.session_state["contexts"], columns=None, label="Saved contexts")

st.markdown("### Criteria schema")
with st.form("criteria_form"):
    schema_name = st.text_input("Schema name", "Ranking criteria v1")
    metrics = st.text_area("Metrics (one per line)", "faithfulness\nconciseness\nreasoning depth\nformat compliance")
    weights = st.text_area("Weights (parallel lines)", "0.35\n0.2\n0.3\n0.15")
    submit_schema = st.form_submit_button("Save schema")
    if submit_schema:
        trace_id = new_trace_id("schema")
        schema = {
            "trace_id": trace_id,
            "schema_name": schema_name,
            "metrics": [m for m in metrics.splitlines() if m.strip()],
            "weights": [float(w) for w in weights.splitlines() if w.strip()],
        }
        st.session_state["criteria_schemas"].append(schema)
        audit_badge(trace_id)
        log_event("schema.saved", data=schema, trace_id=trace_id)
        st.success("Schema saved.")

table(st.session_state["criteria_schemas"], columns=None, label="Criteria schemas")