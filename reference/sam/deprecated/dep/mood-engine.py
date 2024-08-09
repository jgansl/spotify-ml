from base import sp, jprint
from time import sleep
import os
import json

# new databse with artist - popuplarirty related artists, users, playlists
# build network - train ai on lyrics
# impliciylu follow spotify playlists - made for you, friends


# remove songs older than 2021 out of liked songs - use to train new song sorting
# use 



# genres - cache past 2 & years

# new artists ->  explore -> related artists -> add to new artists
class ArtistRelations:
   def __init__(self):
      self.map = {}

   def add_artist(self, artist_name):
      if artist_name not in self.map:
         self.map[artist_name] = []

   def add_relationship(self, artist1, artist2):
      if artist1 in self.map and artist2 in self.map:
         self.map[artist1].append(artist2)
         self.map[artist2].append(artist1)

   def get_related_artists(self, artist_name):
      if artist_name in self.map:
         return self.map[artist_name]
      else:
         return None

followed_artists = []
artists = []
artists_ids = []

# def paginate():

#for a in followed_artists:
#   print(a['name'])

#youtube
#sp.recommendation_genre_seeds()
#sp.recommendations(seed_artists=None, seed_genres=None, seed_tracks=None, limit=20, country=None, **kwargs)
if __name__ == '__main__':
   artists = []
   artists_ids = []
   
   if not os.path.exists('db/artists.json'):
      tmp = sp.current_user_followed_artists(50)
      while tmp['artists']['next'] != None:
         artists.extend(tmp['artists']['items'])
         print(len(artists))
         tmp = sp.next(tmp['artists'])
         sleep(0.1)

      with open('db/artists.json', 'w') as f:
         json.dump(artists, f, indent=2)
   else:
      with open('db/artists.json', 'r') as f:
         artists = json.load(f)

   artists_ids = [a['id'] for a in artists]
   for a in artists:#[:1]:
      sp.user_unfollow_artists([a['id']])
      # res = sp.artist_related_artists(a['id'])
      # jprint(len(res['artists']))

