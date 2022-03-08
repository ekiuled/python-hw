from multiprocessing import Process, Queue, Pipe
from multiprocessing.connection import Connection
import codecs
from time import sleep


def a(input_queue: Queue, conn: Connection):
    while True:
        message = input_queue.get()
        conn.send(message.lower())
        sleep(5)


def b(conn: Connection, output_queue: Queue):
    while True:
        message = conn.recv()
        output_queue.put(codecs.encode(message, 'rot_13'))


def main(input_queue: Queue, output_queue: Queue):
    while True:
        message = input()
        input_queue.put(message)
        print(output_queue.get())


if __name__ == '__main__':
    input_queue = Queue()
    output_queue = Queue()
    conn_a, conn_b = Pipe()

    process_a = Process(target=a, args=(input_queue, conn_a))
    process_b = Process(target=b, args=(conn_b, output_queue))

    process_a.start()
    process_b.start()
    main(input_queue, output_queue)

    process_a.join()
    process_b.join()
