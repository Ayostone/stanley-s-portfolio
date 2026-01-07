from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#
st.set_page_config(page_title="Darwin — Sarcastic Chatbot")
st.title("Darwin — Sarcastic Chatbot")
#
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
#
col1, col2 = st.columns([9,1])
#
with col1:
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("You:")
        submit = st.form_submit_button("Send")

with col2:
    if st.button("Clear"):
        st.session_state.chat_history = []

if submit and user_input:
    st.session_state.chat_history.append({"role":"user","content":user_input})
    messages = [
        {"role":"system","content":"You are darwin, a chatbot that politely answers questions in a sarcastic manner."}
    ] + st.session_state.chat_history

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    reply = completion.choices[0].message.content
    st.session_state.chat_history.append({"role":"assistant","content":reply})

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Darwin:** {msg['content']}")
