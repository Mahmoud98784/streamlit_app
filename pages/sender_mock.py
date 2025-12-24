import streamlit as st
from utils.state import init_state, log_event, new_trace_id
from utils.components import app_header, table

st.set_page_config(page_title="Document sender (mock)", page_icon="📤", layout="wide")
init_state()
app_header("Document sender (mock)", "Preview payload and mock-send to channel")

st.markdown("### Channel")
st.session_state["settings"]["telegram_channel"] = st.text_input("Telegram channel", st.session_state["settings"]["telegram_channel"])

st.markdown("### Select report")
reports = st.session_state.get("reports", [])
labels = [f"{r['title']} ({r['fmt']})" for r in reports] or ["(none)"]
idx = st.selectbox("Report", list(range(len(labels))), format_func=lambda i: labels[i] if reports else "(none)")
selected = reports[idx] if reports else None

if selected:
    st.markdown("**Payload preview:**")
    st.text_area("Content", selected["content"], height=200)
    if st.button("Send (mock)"):
        trace_id = new_trace_id("send")
        st.session_state["outbox"].append({"trace_id": trace_id, "channel": st.session_state["settings"]["telegram_channel"], "content": selected["content"]})
        log_event("report.sent_mock", data={"channel": st.session_state["settings"]["telegram_channel"], "size": len(selected["content"])}, trace_id=trace_id)
        st.success(f"Queued for sending (mock). trace_id={trace_id}")

table(st.session_state["outbox"], columns=None, label="Outbox (mock)")