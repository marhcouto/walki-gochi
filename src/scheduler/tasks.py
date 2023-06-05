
def test_task():
    for i in range(100000000):
        if (i % 1000000 == 0):
            print("Task 1: {}".format(i))
