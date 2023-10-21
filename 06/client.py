import socket
import threading
import time

class Client:

    def __init__(self, threads_number=3, file='06/test.txt', host='127.0.0.1', port=2000) -> None:
        self.threads_number = threads_number
        self.file = file
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self):
        self.socket.connect((self.host, self.port))
        print(f"[CONNECTED] - Connected by {(self.host, self.port)}")
        self.run_threads()
        data = self.socket.recv(1024)
        print(data.decode('utf-8'))

    def run_threads(self):
        threads = [
            threading.Thread(target=self.send_urls)
            for _ in range(self.threads_number)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def send_urls(self):
        with open(file=self.file, encoding='utf-8') as file_object:
            for url in file_object:
                self.socket.sendall(url.encode())


if __name__ == "__main__":
    client = Client()
    client.send()
