import socket
import threading
from queue import Queue
import json


class Client:

    def __init__(self, threads_number=5, file='06/test.txt', host='127.0.0.1', port=3000):
        self.threads_number = threads_number
        self.file = file
        self.host = host
        self.port = port
        self.url_queue = Queue()

    def start(self):
        threads = [
            threading.Thread(target=self.send_urls, name=f'Thread - {i+1}')
            for i in range(self.threads_number)
        ]

        for thread in threads:
            thread.start()

        self.fetch_urls()

        for thread in threads:
            thread.join()

    def send_urls(self):
        while True:
            url = self.url_queue.get()
            thread = threading.current_thread()
            if url is None:
                self.url_queue.put(None)
                print(f"{thread.name} is stopped")
                break

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            client_socket.send(url.encode('utf-8'))

            data = json.loads(client_socket.recv(4096).decode('utf-8'))
            print(data)
            client_socket.close()

    def fetch_urls(self):
        with open(file=self.file, encoding='utf-8') as file_object:
            for url in file_object:
                self.url_queue.put(url.strip())
            self.url_queue.put(None)


if __name__ == "__main__":
    client = Client()
    client.start()
