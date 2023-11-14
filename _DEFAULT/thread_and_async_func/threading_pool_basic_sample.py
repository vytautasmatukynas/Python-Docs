import time
import concurrent.futures


# Run Code Concurrently <----------------
# THREAD POOL <-------------------
#############################################
# launch counter to mesure how long this app.py takes to executing
start = time.perf_counter()

def do_something(second):
    print(f'sleep {second} secs')
    time.sleep(second)
    return 'done sleeping'

# create ThreadPool
with concurrent.futures.ThreadPoolExecutor() as executer:
    # execute func one of a time, use submit. '(func, argument)'
    thread_1 = executer.submit(do_something, 1)
    thread_2 = executer.submit(do_something, 1)

    # print result that is returned
    print(thread_1.result())
    print(thread_2.result())


# launch counter to mesure how long this app.py takes to executing
finish = time.perf_counter()
# prints time of app.py executing
print(f"Finished in {round(finish-start, 2)} seconds")


# Looping thru THREAD POOL
#############################################
# launch counter to mesure how long this app.py takes to executing
start = time.perf_counter()

def do_something(second):
    print(f'sleep {second} secs')
    time.sleep(second)
    return f'done sleeping {second}'

# create ThreadPool
with concurrent.futures.ThreadPoolExecutor() as executer:
    seconds = [5, 4, 8, 6]
    # # execute func ones at a time, use submit. '(func, argument)'
    # results = [executer.submit(do_something, sec) for sec in seconds]
    #
    # # loop over the results as they are completed
    # for f in concurrent.futures.as_completed(results):
    #     print(f.result())
    #
    # <OR> USE map()
    #
    results = executer.map(do_something, seconds)
    for result in results:
        print(result)


# launch counter to mesure how long this app.py takes to executing
finish = time.perf_counter()
# prints time of app.py executing
print(f"Finished in {round(finish-start, 2)} seconds")