# Music Recommendation Study

## Overview

This project is focused on developing a personalized music recommendation system. Initially, the project aimed to use Spotify's API to fetch song attributes and train machine learning models. However, due to Spotify's Terms of Service, which disallow training machine learning models with its API, the project had to pivot.

The current approach involves using the user's "Liked Songs" list from Youtube Music and retrieving the lyrics of these songs using the Genius API. Additionally, the project uses the Librosa library to analyze MP3 files of the liked songs and extract musical features. The lyrics and musical features are then analyzed to understand the user's preferences and recommend songs.

## Issues

During the development of this project, several issues were encountered, particularly with the Genius API used to fetch song lyrics. This API was not officially created by Genius, and it has several bugs. Despite efforts to fix these bugs, there are still instances where the API fetches incorrect information. This is an ongoing issue that is currently being addressed. I am actively researching an alternate library

## Genre Classification as a Stepping Stone

Before diving into personalized song recommendations, we are tackling the challenge of classifying songs by genre. This is a crucial step that will help in understanding the underlying patterns in music that resonate with listeners' preferences. To achieve this, we are leveraging the GTZAN Dataset, a renowned dataset in the music information retrieval field.

### The GTZAN Dataset

The GTZAN dataset is the most-used public dataset for evaluation in machine listening research for music genre recognition (MGR). It contains 1000 audio tracks each 30 seconds long. It contains 10 genres, each represented by 100 tracks. The tracks are all 22050Hz Mono 16-bit audio files in .wav format.

The dataset was collected in 2000-2001 from a variety of sources including personal CDs, radio, and microphone recordings, to represent a variety of recording conditions. This diversity in the dataset challenges our model to be robust and accurate across different recording qualities and environments.

# Genre Classification Progress
## Quantitative Assessment of Model Improvements

The genre classification model's performance was significantly enhanced through stratified data splitting and hyperparameter tuning. The GTZAN dataset's structure, with genres arranged sequentially, necessitated a stratified approach to ensure balanced representation in training and test sets.

### Performance Gains from Stratification

The introduction of stratified splitting led to a substantial increase in model accuracy. Specifically, the accuracy improved by 6.15% from 64.5% to 68.5%. The macro average precision, recall, and F1-score also saw improvements, indicating a more balanced performance across genres.

### Further Improvements with Hyperparameter Tuning

After applying hyperparameter tuning on top of the stratified dataset, the accuracy saw an additional increase of 0.5%, reaching 69%. The macro average F1-score improved, reflecting a more nuanced understanding of genre classification by the model.

### Genre-Specific Insights

The improvements in precision, recall, and F1-score across genres revealed that some genres are inherently more challenging to classify than others. For example, the F1-score for certain genres increased more significantly, suggesting that the model became better at balancing precision and recall for those genres after stratification and hyperparameter tuning.

In conclusion, the combined effect of stratified splitting and hyperparameter tuning has led to a more accurate and reliable genre classification model. These steps have been instrumental in achieving a 6.65% overall increase in accuracy, along with consistent improvements across other key performance metrics.

# Cont. Overview of Overall Study

## Features

* **Genius API Integration**: Retrieves the lyrics of the user's liked songs from Youtube Music.
* **Librosa Analysis**: Analyzes the user's liked songs to extract musical features such as tempo, chroma_stft, spec_contrast, and tonnetz.
* **Lyrics Analysis**: Analyzes the lyrics of user-liked songs to extract features.
* **User Interface**: A Tkinter-based GUI for rating songs and interacting with Spotify to play songs. The GUI is currently in a rough state, and future plans include using a different library for a more user-friendly interface.

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
