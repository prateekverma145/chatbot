import streamlit as st
from streamlit_chat import message
import pathlib
import textwrap
import google.generativeai as genai

GOOGLE_API_KEY=st.secrets['GOOGLE_API_KEY'] #  use your api key in place of GOOGLE_API_KEY  
from IPython.display import Markdown
from IPython.display import display
import PIL.Image
st.set_page_config(layout="centered",page_icon='🤖',page_title="Chatbot")

st.markdown("<h1 style='text-align: center;'>Chatbot</h1>", unsafe_allow_html=True)
st.sidebar.subheader(" Select model :")
st.sidebar.write("1. Gemini-Pro  only for text search")
st.sidebar.write("2. Gemini-pro-vision  for image search")

md=st.sidebar.radio("select model",('Gemini-Pro','Gemini-pro-vision'))

# Used to securely store your API key

st.sidebar.markdown("<h4 style='text-align: right; color: red;'>Made by: Prateek Verma</h4>", unsafe_allow_html=True)
#st.sidebar.markdown("<h5 style='text-align: right; color: red;'>Powered by: Gemini</h5>", unsafe_allow_html=True)
generation_config=genai.types.GenerationConfig(
        # Only one candidate for now.
        candidate_count=1,
        max_output_tokens=800,
        )

if 'bot_history' not in st.session_state:
  st.session_state.bot_history={}


try:
  if(md=='Gemini-Pro'):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro',generation_config=generation_config)
    chat = model.start_chat(history=[])
    
    
  if(md=='Gemini-pro-vision'):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro-vision',generation_config=generation_config)
    chat = model.start_chat(history=[])
    path=st.file_uploader("Upload an image",type=['png','jpg','jpeg'])
    if(st.button("generate caption") and path is not None):
      img= PIL.Image.open(path)
      st.image(img)
      message(model.generate_content(img).text)
except:
  st.error("Some error occured")
    
if(md=='Gemini-Pro'):
  a=st.chat_input("Write a message")
  try:
    if(a):
      if a in st.session_state.bot_history:
        st.warning("You have already asked this question!!!!")
      if a not in st.session_state.bot_history:
        for i ,_ in st.session_state.bot_history.items():
          if(st.session_state.bot_history[i]!=""):
            message(key=f"chat_widget_{i}",message=i,is_user=True)
            message( key=f"chat_{i}",message=f"{st.session_state.bot_history[i]}",is_user=False)
        res=chat.send_message(a).text
        message(key=f"{a}",message=a,is_user=True)
        message( key=f"chat_{a}",message=res,is_user=False)
        st.session_state.bot_history[a]=res
  except:
    st.error("Some error occured")
      

  
  
    
 
  
  