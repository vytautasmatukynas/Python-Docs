import asyncio


"""Asyncio vs threading: Async runs one block of code at a time
while threading just one line of code at a time. With async,
we have better control of when the execution is given to other
block of code but we have to release the execution ourselves.

In addition, another situation when async may not be useful is
when you have a single database server not utilizing connection
pooling. If all requests hit the same database using a long
running connection, it won't make a difference if the calls
are asynchronous or synchronous.

If you have any I/O-bound needs (such as requesting data from a network,
accessing a database, or reading and writing to a file system),
you'll want to utilize asynchronous programming. You could also
have CPU-bound code, such as performing an expensive calculation,
which is also a good scenario for writing async code."""

# BASIC ASYNC SAMPLE_1 <---------
# create async function with "async"
async def sample():
    # executes this
    print('ooooooo_1')
    # then waits for this to finish
    await sample_2("aaaaaa")
    # then exucutes this
    print("finish")

async def sample_2(text):
    print(text)
    # 'await' is async element and run routine to sleep for 1 second
    await asyncio.sleep(1)

# create event-loop and run async func
asyncio.run(sample())

########## BASIC ASYNC SAMPLE_2 'create_task' ########################
# create async function with "async" with task
list_val = ["a", "b", "c"]
async def sample():
    # executes this
    print('ooooooo_1')
    # this is executing in background
    task = asyncio.create_task(sample_2(*list_val))
    # wait for task to finish. Without this it won't wait and execute "finish"
    await task
    # then exucutes this
    print("finish")

async def sample_2(*text):
    for text_item in text:
        print(text_item)
    # 'await' is async element and run routine to sleep for 1 second
    await asyncio.sleep(2)

# create event-loop and run async func
asyncio.run(sample())


