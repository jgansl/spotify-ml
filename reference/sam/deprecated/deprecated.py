# AI developer
# top down; refactor 30 lines of code max
# should not depend on running program as much as possible
"""
TODO
- insert artist only if multiple liked songs in relative recent time
- add unheard to artists in generateDailyArtistMixes
- local sync of spotify
- refactor
- remove 2023 from 2022 - overlap only

- [ ] dance/electronic - implicitly follow
- [ ] dance/electronic - move liked out if in two weeks old, in genre, older than 365 days, cycle cache
- [x] absorb into artist table

- restart
- audio_analysis(track_id)
- audio_features(tracks=[])
- categories() # https://spotipy.readthedocs.io/en/2.22.1/#spotipy.client.Spotify.categories
- local map of tracks for less api calls
"""

import concurrent.futures

from datetime import datetime
# from pydash import flatten
from random import shuffle

from _constants import *
from _functions import *
from _utilities import *


now = datetime.now()

def parallel(lst, func): #! concurrent

   return
def cacheOnRepeat():
   sids = []
   cache = getPlaylist('Cache')
   onRepeat = getPlaylist('On Repeat')
   yearPlaylist = getPlaylist(now.year)
   # for t in retrieve(TRACK, pid=onRepeat['id']):
   lst = [t['track']['id'] for t in retrieve(TRACK, pid=onRepeat['id'])]
   move(yearPlaylist['id'], None, lst) #! difference
   move(SAVED, None, lst)
   return


def generateDailyArtistMixes():
   """
   - db tracks, concurrency, meta flag for running
   """
   print('\ngenerateDailyArtistMixes\n')

   count = 0
   def func(name):
      nonlocal count
      #! ['id'] vs spotify_id
      # sp.current_user_unfollow_playlist(mix.spotify_id) #need to update _playlists; invalidate

      # get the playlist
      mix = getPlaylist(name) #implicitly follow
      if not mix: 
         print('Could not find: '+name)
         return
      

      # extract
      lst = []
      artists = []
      # print(mix)
      for t in retrieve(TRACK, pid=mix.spotify_id):
         # add track to lst;NEW if not in DB
         a = getArtist(t['track']['artists'][0]['id'])
         # print(a, t['track']['artists'][0]['name'])
         if t['track']['id'] not in a.heard and t['track']['id'] not in a.queue:
            count += 1
            print('inserting: ', count)
            # record = insertTrack(t, 'queue')
            try:
               addQueueToArtists(t)
            except: 
               print('ERROR', t['track']['name'], t['track']['artists'][0]['name'])
               continue
            # if record: #not exists double check
            #    db_heard.append(record)
            #    db_heard_ids.append(record.sid)

      #    # extract first artist
      #    artists.append(t['track']['artists'][0]['id'])
      
      # # for artists, get top and latest tracks
      # artists = list(set(artists))
      # for artist in artists:
      #    # get top tracks
      #    topTracks = sp.artist_top_tracks(artist['id'], 'US')

      #    # get latest releases
      #    ## latest first
      #    artist_albums = sp.artist_albums(artist_id, album_type=None, country=None, limit=50, offset=0)
      #    for album in artist_albums:
      #       if album['release_date'].year == now.year:
      #          continue
      #       album_tracks = sp.album_tracks(album['id'], limit=50, offset=0, market=None)

      #    #! get related artists
      #    # sp.artist_related_artists(artist_id)

      # # get the artist playlist
      # artist_mix = getPlaylist(p.replace('Daily Mix', 'Daily Artist Mix'))
      
      # #shuffle and add to artist_mix


      return

   tmp = [
      'Discover Weekly',
      'New Music Friday',
      '2020s Mix',
      'Dance/Electronic Mix',
      'Folk & Acoustic Mix',
      'Hip Hop Mix',
      'House Mix',
      'Indie Mix',
      'Pop Mix',
      'Rock Mix',
   #    'R&B Mix',
      'Monday Mix',
      'Tuesday Mix',
      # 'Wednesday Mix',
      'Weekday Mix',
      'Thursday Mix',
      'Friday Mix',
      'Saturday Mix',
      'Sunday Mix',
   ]
   if now.weekday() == 4:
      tmp.append('Release Radar')
      tmp.append('Release Radar')
   for name in tmp:
      func(name)
   for name in SPOTIFY_DAILY_MIXES: #implicitly follow conditional
      func(name)
   #! func('Release Radar')
   func('Discover Weekly')
   # func('2020s Mix')

# move saved in genre and remove if two weeks old or past years
def removeCachefromSaved():

   print('\nremoveCachefromSaved\n')

   cache = []
   saved_lst = []
   #get saved
   saved = []
   #check date
   for s in saved:
      if s['added_at'] < now - timedelta(days=14):
         saved_lst.append(s['track']['id'])

   for genre in SPOTIFY_COLLECTIONS:
      # get playlist
      mix = getPlaylist(genre + ' Mix')
      playlist = getPlaylist(genre)
      playlist_tracks = getPlaylist(genre)

      # get tracks
      trcks = getTracks(playlist['id'])

      #intersection with saved move to playlist
      lst = set(trcks).intersection(set(saved))
      lst = list(lst.difference(set(playlist_tracks)))
      move(None, playlist['id'], lst) #! update local

      


   #! years - yearly patch
   # base = 2000
   # track_map = {}
   # for i in range(int(now.year), base, -1):
   #    # get playlist

   #    # get tracks
      
   #    # remove from higher playlists - recursion
   #    for j in range(i, base, -1):
   #       lst = []
   #       # move(i, j, lst)
   
   return


def queueUnheard():
   
   print('queueUnheard\n')
   
   lookup = {}
   for a in db_artists:
      for tid in a.queue:
         lookup[tid] = a.spotify_id
   # queue = shuffle(flatten([a.heard for a in db_artists]))
   print(len([*lookup]))
   # print(db_queue)
   # for i in sorted(db_queue, key=lambda x: x.release_date)[:50]: #! shuffle
   lst = [*lookup]
   shuffle(lst) #in place?
   #! 429?
   for i in lst[:50]:
      # print(i.release_date)
      sp.add_to_queue(i)
      artist = db_artist_map[lookup[i]]
      artist.queue = list(set(artist.queue).difference(set([i])))
      artist.heard.append(i)
      pb.collection('artists').update(
         artist.id,
         {
            'queue': artist.queue,
            'heard': artist.heard
         }
      )
   return


def cacheOldSaved():
   print('\ncacheOldSaved\n')
   lst = []
   cycle = getPlaylist('Cycle')
   cycle_trcks = [t['track']['id'] for t in getTracks(cycle.sid)]
   for s in saved():
      # if s['added_at'] < now - timedelta(days=14):
      #    lst.append(s['track']['id'])
      tmp2 = datetime.strptime( s['added_at'], '%Y-%m-%dT%H:%M:%SZ')
      tmp3 = now - tmp2
      if( tmp3.days > 14):
         lst.append(s['track']['id'])
   print(len(lst), '\n')
   lst = list(set(lst).difference(set(cycle_trcks)))
   move(SAVED, cycle.sid, lst)

def checkSavedGenre():
   print('\ncheckSavedGenre\n')
   # for genre in SPOTIFY_COLLECTIONS: #! CHANNELING
   for genre in [
      'Dance/Electronic', # DJ, EDM & Dance Pop, House, Techno, Trance & Progressive, Disco, Electronic & Chill, Bass Mood/Workout
      'Folk & Acoustic',
      'Hip Hop',
      'House',
      'Indie',
      'Pop',
      'Rock',
   ]:
      print(genre)
      # get playlist
      mix = getPlaylist(genre + ' Mix')
      cycle = getPlaylist('Cycle')
      playlist = getPlaylist(genre)

      # get tracks
      mix_trcks = [t['track']['id'] for t in getTracks(mix.sid)]
      cycle_trcks = [t['track']['id'] for t in getTracks(cycle.sid)]
      playlist_trcks = [t['track']['id'] for t in getTracks(playlist.sid)]

      #intersection with saved move to playlist
      # move genre if in saved

      sids = [s['track']['id'] for s in saved()]

      #! duplicate of rmGenreFromCache
      # sids = []
      # for s in saved():
      #    tmp2 = datetime.strptime( s['added_at'], '%Y-%m-%dT%H:%M:%SZ')
      #    tmp3 = now - tmp2
      #    if( tmp3.days > 14):
      #       sids.append(s['track']['id'])
      lst = set(sids).intersection(set(mix_trcks))
      lst = list(set(lst).difference(set(playlist_trcks)))
      # move(SAVED, None, lst) #! update local
      move(None, playlist.sid, lst) #! update local
      
      # playlist_trcks = [t['track']['id'] for t in getTracks(playlist.sid)]

      # lst = set(cycle_trcks).intersection(set(mix_trcks))
      # lst = list(set(lst).difference(set(playlist_trcks)))
      # move(cycle.sid, None, lst) #! update local

def rmCacheFromCycle():
   print('\nrmCacheFromCycle')
   cycle = getPlaylist('Cycle')
   cycle_trcks = [t['track']['id'] for t in getTracks(cycle.sid)]
   
   cache = getPlaylist('Cache')
   cache_trcks = [t['track']['id'] for t in getTracks(cache.sid)]

   lst = list(set(cycle_trcks).intersection(set(cache_trcks)))
   move(cycle.sid, None, lst) #! update local



def rmGenreFromCache():

   print('\nrmGenreFromCache')
   for genre in [
      'Dance/Electronic', # DJ, EDM & Dance Pop, House, Techno, Trance & Progressive, Disco, Electronic & Chill, Bass Mood/Workout
      'Folk & Acoustic',
      'Hip Hop',
      'House',
      'Indie',
      'Pop',
      'Rock',
   ]:
      print(genre)
      # get playlist
      playlist = getPlaylist(genre)
      cycle = getPlaylist('Cycle')
      # print(cycle)
      # return

      # get tracks
      playlist_trcks = [t['track']['id'] for t in getTracks(playlist.sid)]
      cycle_trcks = [t['track']['id'] for t in getTracks(cycle.sid)]

      #intersection with saved move to playlist
      lst = list(set(cycle_trcks).intersection(set(playlist_trcks)))
      # lst = list(lst.difference(set(playlist_tracks)))
      move(cycle.sid, None, lst) #! update local
      move(SAVED, None, lst) #! update local

   return


def rmYearsFromCycle(): #!
   
   print('\nrmYearsFromCache')


   cycle = getPlaylist('Cycle')
   cycle_trcks = [t['track']['id'] for t in getTracks(cycle.sid)]

   for p in [p for p in playlists() if '#year' in p['description']]:
      print(p['name'])
      track_ids = [t['track']['id'] for t in getTracks(p['id'])] #! local copy
      lst = list(set(cycle_trcks).intersection(set(track_ids)))
      move(cycle.sid, None, lst)

   return

def rmYearsFromGenres(): #!
   
   print('\nrmYearsFromGenres')
   
   lookup = {}
   for genre in [
      'Dance/Electronic', # DJ, EDM & Dance Pop, House, Techno, Trance & Progressive, Disco, Electronic & Chill, Bass Mood/Workout
      'Folk & Acoustic',
      'Hip Hop',
      'House',
      'Indie',
      'Pop',
      'Rock',
   ]:
      print(genre)
      playlist = getPlaylist(genre)
      lookup[playlist.sid] = [t['track']['id'] for t in getTracks(playlist.sid)]

   #! does not return records for p in [p for p in playlists() if '#year' in p.description]:
   for p in [p for p in playlists() if '#year' in p['description']]:
      print(p['name'])
      track_ids = [t['track']['id'] for t in getTracks(p['id'])]
      for genre_id in [*lookup]:
         lst = list(set(lookup[genre_id]).intersection(set(track_ids)))
         move(genre_id, None, lst)
   return

def cycle():
   print('\ncycle')
   cycle = getPlaylist('Cycle')
   cycle_trcks = [t['track']['id'] for t in getTracks(cycle.sid)]
   shuffle(cycle_trcks)
   move(None, SAVED, cycle_trcks[:2]) # total 14 * 5 = 28 max songs cycling
   return


def rmPlaylistFromSaved():
   return

def savedMix(): #! check mixes - already done?
   for genre in [
      'Dance/Electronic', # DJ, EDM & Dance Pop, House, Techno, Trance & Progressive, Disco, Electronic & Chill, Bass Mood/Workout
      'Folk & Acoustic',
      'Hip Hop',
      'House',
      'Indie',
      'Pop',
      'Rock',
   ]:
      print(genre)
      mix = getPlaylist(genre + ' Mix')
      playlist = getPlaylist(genre)
      mix_trcks = [t['track']['id'] for t in getTracks(mix.sid)]
      playlist_trcks = [t['track']['id'] for t in getTracks(playlist.sid)]
      lst = set(mix_trcks).intersection(set(sids))
      move(None, playlist.sid, lst) #! update local
   return

def channeling(): #! Chill
   for key in [*CHANNELING]:
      src = getPlaylist(CHANNELING[key])
      src_trcks = [t['track']['id'] for t in getTracks(src.sid)]
      
      mix = getPlaylist(key + ' Mix')
      mix_trcks = [t['track']['id'] for t in getTracks(mix.sid)]
      
      dst = getPlaylist(key)
      
      lst = set(mix_trcks).intersection(set(src_trcks))
      move(None, dst.sid, lst)
      
      dst_trcks = [t['track']['id'] for t in getTracks(dst.sid)]
      lst = set(src_trcks).intersection(set(dst_trcks))
      move(src.sid, None, lst)

def scanPersonalIn():
   
   print('\nscanPersonalIn')
   count = 0
   def localFunc(p):
      nonlocal count
      for t in getTracks(p['id']):
         #get artists
         #update heard and queue
         addHeardToArtists(t)
         count += 1
         print(t['track']['artists'][0]['name'], count)
   with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
      # Start the load operations and mark each future with its URL
      future_to_p = {executor.submit(localFunc, p): p for p in [p for p in playlists() if p['owner']['id'] == usr]}
      for future in concurrent.futures.as_completed(future_to_p):
         url = future_to_p[future]
         try:
            data = future.result()
         except Exception as exc:
            print('%r generated an exception: %s' % (p, exc))
         # else:
         #    print('%r page is %d bytes' % (p, len(data)))

#! remove playlists from liked songs
#! increament day playlist

if __name__ == '__main__':

   syncPlaylistsToDB() #! changing playlist name produces dupliicat Cache
   if False: #not test
      #x cacheOnRepeat()
      #x removeCachefromSaved()
      
      # rmYearsFromGenres()
      # rmPlaylistFromSaved() # mimic of _years
      # savedMix()
      # channeling()



      pass


   else:
      # print('Now: ', now.date(), str(now.date()) == '2023-12-20')
      if str(now.date()) == '2023-12-23': #! only once a day 
         scanPersonalIn() #! ? saved
         cacheOldSaved()
         checkSavedGenre()
         rmCacheFromCycle()
         rmGenreFromCache()
         rmYearsFromCycle()
         rmYearsFromGenres()
         cycle()
         generateDailyArtistMixes()

      queueUnheard() # active device
      #! channeling radio

      pass
