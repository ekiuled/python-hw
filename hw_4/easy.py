from threading import Thread
from multiprocessing import Process
from timeit import timeit
from astplot.fibonacci import fibonacci

repetitions = 10


def synchronous(n: int):
    for _ in range(repetitions):
        fibonacci(n)


def threading(n: int):
    threads = []
    for _ in range(repetitions):
        threads.append(Thread(target=fibonacci, args=(n,)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def multiprocessing(n: int):
    processes = []
    for _ in range(repetitions):
        processes.append(Process(target=fibonacci, args=(n,)))

    for process in processes:
        process.start()

    for process in processes:
        process.join()


def time(stmt: str, timeit_number: int = 10):
    seconds = timeit(stmt, number=timeit_number, globals=globals()) / timeit_number
    print(f'{seconds * 1000 :.1f} ms\t{stmt}')


if __name__ == '__main__':
    n = 100_000
    time('synchronous(n)')
    time('threading(n)')
    time('multiprocessing(n)')
