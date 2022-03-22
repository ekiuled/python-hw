from multiprocessing import Process, Queue, Pipe
from multiprocessing.connection import Connection
import codecs
from time import sleep
from datetime import datetime


def logger(filename: str, process_name: str):
    def log(message: str):
        with open(filename, 'a') as file:
            print(f'{datetime.now().strftime("%H:%M:%S")} {process_name} {message}', file=file)
    return log


def a(input_queue: Queue, conn: Connection, log):
    while (message := input_queue.get()) is not None:
        message = message.lower()
        log(f'sends "{message}"')
        conn.send(message)
        sleep(5)
    conn.send(None)


def b(conn: Connection, output_queue: Queue, log):
    while (message := conn.recv()) is not None:
        message = codecs.encode(message, 'rot_13')
        log(f'sends "{message}"')
        output_queue.put(message)


def main(input_queue: Queue, output_queue: Queue, log):
    try:
        while True:
            message = input()
            log(f'received "{message}"')
            input_queue.put(message)
            message = output_queue.get()
            log(f'prints "{message}"')
            print(message)
    except EOFError:
        input_queue.put(None)
        log('exits...')


if __name__ == '__main__':
    input_queue = Queue()
    output_queue = Queue()
    conn_a, conn_b = Pipe()

    LOG_FILENAME = 'artifacts/hard/log.txt'

    process_a = Process(target=a, args=(input_queue, conn_a, logger(LOG_FILENAME, 'A')))
    process_b = Process(target=b, args=(conn_b, output_queue, logger(LOG_FILENAME, 'B')))

    process_a.start()
    process_b.start()

    main(input_queue, output_queue, logger(LOG_FILENAME, 'Main'))

    process_a.join()
    process_b.join()
