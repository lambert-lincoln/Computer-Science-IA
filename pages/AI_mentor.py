import streamlit as st
from back_end import BackEnd as BE

st.title("🤖 Your Financial AI Mentor")

be = BE()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Displays chat in history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
# User input handling
if input := st.chat_input("Ask something"):
    st.session_state.messages.append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.markdown(input)

    # Streaming response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in be.chatbot(st.session_state.messages):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
