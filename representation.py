import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn

# Load the JSON file
with open('songs_features.json', 'r') as file:
    songs = json.load(file)

# Extract the lyrics
lyrics = [song['lyrics'] for song in songs]

# Combine all lyrics into a single string
all_lyrics = ' '.join(lyrics)

# Generate the word cloud with increased resolution
wordcloud = WordCloud(width=800, height=400).generate(all_lyrics)

# Display the word cloud
plt.figure(figsize=(10, 5))  # Increase the size of the displayed figure
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# Save the figure to a file with increased dpi
plt.savefig('wordcloud.png', dpi=300)

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
import seaborn as sns

vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(lyrics)
word_freq_df = pd.DataFrame({'term': vectorizer.get_feature_names_out(), 'occurrences':np.asarray(X.sum(axis=0)).ravel().tolist()})
word_freq_df['frequency'] = word_freq_df['occurrences']/np.sum(word_freq_df['occurrences'])

# Plotting the top 10 most frequent words
top_words = word_freq_df.sort_values('frequency', ascending=False).head(10)
plt.figure(figsize=(12,6))
sns.barplot(x='term', y='frequency', data=top_words)
plt.show()


word_lengths = [len(w) for w in all_lyrics.split()]
plt.hist(word_lengths, bins=range(1, max(word_lengths)))
plt.show()

import nltk
import matplotlib.pyplot as plt

tokens = nltk.word_tokenize(all_lyrics)
pos_tags = nltk.pos_tag(tokens)
pos_counts = nltk.FreqDist(tag for (word, tag) in pos_tags)

# Get the 10 most common tags and their counts
common_tags = pos_counts.most_common(10)
tags, counts = zip(*common_tags)

# Create a pie chart
plt.pie(counts, labels=tags, autopct='%1.1f%%')
plt.title('Top 10 Part-of-Speech tags')
plt.show()
