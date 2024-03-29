import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import librosa

### In order to properly classify new songs, it is important to obtain the same data the GTZAN dataset gave which is what we used to train the classifier.


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

# Load the trained scaler and KNN model
scaler = joblib.load('C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\Genre Classification\\Model\\scaler.pkl')  
knn_model = joblib.load('C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\Genre Classification\\Model\\knn_model.pkl')  
label_encoder = joblib.load('C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\Genre Classification\\Model\\label_encoder.pkl') 

# Path to the new song file
new_song_path = 'C:\\Users\\andre\\Downloads\\GTZAN\\My_Audio\\50_Cent_In_Da_Club.wav'  

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
print(f"The confidence level of the prediction is: {predicted_genre_confidence}")
