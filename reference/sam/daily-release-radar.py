import spotipy
import datetime
from concurrent.futures import ThreadPoolExecutor
# from spotipy.oauth2 import SpotifyOAuth

from _db import * # db, then external to spotify

from _spotify import sp

# Function to get followed artists
def get_followed_artists():
    artists = []
    results = sp.current_user_followed_artists(limit=50)
    artists.extend(results['artists']['items'])
    while results['artists']['next']:
        results = sp.next(results['artists'])
        artists.extend(results['artists']['items'])
    return [artist['id'] for artist in artists]

# Function to check for new releases in the last 48 hours for a single artist
def check_new_releases(artist_id): #! check all artists
    print(artist_id)
    new_releases = []
    now = datetime.datetime.utcnow()
    two_days_ago = now - datetime.timedelta(days=7)
    print(two_days_ago)
    
    results = sp.artist_albums(artist_id, album_type='album', limit=10)
    print(results)
    for album in results['items']:
        release_date = album['release_date']
        release_date_precision = album['release_date_precision']
        if release_date_precision == 'day':
            release_date = datetime.datetime.strptime(release_date, '%Y-%m-%d')
            if release_date >= two_days_ago:
                new_releases.append(album)
    return new_releases

# Function to batch add tracks to a playlist
def batch_add_tracks_to_playlist(playlist_id, track_ids, batch_size=100):
    for i in range(0, len(track_ids), batch_size):
        sp.playlist_add_items(playlist_id, track_ids[i:i+batch_size])

# Function to get current tracks in a playlist
def get_playlist_track_ids(playlist_id):
    track_ids = []
    track_details = []
    results = sp.playlist_tracks(playlist_id)
    track_ids.extend([item['track']['id'] for item in results['items']])
    track_details.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        track_ids.extend([item['track']['id'] for item in results['items']])
        track_details.extend(results['items'])
    return track_ids, track_details

# Function to remove tracks that are older than 31 days
def remove_old_tracks(playlist_id, track_details, days_old=31):
    now = datetime.datetime.utcnow()
    old_track_ids = []
    for item in track_details:
        added_at = datetime.datetime.strptime(item['added_at'], '%Y-%m-%dT%H:%M:%SZ')
        if (now - added_at).days > days_old:
            old_track_ids.append(item['track']['id'])
    
    if old_track_ids:
        for i in range(0, len(old_track_ids), 100):
            sp.playlist_remove_all_occurrences_of_items(playlist_id, old_track_ids[i:i+100])
        print(f"Removed {len(old_track_ids)} tracks older than {days_old} days.")
    else:
        print("No old tracks to remove.")

# Function to update the playlist
def update_playlist(new_releases, playlist_name="Daily Release Radar"):
    print('Searching for playlist')
    user_id = sp.current_user()['id']
    playlists = sp.user_playlists(user_id)
    
    # Find the playlist by name
    playlist_id = None
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            break
    
    # If the playlist doesn't exist, create it
    print('Creating playlist')
    if not playlist_id:
        playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
        playlist_id = playlist['id']
    
    # Get current track ids and details in the playlist
    current_track_ids, track_details = get_playlist_track_ids(playlist_id)
    
    # Remove tracks older than 31 days
    remove_old_tracks(playlist_id, track_details)
    
    # Get new track ids from the new releases
    print('Gathering tracks...')
    new_track_ids = []
    for album in new_releases:
        tracks = sp.album_tracks(album['id'])
        for track in tracks['items']:
            if track['id'] not in current_track_ids:
                new_track_ids.append(track['id'])
    
    # Batch add the new tracks
    print('Updating playlist')
    if new_track_ids:
        batch_add_tracks_to_playlist(playlist_id, new_track_ids)
    else:
        print("No new tracks to add")

# Main function
def main():
    # artist_ids = get_followed_artists()
    artist_ids = [a.sid for a in drr_artists[:10]]
    new_releases = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_new_releases, artist_id) for artist_id in artist_ids]
        for future in futures:
            new_releases.extend(future.result())
    
    if new_releases:
        update_playlist(new_releases)
    else:
        print("No new releases in the last 48 hours")

if __name__ == "__main__":
    main()