# 004 – Assistant

Starts as a copy of experiment 003 (a streaming chat with a local LLM) and grows into a more robust assistant: **tools** and a better UI.

- **UI:** [Streamlit](https://streamlit.io/) (`app.py`)
- **Backend:** plain Python (`backend.py`) using the `ollama` client
- **LLM:** [Ollama](https://ollama.com/) running in Docker, model `qwen3:8b`

## Goal

Learn the minimal path from a UI to a locally hosted model: start the model server, call it with `stream=True`, and forward chunks to the screen with `st.write_stream`.

## Run

```bash
# 1. start Ollama in Docker
docker compose up -d

# 2. download the model once (~5 GB, stored in the `ollama` volume)
docker compose exec ollama ollama pull qwen3:8b

# 3. start the UI
uv run streamlit run app.py
```

Open http://localhost:8501. To stop the LLM: `docker compose down`.

For an NVIDIA GPU, uncomment the `deploy` block in `docker-compose.yml`.

## How it works

```
Streamlit UI ──st.write_stream──▶ stream_chat() ──ollama client (stream=True)──▶ Ollama :11434
```

`stream_chat()` is a generator that yields each text chunk Ollama sends back. Streamlit renders chunks as they arrive and returns the full text, which is stored in `st.session_state` so the model sees the whole conversation on the next turn.

## Things to try

- Change `MODEL` in `backend.py` (any model from https://ollama.com/library)
- Add a system prompt or a temperature slider
- Add a "Stop" button to cancel generation
