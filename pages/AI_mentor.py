from APIkey import _ApiKey as AK
import streamlit as st
from back_end import BackEnd as BE
import pandas as pd


def initiate_chatbot():

    if st.session_state.show_chatbot == True:

        st.title("🤖 Your Financial AI Mentor")

        be = BE()

        if "messages" not in st.session_state:
            st.session_state.messages = []

        input = st.session_state.price_data

        # Display the entire chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if input is None:
            # Handle user input
            prompt = st.chat_input("Ask Your Financial AI Mentor Something")

        elif input is not None and not input.empty:
            prompt = f'''
            You are an expert financial mentor. A user is looking at a price chart for a stock and needs help interpreting the last 50 days of price and volume data.

            **Your Task:**
            Analyze the provided data and provide a clear, structured interpretation. Do not give financial advice. Focus on explaining what the data *means*.

            **Provide your analysis in these 4 sections:**
            1.  **Price Trend:** What is the overall direction of the stock price over this period (uptrend, downtrend, or sideways)?
            2.  **Volume Analysis:** How does the trading volume relate to significant price movements? Does high volume confirm the trend?
            3.  **Key Observations:** Point out 2-3 interesting patterns or events on the chart (e.g., a breakout on high volume, a period of consolidation).
            4.  **Questions for the User:** What are 2 important questions this data should make the user ask next (e.g., "What news caused that spike?", "Is this volume sustainable?").
            ** Data Analysis for the past 50 days **
            {input[['Close', 'Volume']].iloc[-50:].to_csv()}
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
