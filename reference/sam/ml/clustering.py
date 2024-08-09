import typing
import pandas as pd

from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from dotenv import load_dotenv
from json import dump, dumps, load
from math import ceil
from os import getenv, system
from time import sleep

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy.exceptions import SpotifyException

from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

jprint = lambda x: print(dumps(x, indent=4))


#freezegun
load_dotenv('.env')
username = getenv('USR')

SCOPE = ",".join(
   [
   # Images
   "ugc-image-upload",
   # Listening History
   "user-read-recently-played",
   "user-read-playback-position",
   "user-top-read",
   # Playlists
   "playlist-modify-private",
   "playlist-read-collaborative",
   "playlist-read-private",
   "playlist-modify-public",
   # Playback
   "streaming",
   "app-remote-control",
   # Users
   "user-read-email",
   "user-read-private",
   # Follow
   "user-follow-read",
   "user-follow-modify",
   # Library
   "user-library-modify",
   "user-library-read",
   # Spotify Connect
   "user-read-currently-playing",
   "user-read-playback-state",
   "user-modify-playback-state",
   ]
)
auth = SpotifyOAuth(scope=SCOPE)#,open_browser=False, cache_path="./.cache.json")
sp   = Spotify(auth_manager=auth)


col_features = ['danceability', 'energy', 'valence', 'loudness']
X = MinMaxScaler().fit_transform(df[col_features])
kmeans = KMeans(init="kmeans++",
                n_clusters=2,
                random_state=15).fit(X)

df['kmeans'] = kmeans.labels_

#Separating the clusters into new variables
cluster_0 = df[df['kmeans']==0]
cluster_1  = df[df['kmeans']==1]

#Obtaining the ids of the songs and conver the id dataframe column to a list.
ids_0 = cluster_0['id'].tolist()
ids_1 = cluster_1['id'].tolist()

#Creating 2 new playlists on my Spotify User
pl_energy = sp.user_playlist_create(username=username,
                                           name="Radiohead :)")
pl_relaxed = sp.user_playlist_create(user=username,
                                            name="Radiohead :(")
#Adding the tracks into the playlists
#For energetic Playlist
sp.user_playlist_add_tracks(user=username,
                            playlist_id = pl_energy['id'],
                            tracks=ids_1)
#For relaxed Playlist
sp.user_playlist_add_tracks(user=username,
                            playlist_id = pl_relaxed['id'],
                            tracks=ids_0)