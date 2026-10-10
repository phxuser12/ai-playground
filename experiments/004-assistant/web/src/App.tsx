import { useEffect, useState } from "react";
import { clearLogs, getLogs, getModel, streamChat, type LogEntry, type Message } from "./api";

export default function App() {
  const [model, setModel] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    getModel().then(setModel);
    getLogs().then(setLogs);
  }, []);

  async function send() {
    const text = input.trim();
    if (!text || busy) return;
    const history: Message[] = [...messages, { role: "user", content: text }];
    // Last message is the assistant reply being streamed in.
    setMessages([...history, { role: "assistant", content: "", thinking: "" }]);
    setInput("");
    setBusy(true);

    const update = (patch: (m: Message) => Message) =>
      setMessages((prev) => [...prev.slice(0, -1), patch(prev[prev.length - 1])]);

    try {
      for await (const event of streamChat(history)) {
        if (event.type === "thinking") update((m) => ({ ...m, thinking: m.thinking + event.text }));
        else if (event.type === "content") update((m) => ({ ...m, content: m.content + event.text }));
        else update((m) => ({ ...m, content: m.content + `\n\n⚠️ ${event.text}` }));
      }
    } catch (e) {
      update((m) => ({ ...m, content: m.content + `\n\n⚠️ ${e}` }));
    } finally {
      setBusy(false);
      setLogs(await getLogs());
    }
  }

  return (
    <div className="layout">
      <main className="chat">
        <header>
          <h1>Local LLM chat</h1>
          <small>Model: {model} (Ollama in Docker)</small>
        </header>
        <div className="messages">
          {messages.map((m, i) => (
            <div key={i} className={`message ${m.role}`}>
              {m.thinking && (
                <details open={busy && i === messages.length - 1 && !m.content}>
                  <summary>{busy && i === messages.length - 1 && !m.content ? "Thinking…" : "Thought"}</summary>
                  <div className="thinking">{m.thinking}</div>
                </details>
              )}
              <div className="content">{m.content}</div>
            </div>
          ))}
        </div>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            send();
          }}
        >
          <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Say something" autoFocus />
          <button disabled={busy}>Send</button>
        </form>
      </main>

      <aside className="logs">
        <h2>Logs</h2>
        <button
          onClick={async () => {
            await clearLogs();
            setLogs([]);
          }}
        >
          Clear logs
        </button>
        {logs.length === 0 && <small>No requests yet.</small>}
        {logs
          .map((entry, i) => ({ entry, n: i + 1 }))
          .reverse()
          .map(({ entry, n }) => (
            <details key={n} open={n === logs.length}>
              <summary>
                #{n} · {entry.time}
              </summary>
              <b>Request</b>
              <pre>{JSON.stringify(entry.request, null, 2)}</pre>
              <b>Response</b>
              <pre>{JSON.stringify(entry.response, null, 2)}</pre>
              {entry.error && <pre className="error">{entry.error}</pre>}
            </details>
          ))}
      </aside>
    </div>
  );
}
