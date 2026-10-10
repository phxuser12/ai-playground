import streamlit as st

from backend import MODEL, stream_chat

st.set_page_config(page_title="Assistant", layout="wide")
st.title("Local LLM chat")
st.caption(f"Model: {MODEL} (Ollama in Docker)")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "logs" not in st.session_state:
    st.session_state.logs = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("thinking"):
            with st.expander("Thinking"):
                st.markdown(message["thinking"])
        st.markdown(message["content"])

if prompt := st.chat_input("Say something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        thinking_slot = st.empty()
        answer_slot = st.empty()
        thinking_box = thinking_text = None
        thinking, reply = "", ""
        for kind, text in stream_chat(st.session_state.messages, st.session_state.logs):
            if kind == "thinking":
                if thinking_box is None:
                    thinking_box = thinking_slot.status("Thinking…", expanded=True)
                    thinking_text = thinking_box.empty()
                thinking += text
                thinking_text.markdown(thinking)
            else:
                if thinking_box is not None and not reply:
                    thinking_box.update(label="Thought", state="complete", expanded=False)
                reply += text
                answer_slot.markdown(reply)
        if thinking_box is not None and not reply:
            thinking_box.update(label="Thought", state="complete", expanded=False)
    st.session_state.messages.append({"role": "assistant", "content": reply, "thinking": thinking})

# Rendered last so the newest log entry is included; the sidebar still appears on the side.
with st.sidebar:
    st.header("Logs")
    if st.button("Clear logs"):
        st.session_state.logs.clear()
    if not st.session_state.logs:
        st.caption("No requests yet.")
    for i, entry in reversed(list(enumerate(st.session_state.logs, 1))):
        with st.expander(f"#{i} · {entry['time']}", expanded=(i == len(st.session_state.logs))):
            st.caption("Request")
            st.json(entry["request"], expanded=False)
            st.caption("Response")
            st.json(entry["response"], expanded=False)
            if entry["error"]:
                st.error(entry["error"])
