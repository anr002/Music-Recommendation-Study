import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import librosa
import os
import pickle
import sys

### In order to properly classify new songs, it is important to obtain the same data the GTZAN dataset gave which is what we used to train the classifier.

### Add a user input function that takes in if the provided prediction was correct or not. If correct continue and append data to the relevant  dataset section

# Load the genres list and genre_dict dictionary
try:
    with open('genres.pkl', 'rb') as f:
        genres = pickle.load(f)
    with open('genre_dict.pkl', 'rb') as f:
        genre_dict = pickle.load(f)
except FileNotFoundError:
    # If the files do not exist, initialize with the default values
    genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    genre_numbers = list(range(1, len(genres) + 1))
    genre_dict = dict(zip(genre_numbers, genres))

# Function to extract features from a song file
# Notice that the duration is 30 seconds. The GTZAN dataset provided data for a 3 second snippet and a 30 second snippet. The 30 second set was used for training
def extract_features(file_name):
    # Load the audio file
    y, sr = librosa.load(file_name, mono=True, duration=30)
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
    features = np.hstack((length, features))
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

# Load the existing dataset into a separate DataFrame
df_original = pd.read_csv('C:\\Users\\andre\\Downloads\\GTZAN\\Data\\features_30_secActive.csv')

# Create a copy of the DataFrame and drop the 'filename' column
df = df_original.copy()
df = df.drop('filename', axis=1)

# Load the trained scaler and KNN model
scaler = joblib.load('C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\Genre Classification\\Model\\scaler.pkl')  
knn_model = joblib.load('C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\Genre Classification\\Model\\knn_model.pkl')  
label_encoder = joblib.load('C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\Genre Classification\\Model\\label_encoder.pkl') 

# Path to  new song file
new_song_path = 'C:\\Users\\andre\\Downloads\\GTZAN\\My_Audio\\What You Know.wav'

# Extract the filename from the file path
new_song_filename = os.path.basename(new_song_path)

# Extract features from the new song
new_song_features = extract_features(new_song_path)

# Create a DataFrame with the same feature names as the training data
new_song_features_df = pd.DataFrame([new_song_features], columns=feature_names)

# Scale the features using the loaded scaler
new_song_features_scaled = scaler.transform(new_song_features_df)

# Predict the genre
predicted_genre_index = knn_model.predict(new_song_features_scaled)
predicted_genre = label_encoder.inverse_transform(predicted_genre_index)
# Calculate the confidence level
confidence_level = knn_model.predict_proba(new_song_features_scaled)

# Obtain confidence level of the predicted genre
predicted_genre_confidence = confidence_level[0][predicted_genre_index[0]]

print(f"The predicted genre of the song is: {predicted_genre[0]}")
print(f"The confidence level of the prediction is: {predicted_genre_confidence}\n")

# Print out the confidence levels for all genres
for i, genre in enumerate(label_encoder.classes_):
    print(f"The confidence level that the song is {genre} is: {confidence_level[0][i]}")

genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
genre_numbers = list(range(1, len(genres) + 1))
genre_dict = dict(zip(genre_numbers, genres))

# Ask for user feedback
feedback = input("Is the predicted genre correct? (yes/no/new/skip): ")

# Append the new data to your dataset
if feedback.lower() == 'yes':
    new_song_features_with_label = np.append(new_song_features, predicted_genre[0])
    new_data = pd.DataFrame(new_song_features_with_label.reshape(1, -1), columns=df.columns)
    new_data['filename'] = new_song_filename 
elif feedback.lower() == 'no':
    # Load the genres list and genre_dict dictionary again
    try:
        with open('genres.pkl', 'rb') as f:
            genres = pickle.load(f)
        with open('genre_dict.pkl', 'rb') as f:
            genre_dict = pickle.load(f)
    except FileNotFoundError:
        print("Error: genres.pkl or genre_dict.pkl not found.")
        sys.exit()

    print("Please enter the number corresponding to the correct genre:")
    for number, genre in genre_dict.items():
        print(f"{number}: {genre}")
    correct_genre_number = int(input())
    correct_genre = genre_dict[correct_genre_number]
    new_song_features_with_label = np.append(new_song_features, correct_genre)
    new_data = pd.DataFrame(new_song_features_with_label.reshape(1, -1), columns=df.columns)
    new_data['filename'] = new_song_filename 

elif feedback.lower() == 'new':
    new_genre = input("Please enter the new genre: ")
    if new_genre in genres:
        print("Error: This genre already exists.")
        sys.exit()
    new_song_features_with_label = np.append(new_song_features, new_genre)
    new_data = pd.DataFrame(new_song_features_with_label.reshape(1, -1), columns=df.columns)
    new_data['filename'] = new_song_filename 
    # Add the new genre to the genres list and update the genre_dict
    genres.append(new_genre)
    genre_numbers = list(range(1, len(genres) + 1))
    genre_dict = dict(zip(genre_numbers, genres))
    # Save the updated genres list and genre_dict dictionary
    with open('genres.pkl', 'wb') as f:
        pickle.dump(genres, f)
    with open('genre_dict.pkl', 'wb') as f:
        pickle.dump(genre_dict, f)
elif feedback.lower() == 'skip':
    print("Skipping data addition.")
else:
    print("Invalid feedback. Data will not be added.")

# Only append and save the data if the feedback is 'yes', 'no', or 'new'
if feedback.lower() in ['yes', 'no', 'new']:
    # Find the index where the new genre starts if it's not a new genre
    if feedback.lower() != 'new':
        start_index = df_original[df_original['label'] == new_data['label'].values[0]].index[0]
        # Split the DataFrame at the start index
        df1 = df_original.iloc[:start_index]
        df2 = df_original.iloc[start_index:]
        # Append new data to the first part of the DataFrame
        df1 = pd.concat([df1, new_data], ignore_index=True)
        # Concatenate the second part back to the DataFrame
        df_original = pd.concat([df1, df2], ignore_index=True)
    else:
        # If it's a new genre, append to the end
        df_original = pd.concat([df_original, new_data], ignore_index=True)

    # Save the updated dataset
    df_original.to_csv('C:\\Users\\andre\\Downloads\\GTZAN\\Data\\features_30_secActive.csv', index=False)