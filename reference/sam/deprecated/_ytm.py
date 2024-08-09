# import json, os, re
from functions import *
from spotipy.exceptions import SpotifyException
import urllib.parse

from ytmusicapi import YTMusic # https://ytmusicapi.readthedocs.io/en/latest/setup.html


# https://ytmusicapi.readthedocs.io/en/latest/
ytc = YTMusic('headers_auth.json')

def getSTrack(y):
   name = y['title']
   res = sp.search(name, limit=25, type="track")['tracks']['items']
   for i in res:
      for key in [
         #! 'album', #! 
         'available_markets',
         'disc_number',
         #! 'duration_ms', #! 
         'explicit',
         'external_urls',
         'href',
         'preview_url',
         'track_number',
         'type',
         'uri',
         'external_ids',
         'is_local',
         'popularity'
      ]:
         del i[key]
   lst = []
   for t in res:
      if name.lower() in t['name'].lower():
         lst.append(t) #!check artists
   jprint(lst)
   print(len(lst))
   print(name)
   input()
   # Search - for sp:https://developer.spotify.com/documentation/web-api/reference/#/operations/search
   return



def ytSearch(q):
   res = ytc.search(
      q,
      filter='songs',
      # limit=20,
      # ignore_spelling=False
   )
   # jprint([*res[0]])
   for i in res:
      for key in [
         "resultType",
         # "title",
         "album", #! 
         # "feedbackTokens",
         # "videoId",
         "duration", #! 
         "year",
         # "artists",
         "isExplicit",
         "thumbnails"
      ]:
         del i[key]
   return res


def getYTrack(s): #s is saved item - > check keys
   name = s['track']['name']
   artists = s['track']['artists']
   anames = [a['name'] for a in artists]
   print('Searching for:', name, '-', ', '.join(anames))

   # Search - for sp:https://developer.spotify.com/documentation/web-api/reference/#/operations/search
   res = ytSearch(name)  
   # jprint(res)
   lst = []
   #! type == song
   for t in res:
      try:
         if t['artists'][0]['name'].lower() in [a['name'].lower() for a in artists] and (name.lower() in t['title'].lower() or t['title'].lower() in name.lower()):
            lst.append(t)
      except IndexError:
         return # Distant Utopia - Lawrence Walther, kairos, Iamcloud, Blocktane
   if not lst:
      res = ytSearch(" ".join([name,anames[0]]))   
      for t in res:
         if t['artists'][0]['name'].lower() in [a['name'].lower() for a in artists] and (name.lower() in t['title'].lower() or t['title'].lower() in name.lower()):
            lst.append(t)
      print('\tfailed name only')
      # jprint(res)

   #! filter further for multipel artsts in title or artists len

   if not lst:
      print('\tCould not find:', name, '-', ', '.join(anames))
      # input('Continue?')
      print()
      return
   if len(lst) > 1: #! remix / live / unplugged
      #! reduce exact duplicates; add all remixes
      tmplst = []
      for i in lst:
         # Sea Wolf - You're a Wolf
         if i['title'] in [j['title'] for j in tmplst] or 'live' in i['title'].lower():# or 'remix' in i['title'].lower():#and len(i['artists']) == len():
            continue
         # else:
         # jprint(tmplst)
         # print(i['title'])
         # print()
         tmplst.append(i)
      lst = tmplst
      tmplst = [t for t in lst if 'remix' not in t['title'].lower()]
      jprint(tmplst) #filter - remove dup and remixes
      print(len(tmplst))
      ret = []
      if len(tmplst) > 1:
         inp = ''
         while not inp.isdigit() or int(inp) > len(lst):
            inp = input('Choose:')
         ret = tmplst[int(inp) - 1:int(inp)]
      ret.extend([t for t in lst if 'remix' in t['title'].lower()])
   else:
      ret = lst
   
   print()
   # return lst[0]
   return ret


   # https://ytmusicapi.readthedocs.io/en/latest/reference.html#ytmusicapi.YTMusic.add_playlist_items
   
   
   return
   
def spRemixes():

   for s in mem.saved:
      res = sp.search(name + 'remix', limit=25, type="track")['tracks']['items']
      for i in res:
         for key in [
            #! 'album', #! 
            'available_markets',
            'disc_number',
            #! 'duration_ms', #! 
            'explicit',
            'external_urls',
            'href',
            'preview_url',
            'track_number',
            'type',
            'uri',
            'external_ids',
            'is_local',
            'popularity'
         ]:
            del i[key]
      lst = []
      flag = True
      for t in res:
         if flag:
            jprint(t)
            flag= False
         if s['track']['name'].lower() in t['name'].lower() and s['track']['artists'][0]['name'].lower() in [a['name'] for a in t['track']['artists']]:
            lst.append(t['track']['id']) #!check artists
   mem.move(None, mem.pname('Liked Songs Remixed'), lst)

   return


if __name__ == '__main__':

   """
   add spotify to youtube
   """
   # # try:
   # yt_lib_plsts = ytc.get_library_playlists()
   # # except:
   # #    print('500')
   # #    exit()
   # jprint([p['title'] for p in yt_lib_plsts])
   # # print(len(yt_lib_plsts)) 
   # # p_your_likes = [p for p in yt_lib_plsts if 'Your Likes' in p['title']][0]
   # p_sp_likes = [p for p in yt_lib_plsts if 'Spotify Liked Songs' in p['title']][0]
   # # jprint(p_sp_likes) 
   # p_sp_likes_id = p_sp_likes['playlistId'] # 'LM'
   # # print(p_sp_likes_id)
   
   
   p_sp_likes_id = 'PLnWpdynGEi50UuntxYhcnfWcvmBIiA1cD'
   additions = []
   #! liked = ytc.get-platilst_tracks()
   skipped = [
      'Conquer the World',
      'Tell Her You Love Her',
      'All Night Long',
      'Eternal Youth',
      'Between Two',
      'Fair Trade (with Travis Scott)',
      'Memphis',
      'More Than Friends'
   ]
   #! remove ( info ), Acoustic
   if os.path.exists('tmp.json'):
      with open('tmp.json', 'r') as f:
         skipped = json.load(f)
   for s in mem.saved[3:]:

      if s['track']['name'] in skipped:
         print('Skipping: ', s['track']['name'])
         continue
      # jprint(s)
      
      #search & filter
      system('clear')
      tracks = getYTrack(s) #! len varies
      if not tracks:
         skipped.append(s['track']['name'])
         with open('tmp.json', 'w+') as f:
            json.dump(skipped, f)
         print('Skipping')
         print()
         continue

      jprint(tracks)
      #! internal check for duplicates
      # if track['videoId'] not in liked
      # additions.append(track['videoId'])
      # jprint(additions)

      # add to library - Status String and a dict containing the new setVideoId for each videoId or full response
      # jprint(
      for t in tracks:
         ytc.add_playlist_items(
            #playlistId=
            p_sp_likes_id,
            # "LM",
            # "PLnWpdynGEi51a8HbUtMQ0QxPOqzZE3dGQ", #_Useful
            # additions,
            [t['videoId']]# for t in tracks]
            # [
            #    "BDtJWdTn60g",
            #    "hwsS5ZdY02w"
            # ],
            # None, # dont ad from another playlist
            # False #no duplicates
         )#)
   """
   {
   "status": "STATUS_SUCCEEDED",
   "playlistEditResults": [
      {
         "videoId": "BDtJWdTn60g",
         "setVideoId": "025D37676685A8DA",
         "multiSelectData": {
         "multiSelectParams": "CAESIlBMbldwZHluR0VpNTFhOEhiVXRNUTBReFBPcXpaRTNkR1E=",
         "multiSelectItem": "Ch8KC0JEdEpXZFRuNjBnEhAwMjVEMzc2NzY2ODVBOERB"
         }
      },
      {
         "videoId": "hwsS5ZdY02w",
         "setVideoId": "2F543702F0FEC48B",
         "multiSelectData": {
         "multiSelectParams": "CAESIlBMbldwZHluR0VpNTFhOEhiVXRNUTBReFBPcXpaRTNkR1E=",
         "multiSelectItem": "Ch8KC2h3c1M1WmRZMDJ3EhAyRjU0MzcwMkYwRkVDNDhC"
         }
      }
   ]
   }
   """

   
   exit()



   """
   add youtube to spotify
   """
   lib = ytc.get_library_songs(limit=500)
   # jprint([t['title'] for t in lib])
   print(len(lib))
   
   liked = ytc.get_liked_songs()
   jprint([*liked])
   trackCount = liked['trackCount']
   print(trackCount)
   tracks = liked['tracks']
   print(len(tracks))
   # assert trackCount == len(tracks) # trackCount is wrong
   # jprint([t['title'] for t in lib])
   
   # for y in lib:
   #    getSTrack()
   #    mem.move()
   
   
   
   
   pass