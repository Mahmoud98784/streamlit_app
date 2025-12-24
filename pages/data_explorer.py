import streamlit as st
from utils.state import init_state
from utils.components import app_header, json_view, table

st.set_page_config(page_title="Data explorer", page_icon="🧾", layout="wide")
init_state()
app_header("Data explorer", "Inspect and transform intermediate JSON")

st.markdown("### Select source")
source = st.selectbox("Source dataset", ["raw_posts", "extracted_ai_discussions", "deduplicated_posts", "parsed_posts", "clean_posts", "qdrant_stage"])
data = st.session_state.get(source, [])
table(data, columns=None, label=f"{source}")

st.markdown("### Filter and transform (mock)")
kw = st.text_input("Filter title contains", "")
limit = st.number_input("Limit", min_value=1, max_value=1000, value=50)
if st.button("Apply"):
    filtered = [d for d in data if isinstance(d, dict) and kw.lower() in str(d).lower()]
    st.session_state["explorer_view"] = filtered[:limit]
json_view(st.session_state.get("explorer_view", []), label="Transformed view")