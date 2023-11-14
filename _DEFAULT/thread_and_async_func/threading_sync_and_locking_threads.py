import threading
import time

# subclass for threading 'Thread Class'.
# You can create any number of these classes.
class myThread_1(threading.Thread):
    def __init__(self, threadId, name, count):
        # setup thread to handle new threads. Inherit from threading class 'threading.Thread.__init__(self)'
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.count = count

    # this needs to be called "run",
    # this starts thread and defines what thread will do
    def run(self):
        print("Starting: " + self.name + "\n")
        # lock thread, if you won't release thread in will be locked and
        # won't finish till you unlock it
        threadLock.acquire()
        print_time(self.name, 1, self.count)
        # release lock then thread is finished
        threadLock.release()
        print("Exiting: " + self.name + "\n")

class myThread_2(threading.Thread):
    def __init__(self, threadId, name, count):

        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.count = count


    def run(self):
        print("Starting: " + self.name + "\n")
        # this will check if any other threads is locked and when locked threads
        # finish it will unlock and continue.
        # if there is no other threads locked, this will just start "print_time"
        # In this sample "myThread_1" print_time() is locked, so it waits for it to be finished
        # and then it will continue "myThread_2" execution
        threadLock.acquire()
        threadLock.release()
        print_time(self.name, 1, self.count)
        print("Exiting: " + self.name + "\n")


def print_time(name, delay, count):
    while count:
        time.sleep(delay)
        print(f"{name}: {count}" + "\n")
        count -= 1


threadLock = threading.Lock()

thread_1 = myThread_1(1, "Processing Payment", 5)
thread_2 = myThread_2(2, "Send E-mail", 10)
thread_3 = myThread_2(2, "Load New Page", 3)

thread_1.start()
thread_2.start()
thread_3.start()

thread_1.join()
thread_2.join()
thread_3.join()



print("Finished threading")