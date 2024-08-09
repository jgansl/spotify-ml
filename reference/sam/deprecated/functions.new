import concurrent.futures

"""
function that takes another function, a set or args, and a set of kwargs
and performs the function concurrently
"""
def concurrent(func, *args, **kwargs):
   with concurrent.futures.ThreadPoolExecutor() as executor:
      future = executor.submit(func, *args, **kwargs)
      return future.result()


## grab all playlists from pocketbase table names playlists
# playlists = retrieve(PLAYLIST)

## write a test to time the time it takes to run a funciton on an average of 10 runs
def test(func, *args, **kwargs):
   # use timing decorator
   start = time()
   for i in range(10):
      func(*args, **kwargs)
   end = time()
   print('time:', end - start)
   return

if __name__ == '__main__':

   pass