from os import system
from time import sleep
import json

from _constants import *

from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from spotipy.exceptions import SpotifyException

from time import sleep
from os import getenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from math import ceil

jprint = lambda x: print(json.dumps(x, indent=4))

def _concurrent(fn, key, test=False, *args, **kwargs):
   return

def getArtist():
   return

def getArtists():
   return

def getAlbum():
   return

def getArtistAlbums():
   return

def getTrack():
   return

def getTracks():
   return _concurrent(getTrack, *args, **kwargs);

def getTrackAttr():
   return

def getTrackAttrs():
   return

##
# Youtube X Spotify
##
def SPFindYoutube():
   return
def YTFindSpotify():
   return


load_dotenv()
usr = getenv('usr')

auth = SpotifyOAuth(scope=SCOPE)#,open_browser=False, cache_path="./.cache.json")
sp   = Spotify(auth_manager=auth)

