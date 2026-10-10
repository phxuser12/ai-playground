export type Message = { role: "user" | "assistant"; content: string; thinking?: string };

export type StreamEvent = { type: "thinking" | "content" | "error"; text: string };

export type LogEntry = {
  time: string;
  request: unknown;
  response: unknown;
  error: string | null;
};

export async function getModel(): Promise<string> {
  return (await (await fetch("/api/info")).json()).model;
}

export async function getLogs(): Promise<LogEntry[]> {
  return (await fetch("/api/logs")).json();
}

export async function clearLogs(): Promise<void> {
  await fetch("/api/logs", { method: "DELETE" });
}

/** POST the conversation and yield streamed events (newline-delimited JSON). */
export async function* streamChat(messages: Message[]): AsyncGenerator<StreamEvent> {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    // Only role/content go to the server; the stored "thinking" stays in the UI.
    body: JSON.stringify({ messages: messages.map(({ role, content }) => ({ role, content })) }),
  });
  if (!response.ok || !response.body) throw new Error(`HTTP ${response.status}`);

  const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += value;
    const lines = buffer.split("\n");
    buffer = lines.pop()!;
    for (const line of lines) if (line) yield JSON.parse(line) as StreamEvent;
  }
}
