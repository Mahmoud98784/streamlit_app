import streamlit as st
import time
import uuid

def init_state():
    defaults = {
        "settings": {
            "qdrant_host": "http://qdrant:6333",
            "qdrant_port": 6333,
            "qdrant_collection": "ai-comments",
            "embedding_model": "intfloat/e5-base-v2",
            "reranker_model": "cohere/rerank-v3.5",
            "gemini_model": "gemini-2.5-flash",
            "telegram_channel": "",
            "api_keys": {"cohere": "", 
                         "gemini": "", 
                         "huggingface": ""},
        },
        "crawler_batches": [],
        "raw_posts": [],
        "extracted_ai_discussions": [],
        "deduplicated_posts": [],
        "parsed_posts": [],
        "clean_posts": [],
        "qdrant_stage": [],
        "contexts": [],
        "criteria_schemas": [],
        "rank_inputs": [],
        "rank_results": [],
        "reports": [],
        "outbox": [],
        "logs": [],
        "last_trace_id": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def new_trace_id(prefix="trace"):
    tid = f"{prefix}-{int(time.time())}-{uuid.uuid4().hex[:8]}"
    return tid

def log_event(event, level="INFO", trace_id=None, data=None):
    st.session_state["logs"].append({
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "level": level,
        "event": event,
        "trace_id": trace_id or new_trace_id("evt"),
        "data": data or {},
    })