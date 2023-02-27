import queue
import concurrent.futures as futures
import threading
import time

from loguru import logger

# max limit
# success get, failed put
# q_total = queue.Queue(100)
# q_success = queue.Queue(5)
# semaphore = threading.Semaphore(5)
# q_success = queue.Queue(5)
lock = threading.Lock()
max_limit_cnt = 10
tried_cnt = 0
success_cnt = 0


def fake(cnt):
    global success_cnt
    global tried_cnt
    while tried_cnt < max_limit_cnt and success_cnt < cnt:
        for i in 'q13bbed31':
            if i.isdigit():
                if success_cnt == cnt:
                    break
                if tried_cnt == max_limit_cnt:
                    break
                lock.acquire()
                success_cnt += 1
                print(f'{threading.current_thread().name}-success-{success_cnt}')
                lock.release()
            lock.acquire()
            tried_cnt += 1
            lock.release()


if __name__ == '__main__':
    with futures.ThreadPoolExecutor(max_workers=3, thread_name_prefix="Pecker") as executor:
        executor.submit(fake, 30)
