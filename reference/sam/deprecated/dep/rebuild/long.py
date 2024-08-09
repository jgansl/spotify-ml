import queue
import threading
import time
from time import sleep
import sched
# from multiprocessing import Pool

# Define the function you want to call
def listen():
   print("Function called at", time.strftime("%H:%M:%S"))

# Define the function you want to call
def listen2():
   print("2Function called at", time.strftime("%H:%M:%S"))

def run_events():
   # Define your functions that will be called continuously
   def function1():
      print("Function 1: ", event_queue.qsize())
      event_queue.put(function1)

   def function2():
      print("Function 2: ", event_queue.qsize())
      event_queue.put(function2)
      event_queue.put(function2)

   # Create an event queue
   event_queue = queue.Queue()

   # Define a worker function that processes events from the queue
   def event_worker():
      while True:
         try:
            event = event_queue.get()
            event()  # Call the function
            event_queue.task_done()
            print('sleep')
            sleep(5)
         except queue.Empty:
            time.sleep(1)

   # Create and start a thread for event processing
   event_thread = threading.Thread(target=event_worker)
   event_thread.daemon = True
   event_thread.start()

   # Add functions to the event queue
   event_queue.put(function1)
   event_queue.put(function2)

   # You can add more functions to the queue as needed
   # event_queue.put(another_function)

   # Keep the program running
   try:
      while True:
         time.sleep(1)
   except KeyboardInterrupt:
      print("Exiting...")

# Create a scheduler
scheduler = sched.scheduler(time.time, time.sleep)

# Schedule the function to run at 1-minute intervals
interval = 3  # 60 seconds (1 minute)

def schedule_function():
   listen()
   scheduler.enter(interval, 1, schedule_function)

def schedule_function2():
   listen2()
   scheduler.enter(interval, 1, schedule_function)

# Schedule the first function call
scheduler.enter(interval, 1, schedule_function)
scheduler.enter(interval, 1, schedule_function2)
# scheduler.enter(interval, 1, run_events)

# Start the scheduler
print("Scheduling function to run at 1-minute intervals...")
scheduler.run()


# import sched, time
# s = sched.scheduler(time.monotonic, time.sleep)
# def print_time(a='default'):
#    print("From print_time", time.time(), a)

# def periodic(scheduler, interval, action, actionargs=()):
#    scheduler.enter(
#       interval, 
#       1, 
#       periodic,
#       ( 
#          scheduler, 
#          interval, 
#          action, 
#          actionargs
#       )
#    )
#    action(*actionargs)
# periodic(scheduler, 3600, 1)

# def print_some_times():
#    print(time.time())
#    s.enter(10, 1, print_time)
#    s.enter(5, 2, print_time, argument=('positional',))
#    # despite having higher priority, 'keyword' runs after 'positional' as enter() is relative
#    s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
#    # s.enterabs(1_650_000_000, 10, print_time, argument=("first enterabs",))
#    # s.enterabs(1_650_000_000, 5, print_time, argument=("second enterabs",))
#    s.run()
#    print(time.time())

# print_some_times()

# import asyncio, time

# async def say_after(delay, what):
#    await asyncio.sleep(delay)
#    print(what)
#    await say_after(1, 'hello')

# queue = [
#    1,
#    2,
#    3,
# ]
# async def main():
#    print(f"started at {time.strftime('%X')}")

# while queue.length:
#    await say_after(1, 'hello')
#    await say_after(2, 'world')

#    print(f"finished at {time.strftime('%X')}")

# asyncio.run(main())