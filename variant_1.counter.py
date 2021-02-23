#bodies of functions, core functionality used under LICENSE.third_party
from fei.ppds import Thread, Mutex


class Shared():
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end
        self.mutex = Mutex()


class Histogram(dict):
    def __init__(self, seq=[]):
        for item in seq:
            self[item] = self.get(item, 0) + 1


def counter(shared):
    while True:
        shared.mutex.lock() #I set lock before accessing a common resource - entering a critical section
        if shared.counter >= shared.end:
            shared.mutex.unlock() #I need to unset the lock if this condition is met too, otherwise I would exit the loop and thread without ever unsetting the lock. At this point I have exited a critical section and I will terminate the loop in a next step, this is the last point when I can unset the lock.
            break
        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock() #I unset the lock as soon as I exit the critical section


for _ in range(10):
    sh = Shared(1_000_000)
    t1 = Thread(counter, sh)
    t2 = Thread(counter, sh)

    t1.join()
    t2.join()

    print(Histogram(sh.array)) #The ouput is {1: 1000000} as the lock assures that the 2 threads access the shared resources orderly
