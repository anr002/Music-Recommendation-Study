from flask import Flask, render_template, request, redirect, url_for, flash
from pytube import YouTube
import numpy as np
# Ensure these imports are correctly pointing to where your functions and models are defined
from KNNWholeSong import predict_genre_from_path, scaler, knn_model, label_encoder
from GetNewSongsWEB import download_video, convert_to_wav
import os

app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route('/home')
def home():
    return render_template('home.html')  # Ensure you have a home.html template

@app.route('/predict', methods=['POST'])
def predict():
    try:
        youtube_link = request.form['youtube_link']
        root_folder = 'C:\\Users\\andre\\Downloads\\GTZAN\\My_Audio\\WebInterface'
        video_path = download_video(youtube_link, root_folder)
        yt = YouTube(youtube_link)
        video_title = yt.title
        # Assuming the artist's name is the first part of the video title
        artist_name = video_title.split('-')[0].strip() if '-' in video_title else 'Unknown Artist'
        thumbnail_url = yt.thumbnail_url
        wav_path = convert_to_wav(video_path, root_folder, video_title)
        
        if wav_path:
            flash('Song converted to WAV successfully!', 'success')
            predicted_genre, genre_confidence_averages = predict_genre_from_path(wav_path)
            # Extract artist name and song name from the video title
            artist_name, song_name = video_title.split(' - ', 1) if ' - ' in video_title else ('Unknown Artist', video_title)
            return render_template('results.html', predicted_genre=predicted_genre, confidences=genre_confidence_averages, artist_name=artist_name, song_name=song_name, thumbnail_url=yt.thumbnail_url)


        else:
            flash('Failed to convert song.', 'error')
            return redirect(url_for('home'))
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')
        return redirect(url_for('home'))

@app.route('/results')
def results():
    genre = request.args.get('genre', None)
    print(f"Genre received in results route: {genre}")  # Add this line for debugging
    return render_template('results.html', genre=genre)

if __name__ == '__main__':
    app.run(debug=True)