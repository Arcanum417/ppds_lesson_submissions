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
        if shared.counter >= shared.end:
            break
        shared.mutex.lock() #If I set the lock too late and don't consider that even reading the shared resource contitutes entering the critical area, the other thread will overflow the index between the check and the use of the index and this one will throw an Exception "IndexError: list index out of range" on the next line.
        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock() #I unset the lock as soon as I exit the critical section


for _ in range(10):
    sh = Shared(1_000_000)
    t1 = Thread(counter, sh)
    t2 = Thread(counter, sh)

    t1.join()
    t2.join()

    print(Histogram(sh.array)) #The ouput is {1: 1000000} and one of the threads will throw IndexError: list index out of range.
