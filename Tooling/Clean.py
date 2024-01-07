import re
import json

def clean_lyrics(lyrics):
    cleaned_lyrics = re.sub(r'\d+ Contributors.*Lyrics', '', lyrics)
    cleaned_lyrics = re.sub(r'\d+Embed$', '', cleaned_lyrics)
    cleaned_lyrics = cleaned_lyrics.encode('ascii', 'ignore').decode()
    return cleaned_lyrics.strip()

# Load the JSON file
with open('songs_features.json', 'r') as file:
    songs = json.load(file)

# Clean the lyrics for each song
for song in songs:
    song['lyrics'] = clean_lyrics(song['lyrics'])

# Save the cleaned data back to the JSON file
with open('songs_features.json', 'w') as file:
    json.dump(songs, file, indent=4)