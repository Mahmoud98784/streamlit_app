import streamlit as st
from utils.state import init_state
from utils.components import app_header, table

st.set_page_config(page_title="Logs & traceability", page_icon="📚", layout="wide")
init_state()
app_header("Logs & traceability", "Audit trail of actions and artifacts")

st.markdown("### Filters")
level = st.selectbox("Level", ["ALL", "INFO", "WARN", "ERROR"], index=0)
kw = st.text_input("Contains")

logs = st.session_state["logs"]
if level != "ALL":
    logs = [l for l in logs if l["level"] == level]
if kw:
    logs = [l for l in logs if kw.lower() in str(l).lower()]

table(logs, columns=None, label="Events")