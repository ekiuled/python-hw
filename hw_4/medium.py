import math
from multiprocessing import cpu_count
from threading import current_thread
from concurrent.futures import ThreadPoolExecutor
from timeit import timeit
from typing import TextIO
from functools import wraps


def logged(f, log_file: TextIO):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print(f'{current_thread().name}\t\t{f.__name__}\t{args}\t{kwargs}', file=log_file, flush=True)
        return f(*args, **kwargs)
    return wrapper


def integrate(f, a, b, *, n_jobs=1, n_iter=1000, log_file: TextIO):
    step = (b - a) / n_iter
    with ThreadPoolExecutor(n_jobs) as executor:
        args = (a + i * step for i in range(n_iter))
        return sum(executor.map(logged(f, log_file), args)) * step


def time(n_jobs: int, *, log_file: TextIO, time_file: TextIO, timeit_number: int = 1):
    seconds = timeit(lambda: integrate(math.cos, 0, math.pi / 2, n_jobs=n_jobs, log_file=log_file),
                     number=timeit_number) / timeit_number
    print(f'{n_jobs}\t{seconds * 1000 :.3f} ms', file=time_file)


if __name__ == '__main__':
    cpu_num = cpu_count()
    with open('artifacts/medium/time.txt', 'w') as time_file:
        with open('artifacts/medium/log.txt', 'w') as log_file:
            for n_jobs in range(1, 2 * cpu_num + 1):
                time(n_jobs, log_file=log_file, time_file=time_file)
