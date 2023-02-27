import queue
import concurrent.futures as futures
import threading
from loguru import logger

# max limit
# success get, failed put
# q_total = queue.Queue(100)
# q_success = queue.Queue(5)
# semaphore = threading.Semaphore(5)
# q_success = queue.Queue(5)
lock = threading.Lock()
success_cnt = 0
flag = 1


def fake():
    global success_cnt
    while flag or success_cnt > 5:
        for i in 'th1s2ff3ttt556':
            lock.acquire()
            if i.isdigit():
                success_cnt += 1
                lock.release()
            else:
                lock.release()


with futures.ThreadPoolExecutor(max_workers=3, thread_name_prefix="Pecker") as executor:
    for i in range(0, 10):
        executor.submit(fake)

while success_cnt > 5:
    flag = 0

print(success_cnt)
