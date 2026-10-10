# ai-playground

A personal sandbox for experimenting with AI: LLM APIs, agents, retrieval, tooling, and model internals. Each experiment is small, self-contained, and meant for learning rather than production use.

## Structure

Every experiment lives in its own numbered folder under `experiments/`:

```
experiments/
├── 001-function-calling/
├── 002-rag/
├── 003-agent-memory/
├── 004-langgraph/
├── 005-mcp/
├── 006-pytorch-transformer/
└── 007-vector-search/
```

> The list above is only an example. New experiments are added over time.

### Naming convention

- Prefix each folder with a zero-padded, incrementing number (`001`, `002`, …) so experiments stay in chronological order.
- Follow the number with a short, kebab-case topic name (e.g. `008-fine-tuning`).

### Inside an experiment

Each experiment folder should be self-contained and typically includes:

- `README.md`: the goal, how to run it, and notes or findings
- Source code and notebooks
- Its own dependency file (e.g. `requirements.txt` or `pyproject.toml`), so experiments don't conflict with each other

## Adding a new experiment

1. Create the next numbered folder under `experiments/`.
2. Add a `README.md` describing what you're trying out.
3. Build, run, and write down what you learned.
