# %%
# Ensure the necessary libraries are installed
# !pip install langchain-google-genai streamlit --quiet
# (These installs are usually handled by the requirements.txt file in deployment)

import os
import streamlit as st
# from google.colab import userdata # Remove this if deploying outside Colab
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# %%
# Set your Google API Key securely using Streamlit Secrets
# In your Streamlit Community Cloud dashboard, add a secret named GOOGLE_API_KEY
# with your actual API key as the value.
try:
    # Check if the secret exists before trying to access it
    if "GOOGLE_API_KEY" in st.secrets:
        os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    else:
        st.error("Google API Key not found in Streamlit Secrets.")
        st.stop() # Stop the app if API key is missing

    # Initialize the LLM - Do this only once using session state
    if 'llm' not in st.session_state:
        st.session_state.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

except Exception as e:
    st.error(f"Error setting up API key or LLM: {e}")
    st.stop() # Stop the Streamlit app if API key is not available

# Streamlit UI title
st.title("Conversational Chatbot with Gemini")

# Initialize chat history in Streamlit's session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_history.append(SystemMessage(content="You are a helpful assistant."))

# Display previous chat messages
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("human"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
         with st.chat_message("ai"):
            st.markdown(message.content)
    # Optionally display system messages
    # elif isinstance(message, SystemMessage):
    #     with st.chat_message("system"):
    #         st.markdown(message.content)


# Input field for the user's message
user_input = st.chat_input("Say something...")

# Process user input when provided
if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    with st.chat_message("human"):
        st.markdown(user_input)

    try:
        result = st.session_state.llm.invoke(st.session_state.chat_history)
        ai_response = result.content

        st.session_state.chat_history.append(AIMessage(content=ai_response))

        with st.chat_message("ai"):
            st.markdown(ai_response)

    except Exception as e:
        st.error(f"An error occurred while invoking the model: {e}")
        # Optionally, remove the last human message if the AI call failed
        # st.session_state.chat_history.pop()

# You can add a button to clear the chat history
if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.session_state.chat_history.append(SystemMessage(content="You are a helpful assistant."))
    st.experimental_rerun() # Rerun the app to clear the displayed messages
