import os
import signal
from multiprocessing import Process, Event
from threading import Timer
from random import random
from time import time, sleep

should_run = True
load_factor = float(os.getenv('LOAD_FACTOR', 0.1))
threads = int(os.getenv('THREAD_COUNT', os.cpu_count()))
frequency = 1000

def generate_load(ms: int):
    now = int(time() * 1000)
    result = 0
    while True:
        result += random() * random()
        if (int(time() * 1000) > now + ms):
            return

def worker(shutdown_event: Event):
    while True:
        if shutdown_event.is_set():
            print('worker exiting')
            break
        generate_load(frequency * load_factor)
        sleep(frequency * (1 - load_factor) / 1000)
        
def start():
    shutdown = Event()

    def handle_noop(signum, frame):
        return
    def handle_shutdown(signum, frame):
        shutdown.set()
        sleep(frequency / 1000)
    
    # worker signals
    signal.signal(signal.SIGTSTP, handle_noop)
    signal.signal(signal.SIGTERM, handle_noop)
    signal.signal(signal.SIGINT, handle_noop)
    
    # setup workers
    for i in range(threads):
        p = Process(name=f"Worker-{i:02d}", daemon=True, target=worker, args=[shutdown])
        p.start()

    # main signals
    signal.signal(signal.SIGTSTP, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_noop)
    
    
if __name__ == '__main__':
    print(f'Generating CPU load on {threads} threads at {load_factor} load factor')
    start()