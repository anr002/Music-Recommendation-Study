import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from colorthief import ColorThief
from PIL import Image, ImageTk, ImageFilter
import io
from tkinter import ttk
import json
import time
import pandas as pd
import os


# Setup Spotify API
client_id = os.environ.get('SPOTIFY_CLIENT_ID')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
redirect_uri = 'https://github.com/anr002/'
scope = 'user-modify-playback-state user-library-read user-read-playback-state'

# Auth
auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)





# Retrieve all my liked songs
results = sp.current_user_saved_tracks()

liked_songs = []

# Iterate through the pages to retrieve all liked tracks
while results:
    for item in results['items']:
        track = item['track']
        time.sleep(0.5)  # Had to add a delay becaue of 429 error
        track_id = track['uri'].split(':')[-1]
        album_id = track['album']['uri'].split(':')[-1]
        artist_id = track['artists'][0]['uri'].split(':')[-1]
        #audio_features = sp.audio_features([track_id])[0]
        album = sp.album(album_id)
        artist = sp.artist(artist_id)
        # Storing data for studying later
        song_data = {
            "title": track['name'],
            "artist": track['artists'][0]['name'],
            "album": track['album']['name'],
            "uri": track['uri'],
            "release_year": album['release_date'].split('-')[0],
            "popularity": track['popularity'],
            "genre": artist['genres'],
        }
        #song_data.update(audio_features)
        liked_songs.append(song_data)
    if results['next']:
        results = sp.next(results)
    else:
        results = None


df = pd.DataFrame(liked_songs)

# Saving dataframe to JSON for later use.
df.to_json('liked_songs.json', orient='records', indent=4)