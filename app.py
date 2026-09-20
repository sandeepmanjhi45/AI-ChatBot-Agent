
import streamlit as st
from langchain_groq import ChatGroq

st.title("🤖 The Groq Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    user_api_key = st.text_input("Groq API Key:", type="password")

    persona = st.text_area(
        "System Prompt:",
        value="You are a helpful assistant."
    )

    if st.button("Reset Chat & Apply Persona"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Say something to the AI..."):

    if not user_api_key:
        st.error("Please enter your API key first!")

    else:
        st.session_state.messages.append({
            "role": "user",
            "content": user_query
        })

        with st.chat_message("user"):
            st.markdown(user_query)

        llm = ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0.7,
            api_key=user_api_key
        )

        messages_for_llm = [
            {
                "role": "system",
                "content": persona
            }
        ] + st.session_state.messages

        with st.spinner("AI is thinking..."):
            response = llm.invoke(messages_for_llm)
            bot_answer = response.content

        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_answer
        })

        with st.chat_message("assistant"):
            st.markdown(bot_answer)
