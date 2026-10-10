# 004 – Assistant

Starts as a copy of experiment 003 (a streaming chat with a local LLM) and grows into a more robust assistant: **tools** and a better UI.

- **UI:** React + TypeScript with [Vite](https://vite.dev/) (`web/`)
- **Backend:** Python: `backend.py` talks to Ollama, `server.py` ([FastAPI](https://fastapi.tiangolo.com/)) exposes it over HTTP
- **LLM:** [Ollama](https://ollama.com/) running in Docker, model `qwen3:8b`

## Goal

Build on 003 with a proper split between a TypeScript UI and a Python backend, then add tools and a richer UI. So far: the model's **thinking** is shown, and a side panel shows the **full request and response** of every call.

## Run

```bash
# 1. start Ollama in Docker
docker compose up -d

# 2. download the model once (~5 GB, stored in the `ollama` volume)
docker compose exec ollama ollama pull qwen3:8b

# 3. start the Python backend (port 8000)
uv run uvicorn server:app --reload

# 4. start the UI (in another terminal)
cd web && npm install && npm run dev
```

Open http://localhost:5173 (Vite proxies `/api` to the backend). To stop the LLM: `docker compose down`.

The `deploy` block in `docker-compose.yml` enables an NVIDIA GPU; remove it for CPU-only.

## How it works

```
React UI ──POST /api/chat (NDJSON stream)──▶ FastAPI ──▶ stream_chat() ──stream=True──▶ Ollama :11434
```

- `stream_chat()` yields `("thinking" | "content", text)` chunks and records the full request/response in an in-memory log.
- `server.py` sends each chunk to the browser as one JSON line (`{"type": "thinking", "text": "..."}`); logs are available at `GET /api/logs`.
- The UI keeps the conversation and sends the whole history on each turn (the server is stateless). Stored thinking is shown but never sent back to the model.

## Things to try

- Change `MODEL` in `backend.py` (any model from https://ollama.com/library)
- Add a system prompt or a temperature slider
- Add a "Stop" button to cancel generation
