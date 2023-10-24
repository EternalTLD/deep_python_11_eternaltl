import socket
import threading
from queue import Queue
import time


class Server:

    def __init__(self, workers_number=1, host='127.0.0.1', port=2000) -> None:
        self.host = host
        self.port = port
        self.workers_number = workers_number
        self.queue = Queue()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.res_queue = Queue()

    def start(self):
        self.socket.listen(5)
        client_socket, address = self.socket.accept()
        for i in range(self.workers_number):
            worker = threading.Thread(target=self.proccess_url, name=f'Worker {i}')
            worker.start()
        resper = threading.Thread(target=self.send_resp, name="resp")
        resper.start()
        listener = threading.Thread(target=self.listen_client, args=(client_socket, address), name="Listener")
        listener.start()

    def listen_client(self, client_socket, addres):
        while True:
            client_data = client_socket.recv(4096)
            if client_data:
                sep_data = client_data.decode().split('\n')
                for i in range(len(sep_data)):
                    if sep_data[i] != '':
                        self.queue.put(sep_data[i])

    def proccess_url(self):
        while True:
            th = threading.current_thread()
            url = self.queue.get()
            resp = f"SERVER proccessed {url} TH - {th.name}"
            self.res_queue.put(resp)

    def send_resp(self):
        while True:
            resp = self.res_queue.get()
            print(resp)

if __name__ == "__main__":
    server = Server()
    server.start()
