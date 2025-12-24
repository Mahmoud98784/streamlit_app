import streamlit as st
from utils.state import init_state
from utils.components import app_header, table, json_view

st.set_page_config(page_title="Qdrant browser", page_icon="🧭", layout="wide")
init_state()
app_header("Qdrant browser", "Configure and preview staged vectors (mock)")

st.markdown("### Connection settings")
st.session_state["settings"]["qdrant_host"] = st.text_input("Host", st.session_state["settings"]["qdrant_host"])
st.session_state["settings"]["qdrant_port"] = st.number_input("Port", value=st.session_state["settings"]["qdrant_port"])
st.session_state["settings"]["qdrant_collection"] = st.text_input("Collection", st.session_state["settings"]["qdrant_collection"])

st.markdown("### Staged documents")
table(st.session_state["qdrant_stage"], columns=None, label="Staged points")

st.markdown("### Search (mock)")
query = st.text_input("Query text")
top_k = st.number_input("Top K", min_value=1, max_value=50, value=5)
if st.button("Search"):
    staged = st.session_state["qdrant_stage"]
    results = staged[:top_k] if staged else []
    st.session_state["qdrant_results"] = results
table(st.session_state.get("qdrant_results", []), columns=None, label="Search results")