import os
from io import StringIO

import pandas as pd  # pip install pandas openpyxl
import requests
import streamlit as st
from streamlit_lottie import st_lottie


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_message = load_lottieurl(
    "https://assets10.lottiefiles.com/packages/lf20_uDilo5.json"
)

st.set_page_config(
    page_title="WhatsApp Chat Converter", page_icon=":calling:", layout="centered"
)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
    <style>
    /* Hide default Streamlit header and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 📂 Navigation", unsafe_allow_html=True)
    st.markdown("[▶️ **Watch Explanation Video**](https://youtu.be/i62VbGSI93A?si=sqh1qRZVSOEFRw-r)")
    st.markdown("[📺 YouTube Channel](https://youtube.com/@codingisfun)")
    st.markdown("[🌐 Website](https://pythonandvba.com)")
    st.markdown("[💼 LinkedIn](https://www.linkedin.com/in/sven-bosau/)")
    st.markdown("---")
    st.markdown("<div style='text-align:center; font-size:0.95em;'>Created with ❤️ by <a href='https://www.linkedin.com/in/sven-bosau/' target='_blank'>Sven Bosau</a></div>", unsafe_allow_html=True)


st_lottie(lottie_message, height=120, key="message")
st.title("Convert WhatsApp Chat history to CSV")
st.caption("Easily convert your exported WhatsApp chat to a clean CSV file for analysis.")

uploaded_file = st.file_uploader("Choose your WhatsApp history text file", type="txt")
if uploaded_file is None:
    st.stop()

# To read file as string:
data = StringIO(uploaded_file.getvalue().decode("utf-8"))
data = data.readlines()

# parse text, create list of lists structure & remove first whatsapp info message
dataset = data[1:]
cleaned_data = []
for line in dataset:
    # Check, whether it is a new line or not
    # If the following characters are in the line -> assumption it is NOT a new line
    if "/" in line and ":" in line and "," in line and "-" in line:
        # grab the info and cut it out
        date = line.split(",")[0]
        line2 = line[len(date) :]
        time = line2.split("-")[0][2:]
        line3 = line2[len(time) :]
        name = line3.split(":")[0][4:]
        line4 = line3[len(name) :]
        message = line4[6:-1]  # strip newline charactor
        cleaned_data.append([date, time, name, message])

    # else, assumption -> new line. Append new line to previous 'message'
    else:
        new = cleaned_data[-1][-1] + " " + line
        cleaned_data[-1][-1] = new

# Create the DataFrame
df = pd.DataFrame(cleaned_data, columns=["Date", "Time", "Name", "Message"])


@st.cache
def convert_df(df):
    # Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode("utf-8")


csv = convert_df(df)
st.download_button(
    label="Download CSV File",
    data=csv,
    file_name="WA_History.csv",
    mime="text/csv",
)
