import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash
from pytube import YouTube

# Add the Tooling2 directory to the system path
tooling2_path = 'C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\Tooling2'
sys.path.append(tooling2_path)

from GetNewSongsWEB import download_video, convert_to_wav

app = Flask(__name__)
app.secret_key = 'H@l!3rocks!'  # Replace with your actual secret key

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the YouTube link from the form
        youtube_link = request.form['youtube_link']
        # Get the start and end times from the form
        start_time = int(request.form['start_time'])
        end_time = int(request.form['end_time'])

        # Define the root folder where you want to save the .wav file
        root_folder = 'C:\\Users\\andre\\Downloads\\GTZAN\\My_Audio\\'
        
        # Use the download_video function to download the video and convert it to wav
        video_path = download_video(youtube_link, root_folder)
        
        # Get the title of the video for naming the snippet
        yt = YouTube(youtube_link)
        video_title = yt.title
        
        # Use the convert_to_wav function to create a snippet
        snippet_path = convert_to_wav(video_path, root_folder, start_time, end_time, video_title)
        
        if snippet_path:
            flash('Snippet created successfully!', 'success')
            return redirect(url_for('results', snippet_path=snippet_path))
        else:
            flash('Failed to create snippet.', 'error')
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