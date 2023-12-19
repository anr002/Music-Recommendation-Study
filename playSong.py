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
import os

# Setup Spotify API
client_id = os.environ.get('SPOTIFY_CLIENT_ID')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
redirect_uri = 'https://github.com/anr002/'
scope = 'user-modify-playback-state user-library-read user-read-playback-state'

# Auth
auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

# UI Setup
root = tk.Tk()
root.title("Spotify Song Rating App")
root.geometry("800x500")  # Set a default size

selected_playlist_uri = tk.StringVar(root)  # Define selected_playlist_uri as a global variable

playlist_menu = None
playlist_info = {}
dropdown_menu = tk.Toplevel(root)
dropdown_menu.withdraw()




ratings = pd.DataFrame(columns=["title", "artist", "album", "rating", "image_url"])

song_progress = {}


def fetch_user_playlists():
    playlists = sp.current_user_playlists(limit=10)
    playlist_options = []
    playlist_info.clear() 
    for playlist in playlists['items']:
        playlist_name = playlist['name']
        playlist_uri = playlist['uri']
        playlist_image_url = playlist['images'][0]['url'] if playlist['images'] else None
        playlist_info[playlist_name] = {
            "uri": playlist_uri,
            "image_url": playlist_image_url
        }
        playlist_options.append(playlist_name)
    return playlist_options

def fetch_playlist_songs(playlist_uri):
    results = sp.playlist_tracks(playlist_uri)
    songs.clear()
    for item in results['items']:
        track = item['track']
        image_url = track['album']['images'][0]['url'] if track['album']['images'] else None
        songs.append({
            "title": track['name'],
            "artist": track['artists'][0]['name'],
            "album": track['album']['name'],
            "uri": track['uri'],
            "image_url": image_url
        })
    # Reseting the song index to show the first song
    global current_song_index
    current_song_index = 0
    show_song(current_song_index)

# Delay the first call to show song until after the UI is set up
def initial_song_display():
    if songs: 
        show_song(current_song_index)
    else:
        messagebox.showinfo("No Songs", "No songs available to display.")

# Trying to add functionality to select different test playlists later
def show_user_playlists():
    update_playlist_dropdown()  
    selected_playlist_uri.set("")  
    show_dropdown(None)  

# Function to show the dropdown menu. No need for pretty ui yet
def show_dropdown(event):
    dropdown_menu.geometry(f"+{root.winfo_rootx()+100}+{root.winfo_rooty()+100}")  # Adjust the coordinates as needed
    dropdown_menu.deiconify()


select_playlist_button = tk.Button(root, text="Select a Playlist", command=show_user_playlists, font=("Helvetica", 14))
select_playlist_button.pack()


select_playlist_button.bind("<Button-1>", show_dropdown)



# Function to hide the dropdown menu
def hide_dropdown():
    dropdown_menu.withdraw()

def on_playlist_selected(playlist_name):
    global selected_playlist_uri
    selected_playlist_uri.set(playlist_name)
    if playlist_name in playlist_info:
        playlist_uri = playlist_info[playlist_name]["uri"]
        fetch_playlist_songs(playlist_uri)

def update_playlist_dropdown():
    global dropdown_menu
    playlist_options = fetch_user_playlists()
    dropdown_menu.destroy()
    dropdown_menu = tk.Toplevel(root)
    dropdown_menu.withdraw()
    for option in playlist_options:
        frame = tk.Frame(dropdown_menu)
        frame.pack(fill="x")

        image_url = playlist_info[option]["image_url"]
        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(io.BytesIO(img_data))
        img.thumbnail((150, 150), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        label_image = tk.Label(frame, image=photo)
        label_image.image = photo 
        label_image.pack(side="left", padx=10)

        label_text = tk.Label(frame, text=option, font=("Helvetica", 14, "bold"), anchor="w")
        label_text.pack(side="left", fill="x", expand=True)

        frame.bind("<Button-1>", lambda event, playlist=option: on_playlist_selected(playlist))
        label_image.bind("<Button-1>", lambda event, playlist=option: on_playlist_selected(playlist))
        label_text.bind("<Button-1>", lambda event, playlist=option: on_playlist_selected(playlist))

def update_progress_bar():
    try:
        playback_info = sp.current_playback()
        if playback_info and playback_info['is_playing']:
            current_position = playback_info['progress_ms']
            total_duration = playback_info['item']['duration_ms']
            
            song_progress['value'] = (current_position / total_duration) * 100

            current_time_label['text'] = f"Current Time: {current_position / 1000:.0f} s"
            total_duration_label['text'] = f"Total Duration: {total_duration / 1000:.0f} s"
            
            root.after(1000, update_progress_bar)
        else:
            song_progress['value'] = 0
            current_time_label['text'] = "Current Time: 0.00 s"
            total_duration_label['text'] = "Total Duration: 0.00 s"
    except spotipy.exceptions.SpotifyException as e:
        print(f"An error occurred: {e}")


update_playlist_dropdown()

def fetch_songs():
    results = sp.current_user_saved_tracks(limit=10)  # Limit to N songs
    songs = []
    for item in results['items']:
        track = item['track']
        image_url = track['album']['images'][0]['url'] if track['album']['images'] else None
        songs.append({
            "title": track['name'],
            "artist": track['artists'][0]['name'],
            "album": track['album']['name'],
            "uri": track['uri'],
            "image_url": image_url
        })
    return songs

def skip_song():
    global current_song_index, ratings
    track_id = songs[current_song_index]['uri'].split(':')[-1]
    #audio_features = sp.audio_features([track_id])[0] # NEED TO FIX 429 CAUSED BY AUDIO FEATURES
    song = songs[current_song_index]
    #song.update(audio_features) # NEED TO FIX 429 CAUSED BY AUDIO FEATURES
    song["rating"] = "Skipped"
    song_df = pd.DataFrame([song]) 
    ratings = pd.concat([ratings, song_df], ignore_index=True) 
    
    sp.next_track()
    current_song_index += 1
    save_ratings()
    if current_song_index < len(songs):
        show_song(current_song_index)
    else:
        messagebox.showinfo("End", "No more songs to play.")


        

songs = fetch_songs()
current_song_index = 0
current_playlist_uri = None  


def play_song(uri):
    sp.start_playback(uris=[uri])

def rate_song(rating):
    global current_song_index, ratings
    track_id = songs[current_song_index]['uri'].split(':')[-1]
    #audio_features = sp.audio_features([track_id])[0]   # NEED TO FIX 429 CAUSED BY AUDIO FEATURES
    song = songs[current_song_index]
    #song.update(audio_features)  # NEED TO FIX 429 CAUSED BY AUDIO FEATURES
    song["rating"] = rating
    song_df = pd.DataFrame([song]) 
    ratings = pd.concat([ratings, song_df], ignore_index=True) 
    current_song_index += 1
    if current_song_index < len(songs):
        show_song(current_song_index)
    else:
        messagebox.showinfo("End", "No more songs to rate.")
        save_ratings()

def show_song(index):
    global album_art_label, current_image_url, songs, playlist_menu 
    if songs and 0 <= index < len(songs):
        song = songs[index]
        song_label.config(text=f"{song['title']} by {song['artist']} ({song['album']})")

        if song['image_url']:
            current_image_url = song['image_url']
            response = requests.get(song['image_url'])
            img_data = response.content
            img = Image.open(io.BytesIO(img_data))
            img.thumbnail((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            album_art_label.config(image=photo)
            album_art_label.image = photo  

            temp_path = 'temp_album_art.jpg'
            with open(temp_path, 'wb') as f:
                f.write(img_data)

            dominant_color = get_dominant_color(temp_path)
            blurred_bg = create_blurred_background(temp_path)

            if blurred_bg:
                root.config(background='#%02x%02x%02x' % dominant_color)
                background_label.config(image=blurred_bg)
                background_label.image = blurred_bg

            play_song(song['uri'])
    else:
        messagebox.showinfo("No Songs", "No songs available to display.")

def save_ratings():
    with open("song_ratings.json", "w") as f:
        json.dump(ratings.to_dict(orient="records"), f, indent=4)

def close_app():
    save_ratings()
    root.destroy()

track_id = songs[current_song_index]['uri'].split(':')[-1] 
#s = sp.audio_features([track_id])[0]  

def get_dominant_color(image_path):
    color_thief = ColorThief(image_path)
   
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color

# Function to create a blurred background image
def create_blurred_background(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            img = Image.open(image_file)
            img = img.resize((root.winfo_width(), root.winfo_height()), Image.Resampling.LANCZOS)
            img = img.filter(ImageFilter.GaussianBlur(radius=20))  
            return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error creating blurred background: {e}")
        return None

def open_playlist_menu():
    dropdown_menu.place(x=10, y=80)  

save_ratings()

select_playlist_button = tk.Button(root, text="Select a Playlist", command=show_user_playlists, font=("Helvetica", 14))
select_playlist_button.pack()


select_playlist_button.bind("<Button-1>", show_dropdown)

background_label = tk.Label(root)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

button_style = {'font': ('Helvetica', 12), 'bg': '#4CAF50', 'fg': 'white'}

song_label = tk.Label(root, text="", font=("Helvetica", 16))
song_label.pack(pady=10)

song_progress = ttk.Progressbar(root, orient='horizontal', length=200, mode='determinate')
song_progress.pack(pady=20)

album_art_label = tk.Label(root)
album_art_label.pack(pady=10)

thumbs_up_button = tk.Button(root, text="Thumbs Up", command=lambda: rate_song("Thumbs Up"), **button_style)
thumbs_up_button.pack(side=tk.LEFT, padx=10)

thumbs_down_button = tk.Button(root, text="Thumbs Down", command=lambda: rate_song("Thumbs Down"), **button_style)
thumbs_down_button.pack(side=tk.RIGHT, padx=10)

close_button = tk.Button(root, text="Close", command=close_app, font=('Helvetica', 12), bg='#f44336', fg='white')
close_button.pack(pady=20)

select_playlist_button = tk.Button(root, text="Select a Playlist", command=show_user_playlists, font=("Helvetica", 14))
select_playlist_button.pack()

current_time_label = tk.Label(root, text="", font=("Helvetica", 12))
current_time_label.pack()

total_duration_label = tk.Label(root, text="", font=("Helvetica", 12))
total_duration_label.pack()

skip_song_button = tk.Button(root, text="Skip Song", command=skip_song, font=("Helvetica", 12))
skip_song_button.pack()

update_progress_bar()

root.after(100, initial_song_display)

root.mainloop()