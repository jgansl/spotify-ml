import json, os
import concurrent.futures
from itertools import permutations

# from datetime import datetime, timedelta
# from pydash import flatten
from os import system
from random import shuffle

from _constants import *
from _functions import * # insertTrack



def scanTracks():
   #! defs
   for p in playlists(): #! DB Playists; genres for tracks
   # for p in pb.collection('playlists').get_full_list(): #! DB Playists; genres for tracks
      pname = p['name'] # p.name
      pid   = p['id'] # p.sid
      powner = p['owner']['id'] # p.owner.id

      if pname in [
         'All I Want for Christmas Is You Radio',
         'Beyoncé - This Christmas',
         'Bluegrass Mix',
         'Bluegrass Folk Mix',
         'Calmly Radio',
         'Chill Tracks',
         'Christmas Classics',
         'Christmas',
         'Coding Deep House',
         'Lofi Christmas 2023 /  Christmas Lofi Chillhop Beats 🎄',
         "LoFi Chillhop Christmas / Mellow Holiday Chill Beats / A Merry Lofi Christmas To All!",
         "Classical Bangers 🎹🎻",
         "Indie Bluegrass",
         'New',
         'New Year Radio',
         'Modern Bluegrass Mix',
         "Studio Ghibli Jazz",
         'Sleep Music 😴',
         'Sleepy Zelda: Breath of the Wild',
         'Stream Lofi',
         'Tones And Textures',
         'Vietnamese Hip Hop',
         'Zelda piano for sleeping/relaxing/studying',
      ] or 'Radio' in pname:
         continue


      # print()
      # print(pname)
      if 'Radio' in pname:
         print('Skipping')
         with open('skip.txt', 'a') as f:
            f.write(pname+'\n')
         continue
      # if powner != usr:#and ' Mix' not in pname[-4:] and 'Daily Mix' not in pname[:9]: #! skip certain mixes 2000s
      #    res = input('Continue?')
      #    if len(res):
      #       print('Skipping')
      #       with open('skip.txt', 'a') as f:
      #          f.write(pname+'\n')
      #       continue
      # # continue

      tracks = retrieve(TRACK, pid=pid)
      if powner == usr:
      #    if pname == 'Cycle':
         continue
      #    move(None, cycle['id'], [t['track']['id'] for t in tracks])

      # else:
      print(pname, len(tracks))
      # We can use a with statement to ensure threads are cleaned up promptly
      with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
         # Start the load operations and mark each future with its URL
         future_to_url = {executor.submit(insertTrack, t): t for t in tracks}
         for future in concurrent.futures.as_completed(future_to_url):
            trk = future_to_url[future]
            try:
               data = future.result()
            except Exception as exc:
               print('%r generated an exception: %s' % (trk['track']['id'], exc))
            # else:
            #    # print('%r page is %d bytes' % (url, len(data)))
            #    if data:
            #       # print([*trk])
            #       print(data)

      # input('Continue?')
   
def latestReleases():
   global db_tracks, now, lastest_check
   days = 14
   latest = [t for t in db_tracks if t.release_date > str(now.date() - timedelta(days=days))] #! latest_check
   cutoff = datetime.strptime(lastest_check, '%Y-%m-%d').timestamp()#(now - timedelta(days=days)).timestamp()
   lst = []
   for track in latest:
      if datetime.strptime(track.release_date, '%Y-%m-%d').timestamp() > cutoff:
         lst.append(track.sid)
   print(len(lst), len(latest))
   latest_ids = [t.sid for t in latest]
   platest = [p for p in global_playlists if p['name'] == 'Latest Releases'][0]
   pl_tracks = retrieve(TRACK, pid=platest['id'])
   pl_track_ids = [t['track']['id'] for t in pl_tracks]
   new_tracks = list(set(latest_ids).difference(set(pl_track_ids)))
   move(None, platest['id'], new_tracks)
   # sp.playlist_replace_items(platest['id'], latest_ids[:100])
   # count = 100
   # while count < len(latest_ids):
   #    sp.playlist_add_items(platest['id'], latest_ids[count:count+100])
   #    count += 100
   #! remove old tracks
   lst = []
   cutoff = (now - timedelta(days=days)).timestamp()
   for track in pl_tracks:
      if datetime.strptime(track['added_at'], '%Y-%m-%dT%H:%M:%SZ').timestamp() < cutoff:
         lst.append(track['track']['id'])
   move(platest['id'], None, lst)

def pname(name): #! more than 1
   res = [p for p in global_playlists if p['name'] == name]
   if len(res) == 1:
      return res[0]
   else:
      input(name+': more than on result')


jprint = lambda obj: print(json.dumps(obj, indent=2))
#! main not in results; r-n-b
def discoverGenres():
   #recommendations(seed_artists=None, seed_genres=None, seed_tracks=None, limit=20, country=None, **kwargs)
   seeds = sp.recommendation_genre_seeds()['genres']
   # jprint(seeds)
   data = {}
   if os.path.exists('genres.json'):
      with open('genres.json', 'r') as f:
         data = json.load(f)
   
   # Generate permutations of length two
   perms = [' '.join(p) for p in permutations(seeds, 2)]
   # jprint(perms)
   # seeds.extend(perms)

   for s in seeds:
      if s in [*data]:
         continue
      else:
         print(s)
      # # https://spotipy.readthedocs.io/en/2.22.1/#spotipy.client.Spotify.search
      lst = []
      results = sp.search(q=s, limit=20, type='playlist')
      # 1000 print(results['playlists']['total'])
      lst.extend([p['name'] for p in results['playlists']['items'] if ' Mix' in p['name'][-4:]])
      # while results['playlists']['next']: #? same?
      #    results = sp.next(results['playlists'])
      #    lst.extend([p['name'] for p in results['playlists']['items'] if ' Mix' in p['name'][-4:]])
      lst.sort()
      # jprint(lst)
      data[s] = lst
      with open('genres.json', 'w') as f:
         json.dump(data, f, indent=2)
      sleep(3)

   return

def scanGenres():
   # db
   genres = [
      # 'Beach Music',
      'Country',
      'Dance/Electronic',
      'Drum & Bass',
      'Dubstep',
      'Folk & Acoustic',
      'Future House',
      'House',
      'Hip Hop',
      'Indie',
      'Rap',
      'R&B',
   ]


   # liked = retrieve(SAVED)
   reduce = pname('Reduce')
   liked = retrieve(TRACK, pid=reduce['id'])
   print(len(liked))
   sids = [t['track']['id'] for t in liked]
   tracks = {}
   return
   # concurrent
   for g in genres:
      tracks = retrieve(TRACK, pid=pname(g+' Mix')['id']) #! db
      track_ids = [t['track']['id'] for t in tracks]
      personal = pname(g)
      personal_ids = [t['track']['id'] for t in retrieve(TRACK, pid=personal['id'])]
      lst = list(set(track_ids).intersection(set(sids)))
      lst = list(set(lst).difference(set(personal_ids)))
      print(g, len(lst))
      move(reduce['id'], personal['id'], lst)

      pass

   # move(None, g, [])
   # if release_date > 1:#7:
   #    move(SAVED, None, [])

   return


#! refactor
#! cycle liked songs
#! fine day pretty pink - UTC misalignment - mobile fine?
#! auto genre
#! history of queued - heard

#! db playlists - seeds
if __name__ == '__main__':
   now = datetime.now()
   #today = '2024-02-21' #! UTC; run then update
   global_playlists = playlists()
   # cycles = [p for p in global_playlists if p['name'] == 'Cycle']
   # cycle = cycles[0]
   # caches = [p for p in global_playlists if p['name'] == 'Cache']
   # cache = caches[0]
   # if(len(caches) > 1):
   #    input(caches['name'] + ": " + str(len(caches)))


   # lastest_check = '2024-03-06'
   today = '2024-03-22' #! UTC; run then update

   #!
   # discoverGenres()
   # exit()
   # scanGenres()
   # exit()
   
   db_tracks = pb.collection('tracks').get_full_list()
   db_tracks.sort(key=lambda x: x.release_date, reverse=True)

   # # Patch
   def patch1():
      lst = []
      for t in db_tracks:
         if t.sid in lst:
            #    print(t.sid)
            #    input(t.name)
            #    print()
            try:
               print('Removing '+t.name)
               pb.collection('tracks').delete(
                  t.id
                  # , { 
                  #    'new': True
                  # }
               )
            except: #pocketbase.utils.ClientResponseError
               input(t.name)
               print()
               continue
         else:
            lst.append(t.sid)

   
   # # Patch -set track within released within last
   # days to 'New' -#! randomize
   def patch2():
      for t in [t for t in db_tracks if t.release_date > str(now.date() - timedelta(days=31))]:
         # sp.add_to_queue(t.sid)
         try: 
            pb.collection('tracks').update(
               t.id, 
               { 
                  'new': True 
               }
            )
         except:
            print(t.name, 'Failed') #! check for duplicates
            continue


   def patch3():
      reduce = [p for p in global_playlists if p['name'] == 'Reduce'][0]
      liked = retrieve(SAVED)
      lst = []
      days = 7
      cutoff = (now - timedelta(days=days)).timestamp()
      day_of_year = datetime.now().timetuple().tm_yday
      for track in liked:
         if (
            datetime.strptime(track['added_at'], '%Y-%m-%dT%H:%M:%SZ').timestamp() < cutoff and
            ##str(datetime.strptime(track['track']['album']['release_date'], '%Y-%m-%d').timestamp()) < '2024-01-01'
            track['track']['album']['release_date'] < '2024-01-01'
         ): #day_of_year:
            print(track['track']['album']['release_date'])
            lst.append(track['track']['id'])
      tmp = list(set(lst).difference([t['track']['id'] for t in retrieve(TRACK, pid=reduce['id'])]))
      move(None, reduce['id'], tmp) # + 2024?
      move(SAVED, None, lst)
      return
   # patch3()
   # exit()

   if str(now.date()) == today:
      # patch2()

      tmp = [p for p in global_playlists if '#percent-1' in p['description']][0]
      tmp2 = datetime.now().timetuple().tm_yday
      tmp3 = round(tmp2 * 100 / 366, 2)
      rem = 366 - tmp2
      sp.playlist_change_details(tmp['id'], name=str(rem)+' Days Left - '+str(tmp3)+'% of 2024')

      #! 5/6 years
      # #get number of days left in year 2024
      # remaining_days = 366 - datetime.now().timetuple().tm_yday
      tmp = [p for p in global_playlists if '#percent-2' in p['description']][0]
      day_count = datetime.now() - datetime(2024, 2, 26)
      rem = 365*6 + 2
      rem = round(day_count.days * 100 / rem, 2)
      sp.playlist_change_details(tmp['id'], name=str(day_count.days)+' Days - '+str(rem)+'% of 6 Years')

      # get number of days since Feburary 26, 1995
      # 3951/26298 - 15.03% - 60 years
      day_count = datetime.now() - datetime(1995, 2, 26)
      numdays = day_count.days
      tmp = [p for p in global_playlists if '#percent-3' in p['description']][0]
      percent = round(numdays * 100 / 26298, 2)
      sp.playlist_change_details(tmp['id'], name=str(percent)+'% of 72 Years')

      scanTracks()

   if str(now.date()) == today:
   #    # latestReleases() #! queue instead; every friday - latest

   #    #! playlists db updating; rename cache to cycle and depth 2 to cache
      cycleLiked() #! once a day
   #    pass




