import re
import socket
import threading
import json
from collections import Counter
from queue import Queue
import requests
from bs4 import BeautifulSoup


class Server:
    count_urls = 0

    def __init__(
        self, workers_number, most_common_words_number, host="127.0.0.1", port=3000
    ) -> None:
        self.host = host
        self.port = port
        self.workers_number = workers_number
        self.most_common_words_number = most_common_words_number
        self.clients_queue = Queue()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))

    def start(self):
        self.socket.listen()
        master = threading.Thread(target=self.listen_client, name="Master")
        master.start()
        workers = [
            threading.Thread(target=self.proccess_url, name=f"Worker {i+1}")
            for i in range(self.workers_number)
        ]

        for worker in workers:
            worker.start()

        for worker in workers:
            worker.join()

    def listen_client(self):
        while True:
            try:
                client_socket, _ = self.socket.accept()
                self.clients_queue.put(client_socket)
            except Exception:
                continue

    def proccess_url(self):
        while True:
            client_socket = self.clients_queue.get()
            url = client_socket.recv(4096).decode("utf-8")
            data = self.parse_html(url)
            client_socket.send(data.encode("utf-8"))

            with threading.Lock():
                self.count_urls += 1
                print(f"Proccessed {self.count_urls} urls.")

    def parse_html(self, url):
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        page_text = soup.get_text().lower()
        words = re.findall(r'\b[А-Яа-яA-Za-z]+\b', page_text)
        most_common_words = Counter(words).most_common(
            self.most_common_words_number
        )
        most_common_words_dict = {}
        for word, counter in most_common_words:
            most_common_words_dict[word] = counter
        most_common_words_json = json.dumps(most_common_words_dict)
        return most_common_words_json


if __name__ == "__main__":
    server = Server(50, 7)
    server.start()
