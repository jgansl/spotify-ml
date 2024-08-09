# scan in saved, explore
# top songs and related artists
# sort explore into genres
# supyter
# popular genres creation
# tagging

# EXPART = '#explore-artists' #fetch
# p_explore_gen = mem.ptag(EXPART)

#personal genres - artists summarization into new. unheard

from os import system
from time import sleep
from pydash import flatten
import re
from functions import SAM, sp, jprint, mem, TRACK, SAVED
from pocketbase import PocketBase
pb = PocketBase('http://127.0.0.1:8092', 'en-US')
trk_db = {}
for i in pb.records.get_full_list('spotify'):
   trk_db[i.sid] = i
art_db = {}
for i in pb.records.get_full_list('artists'):
   art_db[i.sid] = i

for i in [*trk_db]:
   s = sp.track(i)
   print('\t\t'+s['name'])
   artists = s['artists']
   for a in s['artists']:
      if a['id'] in [*art_db]: 
         continue
      print('\t'+a['name'])
      genres = sp.artists([a['id']])['artists'][0]['genres']
      try:
         art_db[a['id']] = pb.records.create(
            'artists', 
            {
               "sid":a['id'], 
               "name":a['name'],
               'genres': genres, 
               "tracks":[], 
               # "unheard": [] #!update
            }
         )
         print('\tINSERT '+a['name'])
      except:
         print('SKIP ', a['name'])
   # sleep(1)

#combine genres and song attributes - k lcusting
# auto generate based on genre and attributes fine tuning - auto mixing
# range tempo