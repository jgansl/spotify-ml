ARTIST   = 'artist'
PLAYLIST = 'playlist'
SAVED    = 'saved'
TRACK    = 'track'
USER     = 'user'


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

SPOTIFY_WEEKLY = [
   'Discover Weekly',
   'Release Radar',
   'New Music Friday',
   'Monday Mix',
   'Tuesday Mix',
   #'Wednesday Mix',
   'Thursday Mix',
   'Friday Mix',
   'Saturday Mix',
   'Sunday Mix',
]

SPOTIFY_DAILY = [
   'Daily Mix 1',
   'Daily Mix 2',
   'Daily Mix 3',
   'Daily Mix 4',
   'Daily Mix 5',
   'Daily Mix 6',
]

GENRES = [ # spotify mixes
   'Brostep',
   'Dance/Electronic',

   'Folk & Acoustic',
   'Pop',
   'Rock'
   'R&B'
]

SPOTIFY_GENRES = [

]

SPOTIFY_CACHE = [
   'On Repeat'
]

TAGS = ['hidden', 'cache', 'collection', 'memory', 'playlist']

FOLDERS = [
   
]