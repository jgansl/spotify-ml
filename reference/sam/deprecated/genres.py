


def subgenres(): #! ranking
   sub = getPlaylist('Dark Indie Rock Mix')
   main = getPlaylist('Indie') # getPlaylist('Rock')

   lst = set(getTracks(main.sid).intersection(getTracks(sub.sid)))