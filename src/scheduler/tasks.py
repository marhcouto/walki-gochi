# import sys
# import time
import signal

def interrupt_handler(signum, frame):
    print("Handling signal {}".format(signum))


def test_task():
    signal.signal(signal.SIGINT, interrupt_handler)
    for i in range(100000000):
        if (i % 1000000 == 0):
            print("Task 1: {}".format(i))
