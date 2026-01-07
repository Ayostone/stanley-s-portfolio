from openai import OpenAI
import streamlit as st

# Sets browser tab title and icon and displays CHATBOT as the page heading
st.set_page_config(page_title="Streamlit Chat", page_icon=":speech_balloon:")
st.title("CHATBOT")

# Creates a client to communicate with OpenAI and reads your API key securely from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Stores the model name once per session and prevents re-initialization on every rerun
if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initializes the message history in the session state  
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful tool that talks like you are deeply in love with the user. Also make sure you ask for the users name before responding."}]

#Loops through stored messages and skips the system message (not shown to user) and renders chat bubbles for user & assistant
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accepts user input, appends it to message history, and displays it in a chat bubble            
if prompt := st.chat_input("Your question."):
    st.session_state.messages.append({"role": "user", "content": prompt})
   
    with st.chat_message("user"):
        st.markdown(prompt)
        
# Calls the OpenAI API with the message history and streams the response, displaying it in a chat bubble    
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})