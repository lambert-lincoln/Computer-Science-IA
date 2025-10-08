from APIkey import _ApiKey as AK
import streamlit as st
from back_end import BackEnd as BE


def show_ai_mentor_page ():
    
    st.title("🤖 Your Financial AI Mentor")

    be = BE()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the entire chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input("Ask Your Financial AI Mentor Something"):
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Stream Response
            for chunk in be.chatbot(st.session_state.messages):
                full_response += chunk
                message_placeholder.markdown(
                    full_response + "▌")  # Typing cursor effect

            message_placeholder.markdown(full_response)

        # Add the full assistant response to the history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})
