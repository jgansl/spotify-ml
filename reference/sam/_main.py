#! machine learning
#! refactor often

from _db import * # db, then external to spotify
from _functions import *
from _daily import privatizePlaylists
from random import shuffle


def backup():
   print("backup")

   return

def scanInPlaylists():
   return

#! collections sorted by release date
#! move to position zero if older before news; mass resort and add
#! cutoff date? - db track how many times added? - hidden, permanent remoeval
#! remove if older comes before it
#! hide after 9360 days if not in cycle? (disover added to liked songs)
#! cycle in from liked after 14 days
#! pi auto run

def scanInTracks():
   genres = [] # mark as genred so if removed, not readded
   daily = [
      'Daily Mix 1',
      'Daily Mix 2',
      'Daily Mix 3',
      'Daily Mix 4',
      'Daily Mix 5',
      'Daily Mix 6',
   ]
   for d in daily:
      #queue ungenred
      pass
   return


if __name__ == "__main__":
   # backup()

   # if playlist in db
   # move tracks to cache and unfollow playlist

   # scan artists for new songs - shuffle - k clustering

   scanInTracks()

   pass