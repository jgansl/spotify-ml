import bokeh
import bokeh
import seaborn as sns

from os import system
from time import sleep
from pydash import flatten
import re

from functions import SAM, sp, jprint, mem, TRACK, SAVED

from concurrent.futures import ThreadPoolExecutor
ex = ThreadPoolExecutor(max_workers=25)

from pocketbase import PocketBase
from pocketbase.client import ClientResponseError
# try:
pb = PocketBase('http://127.0.0.1:8090', 'en-US') #else wirte to file to read next tiem -> pi
# except ClientResponseError:
#    exit
#lyrical analysis 
#genre sorting analysis