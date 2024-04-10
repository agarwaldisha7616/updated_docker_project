import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
import uuid
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)
from dotenv import load_dotenv
import os

load_dotenv()



output_parser = StrOutputParser()

openai_api_key = os.getenv("CONVERSATION_API")



history = StreamlitChatMessageHistory(key=openai_api_key)




st.title(":blue[Expert Code Solver]")


if len(history.messages) == 0:
    history.add_ai_message("How can I help you?")



prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert software engineer accross multiple fields. Your task is to recieve errors, and bad code and respond with a proposal for optimal code with an appended detailed explanation. If the question is irrelevant to software engineering, politely decline the request"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chain = prompt | ChatOpenAI(openai_api_key=openai_api_key,temperature=0.8) | output_parser


chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: history,  # Always return the instance created earlier
    input_messages_key="question",
    history_messages_key="history",
)

for msg in history.messages:
    st.chat_message(msg.type).write(msg.content)
    
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)

    # Generate a unique session ID
    session_id = str(uuid.uuid4())

    # Use the session ID in the configuration
    config = {"configurable": {"session_id": session_id}}
    response = chain_with_history.invoke({"question": prompt}, config)
    st.chat_message("ai").info(response)



