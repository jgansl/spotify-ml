# NEW

#scan in playlists marked in PB

#only add tracks to collection if less than 365 days old?

# remove 2020 from liked, cycle, collections - in cache and 2020 mix

# scan in tracks
# for genres, add new, and mark old as added to prevent readding
# remove tag--playlists from liked, cycle, collections
# scan artists for new albums, add and mark as dont add again if in playlist
# same for new - run on pi throughout the day
# add discover weekly to new


____






# Spotify AI Assisted Manager (SAAM)


## Tools
[Dedup](https://spotify-dedup.com/)
[Spotipy](https://spotipy.readthedocs.io/en/2.22.1/)
[Smart Shuffle](https://www.grantholtes.com/smartshuffle#access_token=BQAvVi-dVYMx78rdskHXDIclnfXDsluUHUfBpdKDJDsXaA1PJEua4kIOv3Cf0-imRMxw0eCXcb98_0WmvAd6WZBic0IjIrb5jslPaSEPcIaJCUA4BLqDeIG8hQrw0OAWwAsfGiBaZsfXD5obv0oU9BdRq64Sar1tZQyVvJdsbGEp2hbXWGztDoB39RJpBUTE-9DdoQMrZNdCXNOtfXaqsmWCXHzzO5Cplss&token_type=Bearer&expires_in=3600)




"""
- Minimize External Calls
"""
   """
   # redis local copy; docker
   # scan in playlists sync
   # move all liked songs to cycle
   # remove liked songs older than two weeks
   # remove genres from cycle
   # scan in all mix tracks; update genre
   # remove higher specificity genres
   # channeling
   # add 1% of cycled songs back to liked per day
   # add 1% of level 1 genres back to liked per day
   # remove cache from all genre playlists
   # remove years from all genre playlists
   # queue new tracks - app, pi
   """

# refactor refactor refactor
# DRY_RUN, testing
# watch playlists
# unfollow spotipy playlist
# implcitily scna
# backup every hour on pi
# tasks - pi streamlit controller
# cycle - 90 day -> cache - > genre -> subgenre - > artist collection
"""
scan in playlists - personal vs unowned
discover all genres
scan in artists
scan in tracks - genre queueing
ML
add daily to new
remove genre from new
queue old tracks and remove rom gener?
"""


## CHANGELOG