import streamlit as st
from APIkey import _ApiKey as AK
from zai import ZaiClient

api = AK()
ZAI_KEY = api.get_ZAI_key()

client = ZaiClient(api_key=ZAI_KEY)

response = client.chat.completions.create(
    model="glm-4.5-flash",
    messages=[
           {"role": "system", "content": "You are a helpful AI chatbot"},
            {"role": "user", "content": "test, test, does this work?"}
           ],
      thinking={
           "type": "enabled",
           },
      temperature=0.6,
      stream=True
      )

def content_stream():
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
            
st.write_stream(content_stream())
