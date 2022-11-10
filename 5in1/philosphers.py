from typing import DefaultDict
import time
import threading
import datetime
from random import randint


print_lock = threading.Lock()


def roundTime(dt=None, roundTo=1):
    """Round a datetime object in seconds
    dt : datetime.datetime object, default now.
    roundTo : Closest number of seconds to round to, default 1 second.
    """
    if dt == None:
        dt = datetime.datetime.now()
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + roundTo / 2) // roundTo * roundTo
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)


class chopstick:
    def __init__(self):
        self.lock = threading.Lock()
        self.picked = self.lock.locked
        self.pick = self.lock.acquire
        self.drop = self.lock.release


class Philosopher(threading.Thread):
    def __init__(
        self, id: str, capacity: int, chopstick_l: chopstick, chopstick_r: chopstick
    ):
        threading.Thread.__init__(self)
        self.id, self.capacity = f"{id}", capacity
        self.chopstick_l, self.chopstick_r = chopstick_l, chopstick_r
        self.bar = capacity
        self.att = 0

    def run(self):
        return threading.Thread(target=self.think, args=())

    def think(self, rest=0.3):
        time.sleep(rest)
        self.hungry()
        pass

    def hungry(self):
        self.eat()
        pass

    def eat(self):

        self.chopstick_l.pick()

        if self.chopstick_r.picked():
            self.chopstick_l.drop()
            self.think()

        else:
            self.chopstick_r.pick()

            with print_lock:
                print(self.id, "eating")

            now = time.time()
            time.sleep(self.capacity)

            with print_lock:
                new = time.time()
                print(
                    f"{self.id} done eating {roundTime(datetime.datetime.fromtimestamp(now))} to {roundTime(datetime.datetime.fromtimestamp(new))} => {new-now}"
                )

            self.chopstick_l.drop()
            self.chopstick_r.drop()
            self.att += 1

            if self.att < 5:
                self.think(self.capacity)


def main(philosophers: dict):
    chopsticks = [chopstick() for i in range(len(philosophers))]
    queue = []

    for philosopher, stick in zip(philosophers, range(len(chopsticks))):
        queue.append(
            Philosopher(
                philosopher,
                philosophers[philosopher],
                chopsticks[stick - 1],
                chopsticks[stick],
            )
        )

    queue = [i.run() for i in queue]

    for i in queue:
        i.start()
    for i in queue:
        i.join()


names = ["marx", "lenin", "mao", "rodney", "fanon"]
philosophers = {names[i]: randint(5, 30) for i in range(len(names))}
main(philosophers)
