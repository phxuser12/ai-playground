import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend import MODEL, stream_chat

app = FastAPI()
logs: list[dict] = []


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


@app.get("/api/info")
def info():
    return {"model": MODEL}


@app.post("/api/chat")
def chat(request: ChatRequest):
    """Stream newline-delimited JSON events: {"type": "thinking"|"content"|"error", "text": ...}."""
    messages = [m.model_dump() for m in request.messages]

    def events():
        try:
            for kind, text in stream_chat(messages, logs):
                yield json.dumps({"type": kind, "text": text}) + "\n"
        except Exception as e:
            yield json.dumps({"type": "error", "text": repr(e)}) + "\n"

    return StreamingResponse(events(), media_type="application/x-ndjson")


@app.get("/api/logs")
def get_logs():
    return logs


@app.delete("/api/logs")
def clear_logs():
    logs.clear()
