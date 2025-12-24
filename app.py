import streamlit as st
from utils.state import init_state, new_trace_id
from utils.components import app_header

st.set_page_config(page_title="AI Pipeline Console", page_icon="🧭", layout="wide")
init_state()

app_header(title="AI Pipeline Console", subtitle="Interfaces for Crawler and Ranking Workflows")

st.markdown("### Overview")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Crawler batches", len(st.session_state.get("crawler_batches", [])))
with col2:
    st.metric("Posts parsed", len(st.session_state.get("parsed_posts", [])))
with col3:
    st.metric("Vectors staged", len(st.session_state.get("qdrant_stage", [])))
with col4:
    st.metric("Reports generated", len(st.session_state.get("reports", [])))

st.divider()

st.markdown("### Quick actions")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("New crawl batch"):
        st.session_state["last_trace_id"] = new_trace_id("crawl")
        st.success(f"Initialized new crawl batch. trace_id={st.session_state['last_trace_id']}")
with c2:
    if st.button("Open Context Provider"):
        st.switch_page("pages/context_provider.py")
with c3:
    if st.button("Open Ranking Agent"):
        st.switch_page("pages/ranking_agent.py")

st.info("Use the sidebar to navigate pages. All actions preserve audit fields until final output.")