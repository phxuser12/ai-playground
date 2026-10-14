# 005 – LangChain agent

A very small agent built with [LangChain](https://python.langchain.com/) that decides on its own when to call tools. It talks to a local LLM served by Ollama (Docker).

## Goal

See the agent loop in its simplest form: the model gets a question, **chooses a tool**, the tool runs, the result goes back to the model, and it answers.

## Tools

| Tool | What it does |
|---|---|
| `get_weather(city)` | Current weather via the free [Open-Meteo](https://open-meteo.com/) API (no key needed) |
| `calculate(expression)` | Arithmetic (`+ - * / // % **`, parentheses), parsed with `ast`, not `eval`, so it is safe |

A tool is a plain Python function with the `@tool` decorator; LangChain turns its name, type hints and docstring into the schema the model sees (`tools.py`).

## Run

```bash
# 1. start Ollama in Docker, pull the model once (skip if experiment 004's Ollama is already running)
docker compose up -d
docker compose exec ollama ollama pull qwen3:8b

# 2. ask the agent something
uv run python agent.py "What's the weather in Warsaw?"
uv run python agent.py "What is (1234 + 5678) * 3 / 7 ?"
```

Both experiments use port 11434, so only one Ollama container can run at a time. Without arguments, `agent.py` asks a weather + arithmetic question. It prints every step:

```
→ tool call: get_weather({'city': 'Warsaw'})
← tool result: Warsaw, Poland: 6.7°C, wind 12.6 km/h (WMO weather code 3)
The current weather in Warsaw is 6.7°C ...
```

## How it works

`create_agent(model, tools, system_prompt)` builds the loop: model → (tool calls → tool results → model)* → final answer. `ChatOllama` is the connection to Ollama.

## Notes

- A small local model doesn't always follow instructions: asked for a Fahrenheit conversion, `qwen3:8b` did the arithmetic itself instead of calling `calculate`, despite the system prompt.
- Qwen3 thinks before answering, so a call can take tens of seconds.

## Things to try

- Add a third tool (current time, unit conversion)
- Add conversation memory so follow-up questions work
- Stream tokens instead of whole steps
- Compare tool-calling reliability across models
