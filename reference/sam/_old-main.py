#! machine learning
#! refactor often

from _db import * # db, then external to spotify
from _functions import *
from _daily import privatizePlaylists
from random import shuffle


def genres():
   # remove cache from liked
   # remove memories from liked
   # remove 90 days old from liked
   for c in COLLECTIONS:
      # get mix
      # get tracks
      # get genre
      # get difference in tracks
      # add to genre
      # remove from cache
      # remove from liked - MANUAL
      pass

def find(): #! insert in pb
   return

def scanInTracks():
   # Release Radar
   # New Music Friday
   # Daily Mixes
   # Genres Mixes - manual update

   return

def queueTracks(lim=30, genre=None, new=True): #! currently impliiclty gets active device
   # global db_tracks, _tracks
   db_tracks = pb.collection('tracks').get_full_list()
   db_tracks = sorted(db_tracks, key=lambda x: x.release_date, reverse=True)
   #! for p in db_tracks[:1000]:
   #    pb.collection('tracks').update(p.id, {
   #       "new": True
   #    })


   pnew = get_playlist('New', 1)
   tracks = retrieve(TRACK, pid=pnew.spotify_id)
   tids = get_ids(tracks)
   #lst = [t.spotify_id for t in db_tracks_new[:2000]]
   #sp.playlist_replace_items(pnew.spotify_id, lst)
   #! track add to liked songs, remove?
   lst = [t.sid for t in db_tracks[:250]]# if t.release_date == today ] #! yesterday only; assume run daily and only run once?
   lst = list(set(lst).difference(set(tids)))
   print(len(lst))
   #move(None, pnew.spotify_id, lst)
   move(None, SAVED, lst) #! flag
   return
   #! rm old

   db_tracks_new = [t for t in db_tracks if t.new]
   total = len(db_tracks_new)

   # for p in db_tracks_new[:lim]:
   #    print(p.release_date)

   print('\tqueueTracks::filtering for genre')
   tmplst = []
   if genre:
      #db_tracks_new = [t for t in db_tracks_new if t.genres and genre in t.genres]
      for t in db_tracks_new:
         if t.genres and genre in t.genres:
            tmplst.append(t)
      db_tracks_new = tmplst
      # for t in db_tracks_new[:lim]:
      #    print(t.release_date)
      # input(genre+': '+str(len(db_tracks_new)))

   

   # Queue for listening
   for idx, t in enumerate(db_tracks_new[:lim]):
      system('clear')
      print(round((idx+1)*lim/lim, 2), '%')
      # print(t.release_date)
      try:
         sp.add_to_queue(t.spotify_id)
      except:
         print('Error adding to queue', t.name, t.sid)
         continue
      pb.collection('tracks').update( #! may not be accurate
         t.id, 
         { 
            'new': False 
         }
      )
      sleep(1)

   return

def cycleLiked():
   #egt liked
   #get cycle
   # move 4% of cycles
   # move out liked songs older than 1 week

   # global cycle, today, now, cache
   global today, now
   print('\n\ncycleLiked')

   cycle = get_playlist('Cycle')
   # cycle = cycles[0]
   # caches = get_playlist('Cache')
   # cache = caches[0]

   cache_track_ids = []#[t['track']['id'] for t in retrieve(TRACK, pid=cache['id'])]
   # move(SAVED, None, cache_track_ids)
   # move(cycle['id'], None, cache_track_ids)

   
   liked = retrieve(SAVED)
   # liked_ids = [t['track']['id'] for t in retrieve(SAVED)]
   lst = []
   days = 7
   cutoff = (now - timedelta(days=days)).timestamp()
   for track in liked:
      if datetime.strptime(track['added_at'], '%Y-%m-%dT%H:%M:%SZ').timestamp() < cutoff:
         get_track(track['track']['id']) #! add to db
         lst.append(track['track']['id'])
   #print(len(lst))


   lst = list(set(lst).difference(set(cache_track_ids)))

   # cycle = getPlaylist('Cycle')
   cycle_track_ids = [t['track']['id'] for t in retrieve(TRACK, pid=cycle.sid)]
   
   tmp2 = list(set([t['track']['id'] for t in liked]).difference(set(cache_track_ids)))
   tmp = list(set(tmp2).difference(set(cycle_track_ids)))
   print('Cycling out:', len(lst))
   # print(len(lst))
   # exit()
   if len(tmp): #! only removes if not in cycle
      move(None, cycle.sid, tmp)
   #!! if len(lst):
   #    move(SAVED, None, lst)
   sleep(3)
   
   cycle_tracks = retrieve(TRACK, pid=cycle.sid)
   shuffle(cycle_tracks)
   amt = int(len(cycle_tracks) / 100) # 2%
   print('Cycling in:', amt)
   # move( None, SAVED, lst)
   #! remove those that are less than 10 minutes old; currently only add the oldest 10 percent
   # for c in cycle_tracks[:amt]:
   #    print(c['added_at'])
   cycling = [t['track']['id'] for t in cycle_tracks[:amt]]
   move(cycle.sid, SAVED, cycling)
   sleep(3)
   move(None, cycle.sid, cycling)

   
   return


def main():
   def funct(name, genre=None, idx=0):
      # name = genre + ' Mix'
      print(name)
      playlist = get_playlist(name, idx)
      tracks = retrieve(TRACK, pid=playlist.spotify_id)
      tracks_ids = get_ids(tracks)
      # if (
      #    # 'Daily Mix' in name or
      #    'Discover Weekly' in name or
      #    'Release Radar' in name
      # ):
      #    move(None, SAVED, tracks_ids)
      for tid in tracks_ids:
         record = get_track(tid, genre)
         # if record:
         #    print('\t\t'+record.name)
      return tracks_ids

   # scan all daily mixes for new tracks
   cache = pname('Cache')
   cache_track_ids = get_ids(retrieve(TRACK, pid=cache['id']))
   for name in [ #! scan in genres.json
      #! followed only  ?
      'Chill',
      'Dance/Electronic',
      'Drum and Bass',
      'Dubstep',
      'Folk & Acoustic',
      'Future Bass',
      'Future House',
      'Hip Hop',
      'House',
      'Ibiza', #! search
      'Indie',
      #'Jazz',
      'Laid Back',
      'Pop',
      'R&B', #! 0. R&B Mix 37i9dQZF1EQoqCH7BwIYb7 # 1. R&B Mix 37i9dQZF1EIUJlbtxh7dav
      'Rock',
      # 'Vapor Soul',
      'Vapor Twitch',
      '2020s',
      '2010s',
      '2000s',
      '90s',
      '80s',
   ]:
      try:
         tids = funct(name+' Mix', name)
      except:
         print('Error:', name+' Mix')
         continue
      p = pname(name+' Collection')
      p_track_ids = get_ids(retrieve(TRACK, pid=p['id']))
      # get tracks diff
      lst = list(set(tids).difference(set(p_track_ids)))
      print(len(lst))
      move(None, p['id'], lst)
      # move(None, SAVED, lst)
      # input('Continue')

      #! remoev years from collections
      trks = list(set(cache_track_ids).intersection(set(lst)))
      move(cache['id'], p['id'], trks)
      trks = list(set(cache_track_ids).intersection(set(p_track_ids)))
      move(cache['id'], p['id'], trks)

      """ #!
      Vapor Twitch Mix
      pname- looking for: Vapor Twitch Collection
      50
         Submitted 0
      HTTP Error for POST to https://api.spotify.com/v1/playlists/5W2je3blGFghSqfsZkuEJX/tracks with Params: {'position': None} returned 400 due to No uris provided
      """

   for name in [
      'Daily Mix 1',
      'Daily Mix 2',
      'Daily Mix 3',
      'Daily Mix 4',
      'Daily Mix 5',
      'Daily Mix 6',
      'Monday Mix',
      'Tuesday Mix',
      'Weekday Mix',
      'Thursday Mix',
      'Friday Mix',
      'Saturday Mix',
      'Sunday Mix',
      'Bedroom Vibes ',
      'Car Music',
      'Chill House 2024',
      'Chill Tracks',
      'Colorize: Sunset House',
      'Discover Weekly', #! Discover Daily
      'Dubstep Don',
      "Edmtrain's New Music Weekly",
      'HITS 2024 - Today\'s Top Songs', #! IDs instead - or db marker?
      "just hits",
      'Melodic Techno Elements',
      'New Music Friday',
      'On Repeat',
      'Release Radar', # 0. Release Radar 37i9dQZEVXbvpLI9vZOceC 1. Release Radar 37i9dQZEVXbkwg9UeOLoTP
      # 'Release Radar - Troy' #! name conflicts - dup on retrieve()
      'soft indie saturday morning',
      'Sunday Mood',
      'Trap Mojito',
   ]: #! move Troy + Jesse to Cache
      funct(name, None)
   
   funct('R&B Mix', 'R&B', 1)
   funct('Release Radar', None, 1)

   return 

import os, json
def reorder():
   """# TODO - unfollow?
   0. Indie Collection 4vbyA4Lx2r1VIJqqnF7nhI
   1. Indie Collection 5Yl0uHtoHkL23qX6QVNMMb
   """
   p = 'Indie Collection'
   playlist = get_playlist(p)
   tracks = retrieve(TRACK, pid=playlist.sid) #! not fetched in order
   # for i, t in enumerate(tracks):
      # os.system('clear')
      # print(i+1, t['track']['album']['release_date'])
   #    input('Continue?')
   track_ids = [t['track']['id'] for t in tracks]
   # sort tracks by release date
   tracks_ordered = sorted(tracks, key=lambda x: x['track']['album']['release_date'], reverse=True)
   for t in tracks_ordered:
      print(t['track']['album']['release_date'], t['track']['name'])
   track_ordered_ids = [t['track']['id'] for t in tracks_ordered]
   total = len(tracks_ordered)
   count = 0
   with open('indie.json-ordered', 'w') as f:
      dump([[t['track']['name'], t['track']['album']['release_date']] for t in tracks_ordered], f, indent=2)
   exit()
   # with open('indie.json', 'w') as f:
   #    dump(tracks_ordered, f, indent=2)
   # exit()
   # with open('indie.json', 'r') as f:
   #    tracks_ordered = json.load(f)
   #    track_ordered_ids = [t['track']['id'] for t in tracks_ordered]
   # for i, t in enumerate(tracks_ordered):
   #    #print(track_ordered_ids.index(t['track']['id']), i, t['track']['name'], t['track']['album']['release_date'])
   #    print(t['track']['album']['release_date'], t['track']['name'], track_ids.index(t['track']['id']))

   #    # if(i != track_ordered_ids.index(t['track']['id'])):
   #    #    print('moving')
   #    sp.playlist_reorder_items(playlist.sid, range_start=track_ids.index(t['track']['id']), range_length=1, insert_before=0)
   #    input('Continue?')
   #    # else:
   #    #    print(t['track']['album']['release_date'], track_ids.index(t['track']['id']))
      
   #    # sleep(0.2)
   #! random chance it is aligned?
   #validate

   # print(track_ordered_ids[-50:])
   total = len(track_ordered_ids)
   sp.playlist_replace_items(playlist.sid, [track_ordered_ids[0]])
   sleep(0.2)
   for i in range(total-1, 0, -1):
      # print(track_ordered_ids[i-50:i])
      # j = max(0, i-50)
      sp.playlist_add_items(playlist.sid, [track_ordered_ids[i]])
      # input('Continue?')
      sleep(0.2)
   

   

now = datetime.now()
#! cli; api; async
#! remove years from cache
#! check db for dups
if __name__ == '__main__':
   now = datetime.now()
   with open('db/_meta.json', 'r') as f:
      meta = load(f)
   now_str = datetime.strftime(now, '%Y-%m-%d')
   today = meta['today'] #'2024-03-22' #! UTC; run then update - probelmtaic for new release
   run_daily = now_str != today
   
   percent1 = [p for p in sp_playlists if '#percent-1' in p['description']][0]
   if run_daily:
      meta['today'] = now_str

      tmp2 = datetime.now().timetuple().tm_yday
      tmp3 = round(tmp2 * 100 / 366, 2)
      rem = 366 - tmp2
      sp.playlist_change_details(percent1['id'], name=str(rem)+' Days Left - '+str(tmp3)+'% of 2024')

      #! 5/6 years
      # #get number of days left in year 2024
      # remaining_days = 366 - datetime.now().timetuple().tm_yday
      tmp = [p for p in sp_playlists if '#percent-2' in p['description']][0]
      day_count = datetime.now() - datetime(2024, 2, 26)
      rem = 365*6 + 2
      rem = round(day_count.days * 100 / rem, 2)
      sp.playlist_change_details(tmp['id'], name=str(day_count.days)+' Days - '+str(rem)+'% of 6 Years')

      # get number of days since Feburary 26, 1995
      # 3951/26298 - 15.03% - 60 years
      day_count = datetime.now() - datetime(1995, 2, 26)
      numdays = day_count.days
      tmp = [p for p in sp_playlists if '#percent-3' in p['description']][0]
      percent = round(numdays * 100 / 26298, 2)
      sp.playlist_change_details(tmp['id'], name=str(percent)+'% of 72 Years')


      # #! privatizePlaylists() #! not working; #tag--public; do when scanning playlists - does not change number of queries
      # # make percent playlists public?

      # # # remove cached from saved; #! cycle in?
      # cache = pname('Cache') #! get_playlist
      # cache_ids = [s['track']['id'] for s in retrieve(TRACK, pid=cache['id'])]
      # saved = retrieve(SAVED)
      # sids = [s['track']['id'] for s in saved]
      # move(SAVED, None, list(set(sids).intersection(set(cache_ids))))
      # cycle = pname('Cycle')
      # cycle_ids = [s['track']['id'] for s in retrieve(TRACK, pid=cycle['id'])]
      # move(cycle['id'], None, list(set(sids).intersection(set(cache_ids))))

      # percent1_ids = [s['track']['id'] for s in retrieve(TRACK, pid=percent1['id'])]
      # move(SAVED, None, list(set(sids).intersection(set(percent1_ids))))
      # move(cycle['id'], None, list(set(cycle_ids).intersection(set(percent1_ids))))
      # for name in [ #! const, meta
      #    # '2023',
      #    '2022',
      #    '2021',
      #    '2020',
      #    '20s',
      #    '10s',
      #    '00s',
      #    '90s',
      #    '80s',
      # ]:
      #    print(name)
      #    p = pname(name)
      #    p_ids = [s['track']['id'] for s in retrieve(TRACK, pid=p['id'])]
      #    # remove from cache
      #    #x if track if 7 days old
      #    # remove for saved
      #    move(SAVED, None, list(set(p_ids).intersection(set(sids))))
      #    move(cycle['id'], None, list(set(p_ids).intersection(set(cycle_ids))))
      #    move(cache['id'], None, list(set(p_ids).intersection(set(cache_ids))))

      main()
      # cycleLiked() #! dont add liked to cycle only cycle cycled songs in and out

      #! on success
      with open('db/_meta.json', 'w') as f:
         dump(meta, f, indent=2)

   # reorder()

   # Daily Mix matching - ai

   #cli ? 
   #! take first 1000 tracks - replace new playlist; shuffle
   #! check for device
   # queueTracks(lim=30, genre=None, new=True) # exact genre

   # scan genres - manual specification - set to true
   # insert in pb
   # scan mixes
   # update genres
   # generate new playlists - queueUnheard
   # main()

   # pirvatize
   # cycle liked, remove cached(10s, etc) from liked - after 2 weeks

   #! Kiss - Cache, Cycle, Liked
   #! cache into genres and rm from cache


   pass