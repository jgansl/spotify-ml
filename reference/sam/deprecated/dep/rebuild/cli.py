from functions import *

# from pocketbase import PocketBase
# from pocketbase.client import ClientResponseError
# pb = PocketBase('http://127.0.0.1:8092', 'en-US')


def listGenres():
   jprint(sp.recommendation_genre_seeds()['genres'])

def listPlaylistDescriptions():
   return

# https://spotipy.readthedocs.io/en/2.22.1/#spotipy.client.Spotify.recommendations 
def listRecommendations():
   # recommendations(
   #     seed_artists=None, 
   #     seed_genres=None, 
   #     seed_tracks=None, 
   #     limit=20, 
   #     country=None, 
   #     **kwargs
   # )
   jprint(sp.recommendations())

def showArtist():
   artist = input('Artist Name: ')
   print("Artist: " + artist)

def _prompt(fns):
   print()
   print(" ######################################## ")
   for i, value in enumerate(fns):
      print(f"#  {i}. {value.__name__}  ")
   print(" ######################################## ")
   print()

if __name__ == '__main__':
   # pprint(globals())
   functions = [
      listGenres,
      listPlaylistDescriptions,
      listRecommendations,
      showArtist,
   ]

   while 1:
      _prompt(functions)

      choice = input('Choice: ')
      if choice.isdigit():
         functions[int(choice)]()
      else:
         print("Invalid choice: " + choice)