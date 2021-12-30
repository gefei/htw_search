import streamlit as st
import requests
import json

def show_results(response):
    for item in response.json():
        st.write(item['url'])

st.title("Mini Google")
with st.form(key="q"):
    search_text = st.text_input(label="Search term", value="Query")
    search_button = st.form_submit_button(label="Submit")

if search_button: 
    r = requests.post("http://localhost:8000/search/", data=json.dumps({'query': search_text}))
    if r.status_code == 200:
        st.text("received response")
        show_results(r)