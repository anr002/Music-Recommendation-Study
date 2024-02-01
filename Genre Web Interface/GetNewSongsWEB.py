from pytube import YouTube
from moviepy.editor import AudioFileClip
from pydub import AudioSegment
import os

# Define the root folder where you want to save the .wav file
root_folder = 'C:\\Users\\andre\\Downloads\\GTZAN\\My_Audio\\'

def download_video(url, target_folder):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    # Ensure the target folder exists
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    # Download the file to the target folder
    mp4_file_path = stream.download(output_path=target_folder)
    # Convert the mp4 file to wav
    wav_file_path = os.path.splitext(mp4_file_path)[0] + '.wav'
    audio_clip = AudioFileClip(mp4_file_path)
    audio_clip.write_audiofile(wav_file_path)
    audio_clip.close()
    # Delete the mp4 file
    os.remove(mp4_file_path)
    return wav_file_path

def convert_to_wav(filename, target_folder, start_time, end_time, title):
    # Define the new filename with the .wav extension
    new_filename = os.path.join(target_folder, title + '.wav')
    # Load the audio file
    audio_clip = AudioSegment.from_wav(filename)
    # Convert start_time and end_time to milliseconds
    start_time *= 1000
    end_time *= 1000
    # Extract the snippet
    snippet = audio_clip[start_time:end_time]
    # Save the snippet
    snippet.export(new_filename, format="wav")
