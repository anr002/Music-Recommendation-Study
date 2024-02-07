import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash
from pytube import YouTube

# Add the Tooling2 directory to the system path
tooling2_path = 'C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\Tooling2'
sys.path.append(tooling2_path)

from GetNewSongsWEB import download_video, convert_to_wav

app = Flask(__name__)
app.secret_key = os.urandom(16) 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the YouTube link from the form
        youtube_link = request.form['youtube_link']

        # Define the root folder where you want to save the .wav file, saving to different folder for cleanliness
        root_folder = 'C:\\Users\\andre\\Downloads\\GTZAN\\My_Audio\\WebInterface'
        
        # Use the download_video function to download the video and convert it to wav
        video_path = download_video(youtube_link, root_folder)
        
        # Get the title of the video for naming the file
        yt = YouTube(youtube_link)
        video_title = yt.title
        
        # Use the convert_to_wav function to convert the whole video
        wav_path = convert_to_wav(video_path, root_folder, video_title)
        
        if wav_path:
            flash('Song converted to WAV successfully!', 'success')
            #Placeholder for genre prediction model logic
            return redirect(url_for('results', wav_path=wav_path))
        else:
            flash('Failed to convert song.', 'error')
            return redirect(url_for('home'))
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')
        return redirect(url_for('home'))

@app.route('/results')
def results():
    snippet_path = request.args.get('snippet_path', None)
    return render_template('results.html', snippet_path=snippet_path)

if __name__ == '__main__':
    app.run(debug=True)