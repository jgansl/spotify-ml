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
]

SPOTIFY_DAILY_MIXES = [
   'Daily Mix 1',
   'Daily Mix 2',
   'Daily Mix 3',
   'Daily Mix 4',
   'Daily Mix 5',
   'Daily Mix 6',
]

GENRES = [
   'Folk & Acoustic'
]
SPOTIFY_COLLECTIONS = [ 
   'Dance/Electronic', # DJ, EDM & Dance Pop, House, Techno, Trance & Progressive, Disco, Electronic & Chill, Bass Mood/Workout
   'Drum & Bass',
   'Folk & Acoustic',
   'Indie',
   'Hip Hop',
   'Rock',
   'R&B',
   'Vaporwave'
]
SPOTIFY_GENRES = [

]
SPOTIFY_CACHE = [
   'On Repeat'
]

playlists = []
DAILY_MIXES = []
PUBLIC_PLAYLISTS = [
   'How It Feels To Chew 5 Gum',
   # 'Dance/Electronic', # DJ, EDM & Dance Pop, House, Techno, Trance & Progressive, Disco, Electronic & Chill, Bass Mood/Workout
   # 'Folk & Acoustic',
   # 'Hip Hop',
   # 'House',
   # 'Indie',
   # 'Pop',
   # 'Rock',
]


RANKS = {
   'Dance/Electronic': 1,
   'Chill': 2,
   'Drum and Bass': 2,
   'Chill Drum and Bass': 3,
}

CHANNELING = {
   # dst, src - duplicates
   "Drum & Bass": "Dance/Electronic",
   "House": "Dance/Electronic",
   "Pop": "Dance/Electronic",
   #! "Indie Folk" : "Folk & Acoustic", "Indie"
}


TAGS = [
   'tag--public'
]


COLLECTIONS = [ #Liked Songs Genres & Collections Only
   'Chill', #2
   'Dance/Electronic', #1
   'Dubstep', #2
   'Ibiza', #2
   "Folk & Acoustic", #1
   "Hip Hop", #1
   # "House", #2
   "Indie", #1
   "Ibiza", #3
   "Pop", #1
   "Rock", #1
   "R&B", #1
]

RESERVED = [
   'i'
]

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


YEARS = [
   '2023',
   '2022',
   '2021',
   '2020',
   '20s',
   '10s',
   '00s',
   '90s',
   '80s',
]