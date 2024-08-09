import concurrent.futures

from datetime import datetime
# from pydash import flatten
from random import shuffle

from _constants import *
from _functions import *
from _utilities import *

def adjustYears():
   lst = [
         '10s',
         '2020',
         '2021',
         '2022',
         '2023',
         '2024'
      ]
   for pname1 in lst:
      for pname2 in lst:
         if pname == pname2:
            continue
         p1 = getPlaylist(pname1)
         p2 = getPlaylist(pname2)
         intersection - list( set( p1['tracks'] ).intersection( set( p2['tracks'] ) ) )
         move(p1['id'], p2['id'], intersection)


   return

_playlists = retrieve(PLAYLIST)
def getPlaylist(pname):
   #search pb
   #check for more than 1
   #if not found, retrieve and insert, return resulting record - only happens if created after run start
   #check for more than 1
   return
def getPlaylists(invalidate=False):
   global _playlists
   if not _playlists:
      _playlists = retrieve(PLAYLIST)
   return _playlists


def scanInPlaylists(): #sync


   return
