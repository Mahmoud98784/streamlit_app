import streamlit as st
from utils.state import init_state, log_event
from utils.components import app_header

st.set_page_config(page_title="Embeddings & reranker", page_icon="🧬", layout="wide")
init_state()
app_header("Embeddings & reranker", "Configure models used in dedup and retrieval")

st.markdown("### Embeddings")
emb_model = st.text_input("Embedding model", st.session_state["settings"]["embedding_model"])
emb_dim = st.number_input("Vector dimension (informational)", min_value=128, max_value=4096, value=384)
st.session_state["settings"]["embedding_model"] = emb_model

st.markdown("### Reranker")
reranker_model = st.text_input("Reranker model", st.session_state["settings"]["reranker_model"])
top_k = st.number_input("Reranker top_k", min_value=1, max_value=100, value=20)
st.session_state["settings"]["reranker_model"] = reranker_model

if st.button("Save"):
    log_event("models.config_saved", data={"embedding_model": emb_model, "reranker_model": reranker_model, "top_k": top_k})
    st.success("Model configuration saved.")