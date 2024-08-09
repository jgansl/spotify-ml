"""
-x filtering liked songs into #spotify-genres
- remove liked songs in #spotify-genre weekly
- remove _library in #spotify-genre weekly
- pi - listen; weekyl sync
-? corss containment - new genres
- remove _cache from _library
- remove _cache from #spotify-genre
- artists pb -> rec artists, rec, new->genres channels
- 

# INTEGRATIONS
- move saved to library
- remove two week old, remove frm library if in genre
- tagging system so script does not have to be manually updated
- genre new
- k clustering new sorting and library sorting
- cross api refrenecing 
- ytm sycning
- new sorting by artists - new, spotify genre, and training - auto update playlists labeled #artists
- check artists for new tracks ... personal release radar
- remove classics from nostalgic
- sort library by a single audio attribute

- ml crossrefernce audio attribution information
- check for new mixes every day - can this be automate; optimized; similar playlist - radio; fine tuning reommendation seeding; listen by artist - exploration; pb - daily
- sort library by release date
- pb library - restore destrcutive removal - was liekd attribute
- continually add to cache (dups) and max 10,000 - most frequent will stay cached - but be present ni spotify - pb
- year mixes auto move from library
"""
from datetime import datetime
from os import system
from time import sleep
from pydash import flatten
import re

from functions import SAM, sp, jprint, mem, TRACK, SAVED, usr

from pocketbase import PocketBase

"""
#reservedVariables: 
- p 
- t
- track_ids
- tids, tid, sid, s
"""

TAGS = [
    '#cache',
    '#artist-cache',
    '#genre-cache',
    '#genre-new',
    '#genre-spotify',
    '#spotify-genre',
    '#playlist',
    '#personal',
    '#library',
    '#nostalgic',
    '#testdata'
]

DAE   = 'Dance/Electronic'
DAB   = 'Drums and Bass'
FAA   = 'Folk & Acoustic'
HOUSE = 'House'
INDIE = 'Indie'
POP   = 'Pop'
SAVED = 'saved'

#TODO; use to break up library
genreChanneling = [
    'brooklyn indie'
]


def unknownA():
    '''
    remove liked from saved...
    '''

def genreCache():
    '''
    remove old songs into a cache
    pb - labeling and removal
    '''
    return

def personalize():
    '''
    remove personal from library
    '''

    return

def ytm():
    return

def travelingSaleman():
    return

def saveToLibrary(): #function to automate everything
    '''auto move svae library'''
    return

def cacheOldSaved():
    '''
    remove genres
    move 2 week old to _library
    '''
    return

def fetchYoutube():
    return

def kClusterNew():
    '''goal be able to dynamically restart, regenerate, and sync to youtube'''
    return

def mvLibToLiked():
    

    return

#
#
#
#
#
#


lib = mem.pname('_library')
def likedLibrarySync():
    mem.move(
        None,  
        lib['id'], 
        mem.diff(
            mem.sids, 
            mem.get_track_ids(lib)
        )
    )
    return

numdays = 28
def rmNostaligaFromSaved():
    return
def rmPersonalCacheFromLibrary():
    global lib
    print('rmPersonalCacheFromLibrary') #logging
    
    tids = mem.get_track_ids(lib)
    for p in [p for p in mem.playlists if '#cache' in p['description'] or '#genre-cache' in p['description'] or '#playlist' in p['description'] or '#personal' in p['description'] or '#nostalgic' in p['description']]:
        if p['name'] == lib['name']: #guard
            continue
        mem.move(
            lib['id'],
            None,
            mem.intersect(
                tids,
                mem.get_track_ids(p),
            )
        )


    print() #logging
    return
# @see https://www.geeksforgeeks.org/python-datetime-strptime-function/
format_data = "%Y-%m-%dT%H:%M:%SZ"#.%f" # 2023-02-25T22:29:06Z
now = datetime.utcnow()
def rmSpotifyGenreFromOldLiked(): 
    """
    prevents the need for a library
    """

    print('rmSpotifyGenreFromOldLiked') #logging
    global numdays, now

    spotifyGenres = [p for p in mem.playlists if '#spotify-genre' in p['description']]
    for p in spotifyGenres: #e.submit
        print(p['name']) #logging
        tids = mem.get_track_ids(p)
        for s in mem.saved:
            sid = s['track']['id']
            print(
                (now - datetime.strptime(s['added_at'], format_data)).days,
                s['track']['name'], 
                '\t',
                s['added_at'],
                # datetime.strptime(s['added_at'], format_data),
            )
            # print(now)
            if(
                (now - datetime.strptime(s['added_at'], format_data)).days >= numdays
                and sid in tids
            ):
                # remove from SAVED
                mem.move( 
                    SAVED, 
                    None, 
                    [sid]
                )
        # input('Continue?')
        # sleep(2)
        # e.submit(
        mem.resave() # resync/update mem.saved and mem.sids
        sleep(3)


    print() #logging
    return
def rmSpotifyGenreFromLibrary(): 
    global lib
    print('rmSpotifyGenreFromLibrary') #logging
    lib_tids = mem.get_track_ids(lib)
    spotifyGenres = [p for p in mem.playlists if '#spotify-genre' in p['description']]
    for p in spotifyGenres: #e.submit
        print(p['name']) #logging
        mem.move(
            lib['id'],
            None,
            mem.intersect(
                lib_tids,
                mem.get_track_ids(p)
            )
        )
    
    
    print() #logging
    return
def rmOldSaved():
    global lib, now
    print('rmOldSaved')
    lib_tids = mem.get_track_ids(lib)
    for s in mem.saved:
        sid = s['track']['id']
        print(
            s['track']['name'],
            (now - datetime.strptime(s['added_at'], format_data)).days,
            # s['added_at']
        )
        if(
            (now - datetime.strptime(s['added_at'], format_data)).days > numdays
            and sid in lib_tids
        ):
            mem.move(
                None, #SAVED,
                lib['id'],
                mem.diff(
                    [sid],
                    lib_tids
                )
            )
            mem.move(
                SAVED,
                None, #lib['id'],
                [sid]
            )
        # update lib_tids (if global)

    print() #logging
    return
def mvRemixedSongs():
    """
    """
    return
newChanneling = { #TODO
    "Fresh Finds Dance": DAE,
    'Infinite Indie Folk': FAA,
    'House Party': HOUSE,
}
genre_mixes = [ #pb implicitly follow
    'Chill Future Funk Mix',
    'Dance/Electronic Mix',
    'Dance House Mix',
    'Deep Tropical House Mix',
    'Deep House Mix',
    'Drum and Bass Mix',
    'Experimental Bass Mix',
    'Focus Deep House Mix',
    'Folk & Acoustic Mix',
    'Futurepop Mix',
    'Future Garage Mix',
    'Future House Mix',
    'Hip Hop Mix',
    'House Mix',
    'Indie Mix',
    'Pop Mix',
    'Progressive House Mix',
    'Vapor Soul Mix',
    'Vapor Twitch Mix',
    'Wake Up Mix',
]
def genreExtract(): 
    "diffrers from rmSpotifyGenre as this check the spotify owned playlist rather than than the personal?"
    global lib
    print('genreExtract')
    for z in genre_mixes: #! 2010 -> _cache
        print(z)
        tmpp = mem.pname('_'+re.sub(' Mix', '', z))
        tmplist = mem.diff(
            mem.intersect(
                mem.sids, 
                mem.get_track_ids(mem.pname(z))
            ),
            mem.get_track_ids(tmpp),
        )
        print(len(mem.intersect(
                mem.sids, 
                mem.get_track_ids(mem.pname(z))
            )))
        print(len(tmplist))
        #! mem.move(lib['id'], None, mem.intersect( mem.sids, mem.get_track_ids(mem.pname(z)) ))
        mem.move(None, tmpp['id'], tmplist)
        tmplist = mem.diff(
            mem.intersect(
                mem.get_track_ids(lib),
                mem.get_track_ids(mem.pname(z))
            ),
            mem.get_track_ids(tmpp),
        )
        print(len(tmplist))
        mem.move(lib['id'], tmpp['id'], tmplist)
    """
    genreExtract
    Chill Future Funk Mix
    7
    3
    0
    Dance/Electronic Mix
    5
    1
    0
    Dance House Mix
    20
    16
    0
    Deep Tropical House Mix
    10
    1
    0
    Deep House Mix
    12
    8
    0
    Drum and Bass Mix
    19
    15
    0
    Experimental Bass Mix
    7
    2
    0
    Focus Deep House Mix
    19
    14
    0
    Folk & Acoustic Mix
    0
    0
    0
    Futurepop Mix
    8
    3
    0
    Future Garage Mix
    7
    4
    0
    Future House Mix
    12
    8
    0
    Hip Hop Mix
    3
    1
    0
    House Mix
    2
    1
    0
    Indie Mix
    2
    1
    0
    Pop Mix
    4
    1
    0
    Progressive House Mix
    23
    16
    0
    Vapor Soul Mix
    16
    9
    0
    Vapor Twitch Mix
    20
    8
    0
    Wake Up Mix
    7
    1
    0
    """
    print()
    return
def genreNew():
    """
    """
    print('genreNew')
    for z in genre_mixes: #pb implicitly follow
        print(z)
        tmpp = mem.pname(re.sub('Mix', 'New', z))
        tmplist = mem.diff(mem.diff(mem.get_track_ids(mem.pname(z)), [*db]), mem.get_track_ids(tmpp))
        mem.move(None, tmpp['id'], tmplist)
    
    p_new = mem.pname('New', create=True)
    for z in [ #pb implicitly follow
        'Release Radar',
        'Discover Weekly',
        'Daily Mix 1',
        'Daily Mix 2',
        'Daily Mix 3',
        'Daily Mix 4',
        'Daily Mix 5',
        'Daily Mix 6',
        'Monday Mix',
        'Tuesday Mix',
        'Wednesday Mix',
        'Thursday Mix',
        'Friday Mix',
        'Saturday Mix',
        'Sunday Mix',
        'Pixel Garden',
        'Bass Arcade',
        'Future Funk',
        # 'Futurs Hits'
    ]:
        tmplist = mem.diff(mem.diff(mem.get_track_ids(mem.pname(z)), [*db]), mem.get_track_ids(p_new))
        mem.move(None, p_new['id'], tmplist)
        # for tmpid in tmplist:
        #     sp.add_to_queue(tmpid)



    print()
    return
def searchRemixes():
    #YTM syncing  as well
    return

#
# develop DRY; test-mindset - destructive? lib -> test data set/subset
# refactor - performance and algorithms
if __name__ == '__main__': #TODO pi tasking - job scheduling
    # try:
    pb = PocketBase('http://127.0.0.1:8092', 'en-US')
    # except pocketbase.client.ClientResponseError:
    #    print('db not found')
    #    exit()
    # if 'db' not in st.session_state:
    #    print('init db')
    #    st.session_state.
    db = {}
    for i in pb.records.get_full_list('spotify'):
        #st.session_state.
        db[i.sid] = i

    # if 'device_id' not in st.session_state:
    devices = [d for d in sp.devices()['devices'] if d['is_active']]
    if len(devices):
        # st.session_state.
        device_id = devices[0]['id']
    TESTING = False
    if TESTING:
        rmOldSaved()
        # rmSpotifyGenreFromOldLiked()

        lib = mem.pname('_library (TEST)') #library was tagged as cached rm'ing all tracks
        # rmPersonalCacheFromLibrary()


        # searchRemixes()
        # rmPersonalCacheFromLibrary()
        # rmNostaligaFromSaved()

        exit()
    lib = mem.pname('_library')
    # move old saved into _library
    genreExtract()
    likedLibrarySync() #! READDING REMOVED SONGS - STAYS for another 2 weeks?
    rmOldSaved()  #move old saved to liked
    #! mvRemixedSongs()
    # rmSpotifyGenreFromOldLiked()
    rmSpotifyGenreFromLibrary()
    rmPersonalCacheFromLibrary()
    # rmOldSaved() #remove old liked which have already been placed in libary and readds oldest library backed into saved
    genreNew() #!listen/cleanup rm
    #! move liked into genre - auto
    #! rm heard from genre new
    #! dance pop - channeling
    #! rmHeardFromGenreNew()




    pass

# APP
"""
tempo control
attribute filtering in genre
pi remote
"""
