# dining philosophers problem
# 5 philosophers, 5 forks, 5 chopsticks
# each philosopher needs 2 chopsticks to eat

import threading
import time
import random

class Philosopher(threading.Thread):
    def __init__(self, name, left, right):
        threading.Thread.__init__(self)
        self.name = name
        self.left = left
        self.right = right
    
    def run(self):        
        while True:
            print(self.name, 'is hungry')
            self.dine()
    
    def dine(self):
        fork1, fork2 = self.left, self.right
        
        while self.left.locked():
            time.sleep(0.1)
        self.left.acquire()
        print(self.name, 'got left fork')
        
        while self.right.locked():
            time.sleep(0.1)
        self.right.acquire()
        print(self.name, 'got right fork')
        
        self.dining()
        self.left.release()
        self.right.release()
    
    def dining(self):
        print(self.name, 'is eating')
        time.sleep(random.uniform(3,13))
    
def main():
    forks = [threading.Lock() for n in range(5)]
    names = ('Engels', 'Lenin', 'Nkrumah', 'Marx', 'Rodney')
    
    philosophers = [Philosopher(names[i], forks[i%5], forks[(i+1)%5]) for i in range(5)]
    
    random.seed(507129)
    Philosopher.running = True
    for p in philosophers: p.start()
    time.sleep(100)
    Philosopher.running = False
    print('done')

if __name__ == '__main__':
    main()