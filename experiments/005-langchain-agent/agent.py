import sys

from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from tools import calculate, get_weather

model = ChatOllama(model="qwen3:8b", base_url="http://localhost:11434")

agent = create_agent(
    model,
    tools=[get_weather, calculate],
    system_prompt="You are a helpful assistant. Use the tools when they help; never do arithmetic yourself.",
)


def ask(question: str) -> None:
    """Run the agent and print each step: tool calls, tool results, final answer."""
    for step in agent.stream({"messages": [("user", question)]}, stream_mode="updates"):
        for update in step.values():
            for message in update["messages"]:
                if message.type == "ai" and message.tool_calls:
                    for call in message.tool_calls:
                        print(f"→ tool call: {call['name']}({call['args']})")
                elif message.type == "tool":
                    print(f"← tool result: {message.content}")
                elif message.type == "ai":
                    print(f"\n{message.content}")


if __name__ == "__main__":
    ask(" ".join(sys.argv[1:]) or "What's the weather in Warsaw, and what is that temperature in Fahrenheit?")
