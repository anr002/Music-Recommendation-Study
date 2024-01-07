# Music Recommendation Study

## Overview

This project is focused on developing a personalized music recommendation system. Initially, the project aimed to use Spotify's API to fetch song attributes and train machine learning models. However, due to Spotify's Terms of Service, which disallow training machine learning models with its API, the project had to pivot.

The current approach involves using the user's "Liked Songs" list from Spotify and retrieving the lyrics of these songs using the Genius API. Additionally, the project uses the Librosa library to analyze MP3 files of the liked songs and extract musical features. The lyrics and musical features are then analyzed to understand the user's preferences and recommend songs.

## Issues

During the development of this project, several issues were encountered, particularly with the Genius API used to fetch song lyrics. This API was not officially created by Genius, and it has several bugs. Despite efforts to fix these bugs, there are still instances where the API fetches incorrect information. This is an ongoing issue that is currently being addressed.


## Features

* **Genius API Integration**: Retrieves the lyrics of the user's liked songs from Spotify.
* **Librosa Analysis**: Analyzes the user's liked songs to extract musical features such as tempo, chroma_stft, spec_contrast, and tonnetz.
* **Lyrics Analysis**: Analyzes the lyrics of user-liked songs to extract features.
* **User Interface**: A Tkinter-based GUI for rating songs and interacting with Spotify. The GUI is currently in a rough state, and future plans include using a different library for a more user-friendly interface.

## Librosa Analysis

Librosa is a Python library for music and audio analysis. It provides the building blocks necessary to create music information retrieval systems. In this project, it is used to extract the following features from the MP3 files:

* **Tempo**: The speed or pace of a given piece of music.
* **Chroma_stft**: A representation of the audio that shows how the intensity of different pitches changes over time.
* **Spec_contrast**: The difference in amplitude between peaks and valleys in a sound spectrum.
* **Tonnetz**: A representation of harmonic relations between different pitches.

## Lyrics Analysis

The lyrics analysis involves several steps:

1. **Data Cleaning**: The lyrics data is cleaned to remove any unnecessary information and prepare it for analysis.
2. **Feature Extraction**: Various features are extracted from the lyrics using Natural Language Processing (NLP) techniques. These features include term frequency, sentiment, and others.
3. **Data Representation**: The extracted features are represented in various forms, such as word clouds and bar charts, to better understand the data.

## Future Work

The project is still in progress, and future work includes:

* **Improving the User Interface**: The current GUI will be improved for a better user experience.
* **Expanding the Lyrics Analysis**: More features will be extracted from the lyrics for a more comprehensive analysis.
* **Developing the Recommendation System**: The ultimate goal of the project is to develop a recommendation system that can suggest songs based on the user's preferences.
