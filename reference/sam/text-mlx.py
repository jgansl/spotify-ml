import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from yellowbrick.regressor import PredictionError, ResidualsPlot
import mlx
import pandas as pd

# # Set up Spotipy with your Spotify API credentials
# SPOTIPY_CLIENT_ID = 'your_spotify_client_id'
# SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'

# os.environ['SPOTIPY_CLIENT_ID'] = SPOTIPY_CLIENT_ID
# os.environ['SPOTIPY_CLIENT_SECRET'] = SPOTIPY_CLIENT_SECRET

# sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
from _spotify import sp

# Function to get track features
def get_track_features(track_id):
    features = sp.audio_features(track_id)[0]
    return features

# Function to get track data
def get_track_data(track_ids):
    data = []
    for track_id in track_ids:
        features = get_track_features(track_id)
        track = sp.track(track_id)
        features['popularity'] = track['popularity']
        data.append(features)
    return pd.DataFrame(data)

# Example list of track IDs (you can add more)
track_ids = [
    '3n3Ppam7vgaVa1iaRUc9Lp', # Example track ID
    '0eGsygTp906u18L0Oimnem', # Example track ID
    # Add more track IDs here
]

# Get track data
track_data = get_track_data(track_ids)

# Select features for the model
features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
target = 'popularity'

X = track_data[features]
y = track_data[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build a machine learning model using MLX
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# # Use MLX to create a visual report (optional)
# report = mlx.Report(model, X_train, X_test, y_train, y_test)
# report.publish()

# Visualize prediction error
visualizer = PredictionError(model)
visualizer.fit(X_train, y_train)  # Fit the training data to the visualizer
visualizer.score(X_test, y_test)  # Evaluate the model on the test data
visualizer.show()  # Finalize and render the figure

# Visualize residuals
visualizer = ResidualsPlot(model)
visualizer.fit(X_train, y_train)  # Fit the training data to the visualizer
visualizer.score(X_test, y_test)  # Evaluate the model on the test data
visualizer.show()  # Finalize and render the figure