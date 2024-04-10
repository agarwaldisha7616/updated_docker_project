from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

output_parser = StrOutputParser()


st.title("We Transformed :red[Flawed Docker Scripts] to :blue[Prestine lines] 🐋")

openai_api_key = os.getenv("DOCKER_CHAT")

#api key pending
llm = ChatOpenAI(openai_api_key=openai_api_key,temperature=0.8)


with st.form('Docker Convo'):
    prompt = ChatPromptTemplate.from_messages([("system", "You are world class Docker Expert. and your duty is to write the correct the given docker script to the best version with commented explanation. If input is irrelevant to docker, politely decline the request"),("user", "{input}")])
    
    chain = prompt | llm | output_parser
    
    text: str = st.text_area('Enter your Docker script')
    
    submitted = st.form_submit_button('Improve Docker Script')
    
    if submitted:
        with st.spinner("Thinking... 🧠"): 
            response: str = chain.invoke({"input": text})
        st.info(response)
        
        
   