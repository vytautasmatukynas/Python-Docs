import threading
import time

# subclass for threading 'Thread Class'.
# You can create any number of these classes.
class myThread_1(threading.Thread):
    def __init__(self, threadId, name, count):
        # setup thread. To hHandle new threads
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.count = count

    # this needs to be called "run",
    # this starts thread and defines what thread will do
    def run(self):
        print("Starting: " + self.name + "\n")
        # func to run in thread
        print_time(self.name, 1, self.count)
        print("Exiting: " + self.name + "\n")


class myThread_2(threading.Thread):
    def __init__(self, threadId, name, count):
        # setup thread. To hHandle new threads
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.count = count

    # this needs to be called "run",
    # this starts thread and defines what thread will do
    def run(self):
        print("Starting: " + self.name + "\n")
        # func to run in thread
        print_time(self.name, 1, self.count)
        print("Exiting: " + self.name + "\n")


def print_time(name, delay, count):
    while count:
        time.sleep(delay)
        print(f"{name}: {count}" + "\n")
        count -= 1

thread_1 = myThread_1(1, "Thread_1", 5)
thread_2 = myThread_1(2, "Thread_2", 8)
thread_3 = myThread_2(1, "Thread_3", 3)
thread_4 = myThread_2(2, "Thread_4", 12)

thread_1.start()
thread_2.start()
thread_3.start()
thread_4.start()

thread_1.join()
thread_2.join()
thread_3.join()
thread_4.join()

print("Finished threading")
