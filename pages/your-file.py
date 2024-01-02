import streamlit as st
import requests
import json

def getFiles(name):
    response = requests.get("https://xqyl0erqka.execute-api.ap-northeast-1.amazonaws.com/prod", json = {"name":name})
    file_names = response.json()
    return file_names

# def listItems(file_names):
    

def app():
    st.header("Browse your files")
    name = st.text_input("What is your name?")
    
    colms = st.columns((1,4,1))
    fields = ["№", 'Name', "Download"]
    for col, field_name in zip(colms, fields):
        # header
        col.write(field_name)
    #if name exist then get all the file_name in dynamodb for this name
    #and display them in a list
    if name:
        file_names = getFiles(name)
        for i, file_name in enumerate(file_names):
            col1, col2, col3 = st.columns((1,4,1))
            col1.write(i)
            col2.write(file_name)
            if col3.button("Download", key = i):
                api_base_url = "https://xqyl0erqka.execute-api.ap-northeast-1.amazonaws.com/prod"
                download_url = "{}?download={}".format(api_base_url, file_name)
                response = requests.get(download_url)
                if response.status_code == 200:
                    st.write(response.text)
                else:
                    st.write("Error")
                    st.write(response.text)
        
app()