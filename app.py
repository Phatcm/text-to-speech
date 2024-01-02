import streamlit as st
import requests
from moviepy.editor import concatenate_audioclips, AudioFileClip
import os
import time

def media_player(url):
    html = f"""
        <audio controls style="width: 100%;">
            <source src={url} type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    """
    st.markdown(html, unsafe_allow_html=True)
    
def app():
    st.markdown("<h1 style='text-align: center; color: red;'>My talking app</h1>", unsafe_allow_html=True)
    text = st.text_area("Input your text")
    st.write(f'You wrote {len(text)} characters.')
    
    if st.button("Let's speech"):
        response = requests.post("https://xqyl0erqka.execute-api.ap-northeast-1.amazonaws.com/prod", json = {"text":text})

        if response.status_code == 200:
            audio_urls = response.json()  # Assuming the response.text contains the audio URL
            st.write(audio_urls)

            audio_clips = []
            for url in audio_urls:
                audio_data = requests.get(url).content
                print("Downloaded")
                
                # Save the audio data to a temporary file
                with open('temp.mp3', 'wb') as f:
                    f.write(audio_data)
                    print("Saved")
                
                # Wait for the download to complete
                time.sleep(1)
                
                # Load the audio file with pydub
                audio = AudioFileClip('temp.mp3')
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
            
            with open("output.mp3", "rb") as f:
                st.audio(f.read(), format='audio/mp3')
        else:
            st.write("Error")
            st.write(response.text)
app()

