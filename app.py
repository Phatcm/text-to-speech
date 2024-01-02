import streamlit as st
import requests
from moviepy.editor import concatenate_audioclips, AudioFileClip
import os
import time
import tempfile

def aggreate_audio(audio_urls):
    audio_clips = []
    for url in audio_urls:
        audio_data = requests.get(url).content
        print("Downloaded")
        
        # Create a unique temporary file for this iteration
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_file_name = temp_file.name

        # Save the audio data to the temporary file
        with open(temp_file_name, 'wb') as f:
            f.write(audio_data)
            print("Saved")
        # Load the audio file with pydub
        audio = AudioFileClip(temp_file_name)
        print("Loaded")

        # Add the audio clip to the list
        audio_clips.append(audio)
        

    # Merge the audio clip to the list
    merged_audio = concatenate_audioclips(audio_clips)
    print("Merged")
    

    merged_audio.write_audiofile("output.mp3")
    
    # Close the AudioFileClip objects
    for audio in audio_clips:
        audio.close()

def app():
    st.markdown("<h1 style='text-align: center; color: red;'>My talking app</h1>", unsafe_allow_html=True)
    
    # Text input for required name
    name = st.text_input("What is your name?")
    if name:
        text = st.text_area("Input your text")
        st.write(f'You wrote {len(text)} characters.')
        
        if st.button("Let's speech"):
            response = requests.post("https://xqyl0erqka.execute-api.ap-northeast-1.amazonaws.com/prod", json = {"text":text})

            if response.status_code == 200:
                audio_urls = response.json()  # Assuming the response.text contains the audio URL
                
                # Download the audio file and save it to `output.mp3`
                aggreate_audio(audio_urls)
                
                # Play the audio file
                with open("output.mp3", "rb") as f:
                    st.audio(f.read(), format='audio/mp3')
            else:
                st.write("Error")
                st.write(response.text)
app()

