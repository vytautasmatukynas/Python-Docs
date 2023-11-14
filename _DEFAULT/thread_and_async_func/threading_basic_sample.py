import time
import threading

# Run Code Concurrently <----------------
# SIMPLE THREADS <---------------
#########################################
# launch counter to mesure how long this app.py takes to executing
start = time.perf_counter()

def do_something():
    print(f'sleep 1secs')
    time.sleep(1)
    print('done sleeping')

# create simple threads
thread_1 = threading.Thread(target=do_something)
thread_2 = threading.Thread(target=do_something)

# start threads
thread_1.start()
thread_2.start()

# this will ensure that all threads complete before moving to the "finish"
# comment .joint() and try it with out .join()
thread_1.join()
thread_2.join()

# launch counter to mesure how long this app.py takes to executing
finish = time.perf_counter()
# prints time of app.py executing
print(f"Finished in {round(finish-start, 2)} seconds")
#############################################

# <OR>
# LOOPING THRU THREADS <-------------------
#############################################

# launch counter to mesure how long this app.py takes to executing
start = time.perf_counter()

def do_something(second):
    print(f'sleep {second} secs')
    time.sleep(second)
    print('done sleeping')

# using threads in for loop. Can use .join() in loop.
# You have to create list of threads then loop that list
# and then .join() every thread
# 'args' is arguments that dunc should take, same as 'do_something(1.5)' just
# this one is inside thread
threads_list = []
for _ in range(10):
    threads = threading.Thread(target=do_something, args=[1.5])
    threads.start()
    threads_list.append(threads)

for thread in threads_list:
    thread.join()

# launch counter to mesure how long this app.py takes to executing
finish = time.perf_counter()
# prints time of app.py executing
print(f"Finished in {round(finish-start, 2)} seconds")
###################################################