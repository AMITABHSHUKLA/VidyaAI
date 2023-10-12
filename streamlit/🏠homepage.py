import streamlit as st
from streamlit_option_menu import option_menu
import os
import openai
os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.getenv("OPENAI_API_KEY")

selected = option_menu(menu_title =None, options =["youtube", "app"], 
                        
                        icons=[ 'cloud-upload', "list-task"], 
                        menu_icon="cast", default_index=0, orientation="horizontal")

st.title(":black[HOMEPAGE]-")
p_content = st.sidebar.selectbox("Prompt",index = None, options = ("educational chatbot","script writer","python code explainer"))
role=st.sidebar.selectbox("ROLE",index = None, options = ("user","developer"))


st.markdown(f"<style>.st-emotion-cache-ffhzg2 {{background-image: url('https://images.pexels.com/photos/924824/pexels-photo-924824.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2');background-size: cover; border: 5px solid #252222;border-radius:60px  }}</style>", unsafe_allow_html=True)
st.markdown(f"<style>.st-emotion-cache-6qob1r   {{background-image: url('https://images.pexels.com/photos/5007442/pexels-photo-5007442.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2');background-size: cover; border: 5px solid #0a0828;border-radius:60px }}</style>", unsafe_allow_html=True)
st.markdown(f"<style>p  {{font-size: 28px; }}</style>", unsafe_allow_html=True)



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
        prompt = {}
        message = {}
        prompt["role"] = "system"
        prompt["content"] = p_content
        message["role"] = role
        message["content"] = user_input
        
        
        
            
            
    if submit_button and user_input:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                prompt,
                message,
              ],
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        
        output = response["choices"][0]["message"]["content"]
            
        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(output)
            
if st.session_state["generated"] :
    with response_container:
        for i in range(len(st.session_state["generated"])):
            with st.chat_message(st.session_state["past"][i], avatar = "🍺"):
                st.write(st.session_state["past"][i])
                
            with st.chat_message(st.session_state["generated"][i], avatar = "🤖"):
                st.write(st.session_state["generated"][i])    


if selected == "youtube":
    pass