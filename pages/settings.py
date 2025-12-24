import streamlit as st
from utils.state import init_state, log_event
from utils.components import app_header

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
init_state()
app_header("Settings", "Environment endpoints and API keys")

st.markdown("### Endpoints")
st.session_state["settings"]["qdrant_host"] = st.text_input("Qdrant host", st.session_state["settings"]["qdrant_host"])
st.session_state["settings"]["qdrant_port"] = st.number_input("Qdrant port", value=st.session_state["settings"]["qdrant_port"])
st.session_state["settings"]["qdrant_collection"] = st.text_input("Qdrant collection", st.session_state["settings"]["qdrant_collection"])

st.markdown("### Models")
st.session_state["settings"]["gemini_model"] = st.text_input("Chat model", st.session_state["settings"]["gemini_model"])

st.markdown("### API keys (stored in session only)")
api = st.session_state["settings"]["api_keys"]
api["cohere"] = st.text_input("Cohere API key", api["cohere"])
api["gemini"] = st.text_input("Gemini API key", api["gemini"])
api["huggingface"] = st.text_input("HuggingFace token", api["huggingface"])

if st.button("Save settings"):
    log_event("settings.saved", data=st.session_state["settings"])
    st.success("Settings saved in session (not persisted).")