import asyncio
import config
import psycopg2

params = config.sql_db

""" This script has sync and async functions. First script starts synchronously, then hits async 
functions loop and fetches data from SQL asynchronously, after finishing fetching data it continues 
synchronously and finish script"""

########### SYNC FUNC (normal fun)############
def counter_1():
    for i in range(0, 5):
        print(f"Sync_1: {i}")
###################################

########### BASIC ASYNC SAMPLE_3 'create_task' #####################
########### GETS DATA FROM 3 SQL DBR AT SAME TIME ####################
########### THIS IS USEFUL FOR REQUISTING FEW HTTP 'requests' or SQL DATA FECHING #################
########### CHECK 'aiohttp', FOR MULTIPLKE HTTP 'requests' HANDLING ##################
async def fetch_data():
    """ data fetching from 1st DB"""

    print("start fetching data from sql")
    # connecting to SQL
    con = psycopg2.connect(**params)
    cur = con.cursor()
    cur.execute(
        """SELECT id, company, client, phone_number, order_name,
        order_term, status, comments, update_date
        FROM orders 
        ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
    # fetching data from SQL
    query_start = cur.rowcount

    # this is just printing row number to see how data is fethed, but this could be any operation you want,
    # maybe some counting or whatever
    for num in range(0, query_start + 1):
        print({"ROW NUMBER 1": num})
        # this is just for wait 0.25s to see how numbers are counting
        await asyncio.sleep(0.25)
        # if value is "0" then wait till 'fetch_data_2()' will finish, in mean time 'fetch_data_2()'
        # and 'fetch_data_3()' will execute
        if num == 0:
            await fetch_data_2()

    con.close()

    print("data fetched")

    return {"RESULT": query_start}

async def fetch_data_2():
    """ data fetching from 2nd DB"""

    print("start fetching data from sql 2")
    con = psycopg2.connect(**params)
    cur = con.cursor()
    cur.execute(
        """SELECT id, company, client, phone_number, order_name,
        order_term, status, comments, update_date
        FROM orders 
        ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
    query_start = cur.rowcount

    # this is just printing row number to see how data is fethed, but this could be any operation you want.
    # maybe some counting or whatever.
    for num in range(0, query_start - 2):
        print({"ROW NUMBER <--  2": num})
        await asyncio.sleep(0.25)

    # some action after data is fetched. This just prints some text to see when data is fetched.
    # this could be any operation you want.
    print("data fetched2")

    return {"ROW NUMBER": query_start}


async def fetch_data_3():
    """ data fetching from 3nd DB"""

    print("start fetching data from sql 3")
    con = psycopg2.connect(**params)
    cur = con.cursor()
    cur.execute(
        """SELECT id, company, client, phone_number, order_name,
        order_term, status, comments, update_date
        FROM orders 
        ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
    query_start = cur.rowcount

    # this is just printing row number to see how data is fethed, but this could be any operation you want.
    # maybe some counting or whatever.
    for num in range(0, query_start + 1):
        print({"ROW NUMBER <----- 3": num})
        await asyncio.sleep(0.25)

    # some action after data is fetched. This just prints some text to see when data is fetched.
    # this could be any operation you want.
    print("data fetched 3")


async def main():
    """ main async func where all task goes and etc. and there is sample how return works in async func task handling"""
    # create tasks for async func
    task_1 = asyncio.create_task(fetch_data())
    task_2 = asyncio.create_task(fetch_data_2())
    task_3 = asyncio.create_task(fetch_data_3())


    # You have to set value so task if you want to RETURN normal result
    # with 'value = await task_1': <- this is 'Future'
    # "DATA": 1
    # with 'await task_2' you'll get:
    # <Task finished name='Task-2' coro=<fetch_data() done, defined at D:\Python\python-default\
    # threading_async_multiprocess\asyncio_await_basic_sample.py:62> result={'DATA': 1}>
    # with 'await task_3' and no RETURN statment you'll get:
    # TASK 2 RESULt: <Task finished name='Task-4' coro=<fetch_data_3() done, defined at
    # D:\Python\python-default\threading_async_multiprocess\async_fetch_data_from_3_DBs.py:69> result=None>


    # with asign value task
    value = await task_1
    print(f"TASK 1 RESULt: {value}")
    # with no asign value task
    await task_2
    print(f"TASK 2 RESULt: {task_2}")
    # func without return statment <---
    await task_3
    print(f"TASK 2 RESULt: {task_3}")

    # after all tasks are finish, this prints some text. This could be any operation you want, maybe UI filling, some
    # counting from two APIs or DBs or whatever you need to be.
    print("finished counting")

########### SYNC FUNC (normal fun)############
def counter_2():
    for i in range(0, 5):
        print(f"Sync_2: {i}")
###################################

counter_1()
## this creates ASYNC loop. You can asign this to button or whatever you like to. ##
asyncio.run(main())
####################################################################################
counter_2()