import time

import ollama

HOST = "http://localhost:11434"
MODEL = "qwen3:8b"

client = ollama.Client(host=HOST)


def stream_chat(messages, log):
    """Yield ("thinking" | "content", text) chunks; append the full request/response to `log`."""
    # Keep only what Ollama needs (the UI also stores "thinking" on messages).
    messages = [{"role": m["role"], "content": m["content"]} for m in messages]
    entry = {
        "time": time.strftime("%H:%M:%S"),
        "request": {"model": MODEL, "messages": list(messages), "stream": True},
        "response": {"content": "", "thinking": "", "final_chunk": None},
        "error": None,
    }
    log.append(entry)
    try:
        for chunk in client.chat(model=MODEL, messages=messages, stream=True):
            message = chunk["message"]
            thinking_part = message.get("thinking") or ""
            entry["response"]["thinking"] += thinking_part
            entry["response"]["content"] += message["content"]
            if chunk.get("done"):
                entry["response"]["final_chunk"] = chunk.model_dump(exclude={"message"})
            if thinking_part:
                yield "thinking", thinking_part
            if message["content"]:
                yield "content", message["content"]
    except Exception as e:
        entry["error"] = repr(e)
        raise
