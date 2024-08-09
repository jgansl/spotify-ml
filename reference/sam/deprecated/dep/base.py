from os import system
from time import sleep
import json

from _constants import (
   SCOPE, 
   PLAYLIST,
   SAVED,
   TRACK
)

jprint = lambda x: print(json.dumps(x, indent=4))


# from pocketbase import PocketBase
# from pocketbase.client import ClientResponseError
# pb = PocketBase('http://127.0.0.1:8092', 'en-US')