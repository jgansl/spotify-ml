GENRES = [
   # 'Chill',
   'Dance/Electronic',
   'Folk & Acoustic',
   'Hip Hop',
   'House',
   'Drum and Bass',
   'Indie',
   'R&B',
   'Pop',
   'Rock',
   'Vapor Soul',
   'Vapor Twitch',
   'Vaporwave',
]

PLAYLIST = 'playlist'

PUBLIC_PLAYLISTS = [
   #''
]

SAVED = 'saved'

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

TAGS = [
   '#tag--collection',
   '#tag--genre',
   '#tag--playlist',
   '#tag--year',
]

TRACK = 'track'