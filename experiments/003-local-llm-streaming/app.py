import streamlit as st

from backend import MODEL, stream_chat

st.title("Local LLM chat")
st.caption(f"Model: {MODEL} (Ollama in Docker)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        reply = st.write_stream(stream_chat(st.session_state.messages))
    st.session_state.messages.append({"role": "assistant", "content": reply})
