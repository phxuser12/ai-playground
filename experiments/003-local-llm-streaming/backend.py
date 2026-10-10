import ollama

HOST = "http://localhost:11434"
MODEL = "llama3.2:1b"

client = ollama.Client(host=HOST)


def stream_chat(messages):
    """Yield the reply text chunk by chunk as the model generates it."""
    for chunk in client.chat(model=MODEL, messages=messages, stream=True):
        yield chunk["message"]["content"]
