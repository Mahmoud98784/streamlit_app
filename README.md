Below is a professional `README.md` tailored for the `streamlit_app` repository. It explains the purpose, setup, structure, and usage of the Streamlit interfaces for the crawler and ranking workflows:

---

## 📘 `README.md`

```markdown
# 🧠 Streamlit App for AI Crawler & Ranking Workflows

This project provides a modular Streamlit interface for orchestrating and evaluating AI tools across the full SDLC. It integrates with n8n workflows (external) and supports mock execution, traceability, and future extensibility.

---

## 🚀 Features

- **Crawler pipeline**: Build Reddit URL batches, fetch posts, extract AI discussions, deduplicate, clean, and stage to Qdrant.
- **Context provider**: Design randomized evaluation scenarios and criteria schemas.
- **Ranking agent**: Assemble context, memory, and tools to rank AI model outputs.
- **Report generator**: Format and export TXT/MD reports for Telegram delivery.
- **Qdrant browser**: Preview staged vectors and mock search results.
- **Embeddings & reranker config**: Configure HuggingFace and Cohere models.
- **Logs & traceability**: Audit every action with trace IDs and timestamps.

---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/Mahmoud98784/streamlit_app.git
cd streamlit_app
```

### 2. Install dependencies

```bash
pip install streamlit pydantic
```

### 3. Run the app

```bash
streamlit run app.py
```

---

## 🗂️ Folder structure

```
streamlit_app/
├── app.py                  # Main dashboard
├── pages/                  # Modular Streamlit pages
│   ├── 01_crawler_pipeline.py
│   ├── 02_data_explorer.py
│   ├── 03_qdrant_browser.py
│   ├── 04_context_provider.py
│   ├── 05_ranking_agent.py
│   ├── 06_embeddings_reranker.py
│   ├── 07_report_generator.py
│   ├── 08_sender_mock.py
│   ├── 09_settings.py
│   └── 10_logs.py
├── utils/                  # Shared components and state
│   ├── state.py
│   └── components.py
└── .gitignore
```

---

## 🔐 Secrets & API Keys

This app uses session-based storage for API keys. Do **not** hardcode secrets. Instead:

1. Create a `.env` file (optional)
2. Add `.env` to `.gitignore`
3. Load secrets using `os.getenv()` if needed

---

## 📦 Integration points

- **n8n workflows**: All mock actions are designed to be replaced with webhook calls.
- **Qdrant**: Staged documents can be upserted and searched via API.
- **Telegram**: Reports can be sent via bot once connected.

---

## 📄 License

This project is for educational and internal evaluation purposes. No license specified.

---

## 🤝 Contributing

Feel free to fork and extend. For major changes, open an issue first to discuss what you’d like to change.

---

## 👤 Author

Mahmoud98784  
GitHub: [github.com/Mahmoud98784](https://github.com/Mahmoud98784)

```


