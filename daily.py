"""
- top downa approach
- refactor and test
- dry run
- ai written/managed i.e. codium
"""

import _functions as _f
from _functions import log, sp, user_id

RECENTLY_RELEASED = 'Recently Released'

# move liked songs from recently released
def move_liked_songs_from_recently_released():
   # Get the playlist ID of "Recently Released"
   playlists = _f.get_all_playlists()
   recently_released_p = [playlist for playlist in playlists if playlist['name'] == RECENTLY_RELEASED]
   if not recently_released_p:
      print("Playlist 'Recently Released' not found.")
      return

   recently_released_pid = recently_released_p[0]['id']

   # Get track IDs from "Liked Songs" and "Recently Released" playlist
   liked_tracks = set(_f.get_liked_tracks())
   recently_released_tracks = set(_f.get_playlist_tracks(recently_released_pid))

   # Find tracks that are in both "Recently Released" and "Liked Songs"
   tracks_to_move = recently_released_tracks.intersection(liked_tracks)

   if not tracks_to_move:
      print("No tracks to move.")
      return

   # # Move tracks to Liked Songs
   # add_tracks_to_liked(list(tracks_to_move))

   # Remove tracks from "Recently Released" playlist
   _f.remove_tracks_from_playlist(list(tracks_to_move), recently_released_pid)

   print(f"Moved {len(tracks_to_move)} tracks to 'Liked Songs' and removed them from 'Recently Released'.")


def move_discover_weekly_to_release_radar():
   # if not monday return
   return

# Top-Down Approach
def main():
   #! search for playlist - not following?
   # discover weekly
   # release radar
   # EDM Train
   # move Troy + Jesse into recently released
   move_liked_songs_from_recently_released()
   # move_collections_from_recently_released()
   # move_liked_songs_from_collections()

   move_discover_weekly_to_release_radar()


if __name__ == '__main__':

   main()