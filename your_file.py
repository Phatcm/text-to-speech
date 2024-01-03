import streamlit as st
import requests
import json
from tts import aggreate_audio

def getFiles(name):
    response = requests.get("https://xqyl0erqka.execute-api.ap-northeast-1.amazonaws.com/prod", json = {"name":name})
    file_data = response.json()
    return file_data

# def listItems(file_names):
    

def app():
    st.header("Browse your files")
    name = st.text_input("What is your name?")
    
    colms = st.columns((1,4,2,2))
    fields = ["№", "Name", "UploadTime", "Download"]
    for col, field_name in zip(colms, fields):
        # header
        col.write(field_name)
    #if name exist then get all the file_name in dynamodb for this name
    #and display them in a list
    if name:
        file_data = getFiles(name)
        for i, file_info in enumerate(file_data):
            col1, col2, col3, col4 = st.columns((1,4,2,2))
            col1.write(i)
            col2.write(file_info['file_name'])
            col3.write(file_info['upload_time'])
            if col4.button("Download", key = i):
                api_base_url = "https://xqyl0erqka.execute-api.ap-northeast-1.amazonaws.com/prod"
                print(file_info['file_name'])
                download_url = "{}?download={}".format(api_base_url,file_info['file_name'])
                response = requests.get(download_url)
                if response.status_code == 200:
                    audio_urls = response.json()  # Assuming the response.text contains the audio URL
                
                    # Download the audio file and save it to `output.mp3`
                    aggreate_audio(audio_urls)
                    
                    # Play the audio file
                    with open("output.mp3", "rb") as f:
                        audio_file = f.read()
                        st.audio(audio_file, format='audio/mpeg')
                else:
                    st.write("Error")
                    st.write(response.text)
        