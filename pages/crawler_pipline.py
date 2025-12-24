import streamlit as st
from utils.state import init_state, new_trace_id, log_event
from utils.components import app_header, audit_badge, json_view, table

st.set_page_config(page_title="Crawler pipeline", page_icon="🕷️", layout="wide")
init_state()
app_header("Crawler pipeline", "Design inputs and inspect each stage")

with st.sidebar:
    st.markdown("**Stages**")
    st.markdown("- Build Reddit URLs\n- Fetch posts\n- Extract AI discussions\n- Deduplicate\n- Parse JSON\n- Deep clean\n- Stage to Qdrant")

st.markdown("### Build Reddit URLs")
with st.form("build_urls"):
    subs = st.text_area("Subreddits (one per line)", "MachineLearning\nLocalLlama\nArtificialInteligence")
    limit = st.number_input("Per-subreddit post limit", min_value=10, max_value=500, value=100, step=10)
    submitted = st.form_submit_button("Generate URLs")
    if submitted:
        trace_id = new_trace_id("crawler")
        urls = [f"https://www.reddit.com/r/{s.strip()}/new.json?limit={limit}" for s in subs.splitlines() if s.strip()]
        batch = {"trace_id": trace_id, "urls": urls}
        st.session_state["crawler_batches"].append(batch)
        audit_badge(trace_id)
        log_event("crawler.urls_generated", data=batch, trace_id=trace_id)
        st.success(f"Generated {len(urls)} URLs")

st.markdown("### Fetch posts (mock)")
if st.button("Fetch now (mock)"):
    if not st.session_state["crawler_batches"]:
        st.warning("No URL batch. Generate URLs first.")
    else:
        trace_id = st.session_state["crawler_batches"][-1]["trace_id"]
        mock_posts = [
            {"id": f"p{i}", "sub": "MachineLearning", "title": f"AI discussion {i}", "body": "Content...", "created_utc": 1730000000+i}
            for i in range(1, 21)
        ]
        st.session_state["raw_posts"] = mock_posts
        audit_badge(trace_id)
        log_event("crawler.posts_fetched", data={"count": len(mock_posts)}, trace_id=trace_id)
        st.success(f"Fetched {len(mock_posts)} posts (mock)")

table(st.session_state["raw_posts"], columns=None, label="Raw posts")

st.markdown("### Extract AI discussions")
if st.button("Extract (mock)"):
    posts = st.session_state["raw_posts"]
    extracted = [p for p in posts if "AI" in p["title"]]
    st.session_state["extracted_ai_discussions"] = extracted
    log_event("crawler.extracted_ai", data={"count": len(extracted)})

table(st.session_state["extracted_ai_discussions"], columns=None, label="Extracted AI discussions")

st.markdown("### Search deduplication + embeddings (mock)")
if st.button("Deduplicate"):
    seen = set()
    dedup = []
    for p in st.session_state["extracted_ai_discussions"]:
        if p["title"] not in seen:
            dedup.append({**p, "embedding": "[vector]"})
            seen.add(p["title"])
    st.session_state["deduplicated_posts"] = dedup
    log_event("crawler.deduplicated", data={"count": len(dedup)})
table(st.session_state["deduplicated_posts"], columns=None, label="Deduplicated posts")

st.markdown("### JSON parsing + deep cleaning")
if st.button("Parse to JSON"):
    parsed = [{"post_id": p["id"], "sub": p["sub"], "title": p["title"], "body": p["body"]} for p in st.session_state["deduplicated_posts"]]
    st.session_state["parsed_posts"] = parsed
    log_event("crawler.parsed_json", data={"count": len(parsed)})
json_view(st.session_state["parsed_posts"], label="Parsed JSON")

with st.form("deep_clean"):
    rm_short = st.checkbox("Remove bodies < 20 chars", value=True)
    lower = st.checkbox("Lowercase bodies", value=True)
    keep_fields = st.multiselect("Keep fields", options=["post_id", "sub", "title", "body"], default=["post_id","sub","title","body"])
    submit_clean = st.form_submit_button("Apply deep clean")
    if submit_clean:
        cleaned = []
        for p in st.session_state["parsed_posts"]:
            body = p["body"].lower() if lower else p["body"]
            if rm_short and len(body) < 20:
                continue
            cleaned.append({k: p[k] for k in keep_fields})
        st.session_state["clean_posts"] = cleaned
        log_event("crawler.deep_cleaned", data={"count": len(cleaned)})
table(st.session_state["clean_posts"], columns=None, label="Clean posts")

st.markdown("### Stage to Qdrant (mock)")
if st.button("Stage as documents"):
    staged = [{"doc_id": f"d{i}", "payload": p, "vector": "[embedding]"} for i, p in enumerate(st.session_state["clean_posts"], start=1)]
    st.session_state["qdrant_stage"] = staged
    log_event("crawler.qdrant_staged", data={"count": len(staged)})
table(st.session_state["qdrant_stage"], columns=None, label="Qdrant stage")