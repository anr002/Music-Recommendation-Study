import json
import lyricsgenius
import time
import os
import requests
import re, string

# STRING STUFF
def remove_punctuation(s):
    no_punc = str.maketrans('', '', string.punctuation)
    return s.translate(no_punc)

def remove_extra_spaces(s):
    return ' '.join(s.split())

def remove_apostrophe(s):
    return s.replace('’', '')

def replace_apostrophe(s):
    return s.replace('’', "'")

def remove_zero_width_space(s):
    return s.replace('\u200b', '')

def remove_right_to_left_mark(s):
    return s.replace('\u200f', '')

def scrub_string(s):
    s = remove_zero_width_space(s)
    s = remove_right_to_left_mark(s)
    s = remove_apostrophe(s)
    s = remove_extra_spaces(s)
    return s

def clean_line(s):
    s = remove_extra_spaces(s)
    s = replace_apostrophe(s)
    s = remove_zero_width_space(s)
    s = remove_right_to_left_mark(s)
    return s

# Get the Genius API token from an environment variable
genius_api_token = os.getenv('GENIUS_API_TOKEN')

# Initialize the Genius API client
genius = lyricsgenius.Genius(genius_api_token, remove_section_headers=True)

# Load the JSON file
with open('songs_features.json', 'r') as file:
    songs = json.load(file)

# Fetch the lyrics for each song
for song in songs:
    # Skip the song if it already has lyrics
    #if 'lyrics' in song and song['lyrics']:
    #    continue

    song_name = song['song_name']
    artist_name = song['artist_name']

    # Retry the request up to 3 times in case of a timeout
    for _ in range(3):
        try:
            genius_song = genius.search_song(song_name, artist_name)
            if genius_song is not None:
                song['lyrics'] = clean_line(genius_song.lyrics)
            else:
                print(f"Couldn't fetch lyrics for {song_name} by {artist_name}")
                song['lyrics'] = ""
            break
        except requests.exceptions.Timeout:
            print(f"Request timed out for {song_name} by {artist_name}, retrying...")

    with open('songs_features.json', 'w') as file:
        json.dump(songs, file, indent=4)

    time.sleep(1)