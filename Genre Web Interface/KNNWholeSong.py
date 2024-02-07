import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import librosa
import os
import pickle
import sys
from scipy.stats import mode


### In order to properly classify new songs, it is important to obtain the same data the GTZAN dataset gave which is what we used to train the classifier.

### Add a user input function that takes in if the provided prediction was correct or not. If correct continue and append data to the relevant  dataset section



# Function to extract features from a song file
# Notice that the duration is 30 seconds. The GTZAN dataset provided data for a 3 second snippet and a 30 second snippet. The 30 second set was used for training
def extract_features_song(file_name):
    y, sr = librosa.load(file_name, mono=True)
    song_length = librosa.get_duration(y=y, sr=sr)
    
    features_list = []
    
    for start in np.arange(0, song_length, 30):
        end = start + 30
        if end > song_length:
            end = song_length
        y_snippet = y[int(start*sr):int(end*sr)]
        
        snippet_features = extract_features_snippet(y_snippet, sr)
        features_list.append(snippet_features)
    
    return np.array(features_list)

def extract_features_snippet(y, sr):
    # Your existing feature extraction logic here, applied to y, sr
    # This should return the extracted features for the snippet
    length = len(y) / sr  # Calculate the length in seconds
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    
    # Calculate the various features
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
    harmony = np.mean(y_harmonic)
    perceptr = np.mean(y_percussive)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    
    # Aggregate the mean and variance of each feature
    features = np.hstack((
        length,
        np.mean(chroma_stft),
        np.var(chroma_stft),
        np.mean(rms),
        np.var(rms),
        np.mean(spectral_centroid),
        np.var(spectral_centroid),
        np.mean(spectral_bandwidth),
        np.var(spectral_bandwidth),
        np.mean(rolloff),
        np.var(rolloff),
        np.mean(zero_crossing_rate),
        np.var(zero_crossing_rate),
        harmony,
        np.var(y_harmonic),
        perceptr,
        np.var(y_percussive),
        tempo
    ))
    
    # Append the mean and variance of each MFCC
    for e in mfcc:
        features = np.hstack((features, np.mean(e), np.var(e)))
    
    return features

# Define the feature names as they were in the training data
feature_names = [
    'length', 'chroma_stft_mean', 'chroma_stft_var', 'rms_mean', 'rms_var',
    'spectral_centroid_mean', 'spectral_centroid_var', 'spectral_bandwidth_mean',
    'spectral_bandwidth_var', 'rolloff_mean', 'rolloff_var',
    'zero_crossing_rate_mean', 'zero_crossing_rate_var', 'harmony_mean',
    'harmony_var', 'perceptr_mean', 'perceptr_var', 'tempo'
]

# Append the mean and variance of each MFCC (20 MFCCs total)
for i in range(1, 21):
    feature_names.append(f'mfcc{i}_mean')
    feature_names.append(f'mfcc{i}_var')

def predict_genre_from_path(song_path):
    # Use the provided song_path to extract features
    new_song_features = extract_features_song(song_path)

    # Initialize a dictionary to store the sum of confidence levels for each genre
    genre_confidences_sum = {genre: [] for genre in label_encoder.classes_}

    # Iterate over each snippet's features
    for features in new_song_features:
        features_df = pd.DataFrame([features], columns=feature_names)
        scaled_features = scaler.transform(features_df)
        
        # Get confidence levels for the current snippet
        snippet_confidences = knn_model.predict_proba(scaled_features)[0]
        
        # Sum the confidence levels for each genre
        for i, genre in enumerate(label_encoder.classes_):
            genre_confidences_sum[genre].append(snippet_confidences[i])

    # Calculate the average confidence level for each genre
    genre_confidence_averages = {genre: np.mean(confidences) for genre, confidences in genre_confidences_sum.items()}

    # Find the genre with the highest average confidence level
    predicted_genre = max(genre_confidence_averages, key=genre_confidence_averages.get)

    print(f"Predicted Genre: {predicted_genre}")  # Optional: Print the predicted genre for debugging
    return predicted_genre, genre_confidence_averages

# Load the existing dataset into a separate DataFrame
df_original = pd.read_csv('C:\\Users\\andre\\Downloads\\GTZAN\\Data\\features_30_secActive.csv')

# Create a copy of the DataFrame and drop the 'filename' column
df = df_original.copy()
df = df.drop('filename', axis=1)

# Load the trained scaler and KNN model
scaler = joblib.load('C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\Genre Classification\\Model\\scaler.pkl')  
knn_model = joblib.load('C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\Genre Classification\\Model\\knn_model.pkl')  
label_encoder = joblib.load('C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\Genre Classification\\Model\\label_encoder.pkl') 

