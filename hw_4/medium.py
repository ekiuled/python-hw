import math
from multiprocessing import cpu_count, current_process
from threading import current_thread
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from timeit import timeit
from typing import TextIO
from datetime import datetime


def log(log_filename: str, current_function, job: int):
    with open(log_filename, 'a') as log_file:
        print(f'{datetime.now().strftime("%M:%S.%f")} {job} {current_function().name}', file=log_file, flush=True)


def log_start(log_filename: str, n_jobs: int):
    with open(log_filename, 'a') as log_file:
        print(f'\n{n_jobs} jobs', file=log_file, flush=True)


def integration_job(f, a: float, step: float, n_iter: int, n_jobs: int, job: int, log_filename: str, current_function):
    log(log_filename, current_function, job)
    xs = (a + i * step for i in range(job - 1, n_iter, n_jobs))
    return sum((f(x) for x in xs))


def integrate(f, a, b, *, n_jobs=1, n_iter=1000, log_filename: str, executor, current_function):
    log_start(log_filename, n_jobs)
    step = (b - a) / n_iter
    with executor(n_jobs) as pool:
        futures = [pool.submit(integration_job, f, a, step, n_iter, n_jobs, job, log_filename, current_function) for job in range(n_jobs)]
        return sum((future.result() for future in as_completed(futures))) * step


def time(n_jobs: int, *, log_filename: str, time_file: TextIO, timeit_number: int = 1, executor, current_function):
    seconds = timeit(lambda: integrate(math.cos, 0, math.pi / 2,
                                       n_jobs=n_jobs,
                                       n_iter=10 ** 8,
                                       log_filename=log_filename,
                                       executor=executor,
                                       current_function=current_function),
                     number=timeit_number) / timeit_number
    print(f'{n_jobs}\t{seconds:.3f} s', file=time_file)


if __name__ == '__main__':
    cpu_num = cpu_count()
    with open('artifacts/medium/time.txt', 'w') as time_file:
        print("Processes", file=time_file)
        for n_jobs in range(1, 2 * cpu_num + 1):
            time(n_jobs,
                 log_filename='artifacts/medium/log_processes.txt',
                 time_file=time_file,
                 executor=ProcessPoolExecutor,
                 current_function=current_process)

        print("\nThreads", file=time_file)
        for n_jobs in range(1, 2 * cpu_num + 1):
            time(n_jobs,
                 log_filename='artifacts/medium/log_threads.txt',
                 time_file=time_file,
                 executor=ThreadPoolExecutor,
                 current_function=current_thread)
