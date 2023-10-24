import socket
import threading
from queue import Queue
import time


class Client:

    def __init__(self, threads_number=5, file='06/test.txt', host='127.0.0.1', port=2000) -> None:
        self.threads_number = threads_number
        self.file = file
        self.host = host
        self.port = port
        self.task_queue = Queue()

    def work(self):
        threads = [
            threading.Thread(target=self.send_urls)
            for _ in range(self.threads_number)
        ]

        for thread in threads:
            thread.start()

        self.fetch_urls()

        for thread in threads:
            thread.join()

    def send_urls(self):
        while True:
            client_socket = socket.socket()
            client_socket.connect((self.host, self.port))
            thread = threading.current_thread()
            url = self.task_queue.get()
            # if url is None:
            #     self.queue.put(None)
            #     print(f"Thread - {thread.name} is stopped")
            #     return
            print(f"{url} from thread - {thread.name}")
            url = url.encode() + '\n'.encode()
            client_socket.send(url)
            data = client_socket.recv(4096).decode('utf-8')
            print(data)

    def fetch_urls(self):
        with open(file=self.file, encoding='utf-8') as file_object:
            for url in file_object:
                self.task_queue.put(url.strip())
            self.task_queue.put(None)


if __name__ == "__main__":
    client = Client()
    client.work()
