from io import StringIO
import socket
import threading
import time

import pytest
from client import Client
from server import Server
from unittest import mock
from requests import Response, patch


def test_client(mocker, capsys):
    urls = []
    with open('06/urls.txt', 'r') as file_object:
        for url in file_object:
            urls.append(url.strip())
    urls.append("SHUTDOWN")

    expected_recv_data = [url + ": {'word1': 6, 'word2': 5}" for url in urls if url != "SHUTDOWN"]
    expected_send_data = [url.encode("utf-8 ") for url in urls]

    recv_mock = mocker.patch(
        "socket.socket.recv", 
        return_value='{"word1": 6, "word2": 5}'.encode("utf-8")
    )
    connect_mock = mocker.patch("socket.socket.connect")
    send_mock = mocker.patch("socket.socket.send")

    client = Client(3, '06/urls.txt')
    client.start()
    captured = capsys.readouterr()
    recv_data = [data for data in captured.out.split("\n")[:-1]]
    send_data = [data[0][0] for data in send_mock.call_args_list]

    assert sorted(recv_data) == sorted(expected_recv_data)
    assert sorted(send_data) == sorted(expected_send_data)
    assert recv_mock.call_count == 100
    assert send_mock.call_count == 101
    assert connect_mock.call_count == 101


def test_server_master():
    server = Server(workers_number=2, most_common_words_number=10, host="127.0.0.1", port=4000)
    master_thread = threading.Thread(target=server.listen_client_connection)
    master_thread.start()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 4000))
    client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket2.connect(("127.0.0.1", 4000))
    client_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket3.connect(("127.0.0.1", 4000))

    server.shutdown_event.set()
    master_thread.join()
    assert server.clients_queue.qsize() == 3


# def test_server_broken_url():
#     server = Server(workers_number=2, most_common_words_number=10, port=5000)
#     s_th = threading.Thread(target=server.start)
#     s_th.start()

#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect(('127.0.0.1', 5000))

#     client_socket.send(b'not_a_url')
#     response = client_socket.recv(4096).decode("utf-8")
#     assert "URL is broken" in response

#     time.sleep(1)

#     client_socket.send(b'SHUTDOWN')
#     response = client_socket.recv(4096).decode("utf-8")
#     assert "URL is broken" not in response

#     server.shutdown_event.set()
#     s_th.join()



# def test_server_worker(mocker, capsys):
#     urls = [f"URL {i}".encode('utf-8') for i in range(100)]
#     urls.append("SHUTDOWN")
#     server = Server(workers_number=1, most_common_words_number=3, port=5000)
#     server.clients_queue.put(mock.MagicMock())
#     worker_thread = threading.Thread(target=server.proccess_url)
#     worker_thread.start()
#     recv_mock = mocker.patch("socket.socket.recv", return_value="urls")
#     parse_mock = mocker.patch("server.Server.parse_html", return_value="text")
#     count_mock = mocker.patch("server.Server.count_words", return_value='{"word": 2, "test": 1}')

#     send_mock = mocker.patch("socket.socket.send", return_value="text".encode('utf-8'))
#     server.shutdown_event.set()
#     worker_thread.join()
#     captured = capsys.readouterr()
#     print_data = [data for data in captured.out.split("\n")[:-1]]
#     # assert print_data is False
#     assert parse_mock.call_args_list is False

def test_parse_html(mocker):
    response = Response()
    response._content = "<html>Some text with <a>link</a></html>".encode('utf-8')
    mocker.patch("requests.get", return_value=response)
    server = Server(1, 3)
    html_text = server.parse_html("https://somesite.com")
    assert html_text == "Some text with link"


def test_count_words():
    server = Server(1, 2)
    text = "Test, teStiNg. Testcase // test, test."
    expected_data = '{"test": 3, "testing": 1}'
    count_words = server.count_words(text)
    assert count_words == expected_data
