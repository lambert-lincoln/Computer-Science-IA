from APIkey import _ApiKey as AK
import streamlit as st
from back_end import BackEnd as BE
import pandas as pd


def initiate_chatbot(input: pd.DataFrame = None):

    st.title("🤖 Your Financial AI Mentor")

    be = BE()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    prompt = None

    # Display the entire chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if input is None:
        # Handle user input
        prompt = st.chat_input("Ask Your Financial AI Mentor Something")

    elif isinstance(input, pd.DataFrame):
        prompt = f'''
        # TASK
        You are to help me interpret this financial data which contains the variation in price and trading volume of the past 50 days. The following is the full dataframe
        
        ## COMPLETE DATAFRAME
        {input.iloc[-50:]}
        
        ## QUESTION
        How should I, as both a trader and an investor interpret the variation of prices and volume based on the following data?
        '''
        
    st.session_state.messages.append(
        {"role": "user", "content": prompt})

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
