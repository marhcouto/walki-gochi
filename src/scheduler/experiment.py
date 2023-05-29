import os
import time
from threading import Thread, get_native_id


def test_a():
    param = os.sched_param(os.sched_get_priority_max(os.SCHED_FIFO))
    os.sched_setscheduler(0, os.SCHED_FIFO, param)
    n = 0
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print("Child 1 start:", get_native_id(), current_time)
    for i in range(1000000000):
        n += i
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print("Child 1 end:", get_native_id(), current_time)
    os.sched_yield()

def test_b():
    param = os.sched_param(os.sched_get_priority_max(os.SCHED_FIFO))
    os.sched_setscheduler(0, os.SCHED_FIFO, param)
    n = 0
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print("Child 2 start:", get_native_id(), current_time)
    for i in range(1000000000):
        n += i
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print("Child 2 end:", get_native_id(), current_time)
    os.sched_yield()
    

def test_c():
    param = os.sched_param(os.sched_get_priority_max(os.SCHED_FIFO))
    os.sched_setscheduler(0, os.SCHED_FIFO, param)
    n = 0
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print("Child 3 start:", get_native_id(), current_time)
    for i in range(1000000000):
        n += i
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print("Child 3 end:", get_native_id(), current_time)
    os.sched_yield()
    

if __name__ == "__main__": 
    t = Thread(target=test_a)
    t2 = Thread(target=test_b)
    t3 = Thread(target=test_c)
    print("Parent:", get_native_id())
    t.start()
    time.sleep(1)
    t2.start()
    t3.start()
    t.join()
    t2.join()
    t3.join()