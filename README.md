# Spotify Music Prediction Model

## Overview
This project is focused on developing a machine learning model to predict songs that a user might like, using data from their Spotify liked songs. By analyzing various song attributes and user preferences, the model aims to provide personalized song recommendations.

## Features
- **Spotify API Integration**: Retrieves the user's liked songs and their attributes from Spotify.
- **Song Attributes Analysis**: Examines attributes like danceability, energy, key, loudness, etc., from user-liked songs.
- **User Interface**: A Tkinter-based GUI for rating songs and interacting with Spotify. GUI is really rough right now. Will use a different library later for a prettier one

## Machine Learning Algorithms
The project will explore a few different machine learning algorithms. Looking to take an ensemble learning approach. Looking to incorporate a reinforcement learning x KNN approach first.

### 1. **K-Nearest Neighbors (KNN)**
  - Easiest, less effective. Will test this first.
   - A simple algorithm that recommends songs similar to the ones the user already likes.
   - Effective for small datasets and provides a baseline for comparison with more complex models.

### 2. **Collaborative Filtering**
   - Utilizes the preferences of many users to predict the interests of a single user.

### 3. **Content-Based Filtering**
   - Makes predictions based on the similarity of song attributes.
   - Personalizes recommendations by learning the user's specific tastes.

### 4. **Deep Learning**
   - Potentially using neural networks to capture complex patterns in the data.

### 5. **Reinforcement Learning**
   - An advanced approach where the model learns to make better recommendations through trial and error.
   - Adapts to user feedback over time, refining its predictions based on user interactions.
   - Will utilize the thumbs up and thumbs down feature

