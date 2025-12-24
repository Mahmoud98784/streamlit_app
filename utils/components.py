import streamlit as st

def app_header(title, subtitle=None):
    st.title(title)
    if subtitle:
        st.caption(subtitle)

def audit_badge(trace_id: str):
    if trace_id:
        st.code(f"trace_id={trace_id}", language="text")

def two_col():
    return st.columns([1, 1, 1])

def json_view(data, label="Preview JSON"):
    st.markdown(f"**{label}:**")
    st.json(data, expanded=False)

def table(items, columns, label="Table"):
    st.markdown(f"**{label}:**")
    if items:
        st.dataframe(items, use_container_width=True, hide_index=True)
    else:
        st.info("No items to display yet.")