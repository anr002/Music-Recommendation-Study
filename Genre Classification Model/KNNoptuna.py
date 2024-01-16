import numpy as np
import pandas as pd
import optuna
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from tqdm import tqdm

# Load the preprocessed data
data_path = 'C:\\Users\\andre\\OneDrive\\Documents\\Data Science Projects\\Music Recommendations Study\\preprocessed_data.npz'
with np.load(data_path) as data:
    X_train = data['X_train']
    y_train = data['y_train']

def objective(trial):
    # Hyperparameters to be tuned
    n_neighbors = trial.suggest_int('n_neighbors', 1, 100)
    weights = trial.suggest_categorical('weights', ['uniform', 'distance'])
    p = trial.suggest_int('p', 1, 5)

    # Initialize the KNN classifier with the current hyperparameters
    knn = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights, p=p)

    # Perform cross-validation
    score = cross_val_score(knn, X_train, y_train, cv=5, scoring='accuracy').mean()
    return score

# Create a study object and specify the direction is 'maximize'.
study = optuna.create_study(direction='maximize')

# Wrap the study.optimize call with tqdm for a progress bar
tqdm_study = tqdm(total=10000, desc='Optimization Progress')
def callback(study, trial):
    tqdm_study.update(1)

study.optimize(objective, n_trials=10000, callbacks=[callback])

# Close the tqdm progress bar
tqdm_study.close()

# Best hyperparameters
best_trial = study.best_trial
print(f'Number of finished trials: {len(study.trials)}')
print(f'Best trial number: {best_trial.number}')
print(f'Best trial parameters: {best_trial.params}')