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
        shared.mutex.lock()
        if shared.counter >= shared.end:
            shared.mutex.unlock()
            break
        shared.mutex.unlock() #If I devide the critical section into two, the other thread (not in every instance as with variant_2) can still overflow the index between the check and use.
        shared.mutex.lock()
        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


for _ in range(10):
    sh = Shared(1_000_000)
    t1 = Thread(counter, sh)
    t2 = Thread(counter, sh)

    t1.join()
    t2.join()

    print(Histogram(sh.array)) #The ouput is {1: 1000000} and there is a chance that one of the threads throws IndexError: list index out of range
