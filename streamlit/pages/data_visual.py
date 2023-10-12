import streamlit as st
import pandas as pd
import pygwalker as pyg
import json

# Set page configuration
st.set_page_config(
    page_title="VidyaAI",
    page_icon=":snake:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Create a sidebar with a file upload widget
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# Load Data
#@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df
    else:
        return None

df = load_data(uploaded_file)

# Set title and subtitle
st.title('Vidya Vizualizer')

# Display PyGWalker
with open("design1.json","r") as data:
    data_f= data.read()

if df is not None:
    pyg.walk(df, env='Streamlit', dark='dark', spec=data)
else:
    st.warning("Upload a CSV file to visualize the data.")
