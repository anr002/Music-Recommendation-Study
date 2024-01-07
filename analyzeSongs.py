import librosa
import json
import os
from tqdm import tqdm

# Get a list of all the MP3 files
mp3_files = [f for f in os.listdir('Songs') if f.endswith('.mp3')]

songs = []

# Extract features from each MP3 file
for mp3_file in tqdm(mp3_files, desc="Processing songs", unit="song"):
    y, sr = librosa.load(os.path.join('Songs', mp3_file))

    # Extract the song name and artist name from the file name
    parts = mp3_file[:-4].split(' - ')
    if len(parts) == 2:
        song_name, artist_name = parts
    else:
        print(f"Unexpected filename format: {mp3_file}")
        continue

    # Compute the onset envelope
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    # Extract the tempo
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0]

    # Extract other features
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr).mean().item()
    spec_contrast = librosa.feature.spectral_contrast(y=y, sr=sr).mean().item()
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr).mean().item()

    # Add the song to the list
    songs.append({
        'song_name': song_name,
        'artist_name': artist_name,
        'tempo': tempo,
        'chroma_stft': chroma_stft,
        'spec_contrast': spec_contrast,
        'tonnetz': tonnetz,
    })

    # Convert the songs to JSON
    songs_json = json.dumps(songs, indent=4)

    # Write the JSON to a file
    with open('songs_features.json', 'w') as file:
        file.write(songs_json)