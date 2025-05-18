# %%
# Ensure the necessary libraries are installed
# !pip install langchain-google-genai streamlit --quiet
# (These installs are usually handled by the requirements.txt file in deployment)

import os
import streamlit as st
# from google.colab import userdata # Remove this if deploying outside Colab
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# --- Set your Google API Key ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    else:
        st.error("Google API Key not found in Streamlit Secrets.  Please add to secrets.toml or Streamlit secrets.")
        st.stop()
    if 'llm' not in st.session_state:
        st.session_state.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# --- Streamlit App ---
st.title("Gemini Chatbot")

# --- Chat History ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant.")]

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("human"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("ai"):
            st.markdown(message.content)

# --- User Input ---
if prompt := st.chat_input("Enter your prompt"):
    st.session_state.chat_history.append(HumanMessage(content=prompt))
    with st.chat_message("human"):
        st.markdown(prompt)

    try:
        response = st.session_state.llm.invoke(st.session_state.chat_history)
        st.session_state.chat_history.append(AIMessage(content=response.content))
        with st.chat_message("ai"):
            st.markdown(response.content)
    except Exception as e:
        st.error(f"Exception: {e}")

if st.button("Clear Chat"):
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant.")]
    st.experimental_rerun()
