import streamlit as st
import tempfile
from langchain.document_loaders import PyPDFLoader
import numpy as np
import os
import openai
import sys
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter,CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
persist_directory = 'docs/chroma/'
#!rm-rf./docs/chroma
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)


st.title("chat with pdf")
st.markdown("<h1 style='text-align: center; color: #d5d2d2;text-shadow: 2px 4px 5px #20201f;'>Chat with your PDF 📑📚 </h1>", unsafe_allow_html=True)
st.markdown(f"<style>.st-emotion-cache-6qob1r {{background-image: url('https://images.pexels.com/photos/6331040/pexels-photo-6331040.jpeg?auto=compress&cs=tinysrgb&w=800&lazy=load');background-size: cover; border: 5px solid #252222;border-radius:60px  }}</style>", unsafe_allow_html=True)

st.markdown(f"<style>.st-emotion-cache-1wrcr25  {{background-image: url('https://images.pexels.com/photos/2362009/pexels-photo-2362009.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2');background-size: cover; }}</style>", unsafe_allow_html=True)
    
file_uploader = st.sidebar.file_uploader("upload PDF",type = "pdf")

if file_uploader :
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file_uploader.getvalue())
        tmp_file_path = tmp_file.name
    
    print(tmp_file_path)
    loader = PyPDFLoader(file_path = str(tmp_file_path))
    pages = loader.load()
    
    c_splitter = CharacterTextSplitter(
      chunk_size = 50,
      chunk_overlap = 10,
      separator ="\n" ,
      length_function= len)
    docs = c_splitter.split_documents(pages)
    embedding = OpenAIEmbeddings(openai_api_key="sk-##OpenAI_apikey##")
    vectordb = Chroma.from_documents(
        documents= docs,
        embedding=embedding,
        persist_directory=persist_directory)

    
    
    def snap(query):
        
        question = query
        llm_chat = ChatOpenAI(openai_api_key="sk-########", openai_organization="org-JVzRB41h7wqZNEbW4DiJj4kC",model_name="gpt-3.5-turbo",temperature=0)
        retriever=vectordb.as_retriever()
        qa = ConversationalRetrievalChain.from_llm(
            llm_chat,
            retriever=retriever,
            memory=memory
            )
        result = qa({"question": question})
        return result['answer']
        
                          
    if "history" not in st.session_state:
        st.session_state["history"] = []
        
    if "generated" not in st.session_state:
        st.session_state["generated"] = ["Hello how can i help you"]
        
    if "past" not in st.session_state:
        st.session_state["past"] = ["Hey ! :wave: "]
    
    
    
    
    response_container = st.container()
    
    container = st.container()
    
    with container:
        #st.write("This is inside the container")
        with st.form(key = "my_form", clear_on_submit=True):
            user_input = st.text_input("Query:", placeholder = "talk with me", key = "input")
            submit_button = st.form_submit_button(label = "CHAT")
            
            
        if submit_button and user_input:
            output = snap(user_input)
            
            st.session_state["past"].append(user_input)
            st.session_state["generated"].append(output)
            
    if st.session_state["generated"] :
        with response_container:
            for i in range(len(st.session_state["generated"])):
                with st.chat_message(st.session_state["past"][i], avatar = "🍺"):
                    st.write(st.session_state["past"][i])
                
                with st.chat_message(st.session_state["generated"][i], avatar = "🤖"):
                    st.write(st.session_state["generated"][i])
                    
            
