import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
import numpy as np
import os
import joblib

# Load the dataset
data_path = 'C:\\Users\\andre\\Downloads\\GTZAN\\Data\\features_30_sec.csv'
df = pd.read_csv(data_path)

# Explore the data
print(df.head())

# Preprocess the data
# Drop the filename as it's not a feature
df = df.drop('filename', axis=1)

# Encode the labels
label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['label'])

# Separate features and labels
X = df.drop('label', axis=1)
y = df['label']

# Normalize the features
scaler = StandardScaler()
X = scaler.fit_transform(X)



## The GTZAN dataset is split up into sections where the first 100 lines are blues the next 100 lines are classical and so on.
## It is important to keep this in mind when splitting because it does not make sense to split the bottom portion of the dataset as it wont be representative of the whole dataset.
## This requires a stratified split.


# Split the dataset into training and test sets, with stratification
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Initialize the KNN classifier with the optimized hyperparameters
knn = KNeighborsClassifier(n_neighbors=4, weights='distance', p=1)

# Train the classifier
knn.fit(X_train, y_train)

# Predict the test set results
y_pred = knn.predict(X_test)

# Evaluate the classifier
report = classification_report(y_test, y_pred, output_dict=True)

# Convert the report to a DataFrame
report_df = pd.DataFrame(report).transpose()

# Save the classification report to a CSV file
report_csv_path = 'C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\classification_report.csv'
report_df.to_csv(report_csv_path, index=True)

# Save the preprocessed data
preprocessed_data_path = 'C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\preprocessed_data.npz'
np.savez(preprocessed_data_path, X_train=X_train, y_train=y_train)


# Create a Model directory if it doesn't exist
model_dir = 'C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\Genre Classification\\Model'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# Save the KNN model
joblib.dump(knn, os.path.join(model_dir, 'knn_model.pkl'))

# Save the scaler
joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))

# Save the label encoder
joblib.dump(label_encoder, os.path.join(model_dir, 'label_encoder.pkl'))