import json
import numpy as np

## I noticed that my method of obtaining lyrics is very buggy. I noticed it grabbing articles or something. They were very long so I wanted to test what songs fetched articles instead of lyrics.

# Load the JSON file
with open('songs_features.json', 'r') as file:
    songs = json.load(file)

# Calculate the length of lyrics for each song
lyrics_lengths = [len(song['lyrics']) for song in songs]

# Calculate the mean and standard deviation of lyrics length
mean_length = np.mean(lyrics_lengths)
std_length = np.std(lyrics_lengths)

# Define an outlier as a song with lyrics length more than 3 standard deviations from the mean
outlier_threshold = mean_length + 3 * std_length

# Find and print the songs with extremely long lyrics
outlier_songs = [song for song in songs if len(song['lyrics']) > outlier_threshold]

for song in outlier_songs:
    print(f"Song '{song['song_name']}' by {song['artist_name']} has extremely long lyrics.")