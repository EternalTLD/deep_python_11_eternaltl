import threading
import time
from requests import Response

from client import Client
from server import Server


def setup_urls(filename):
    urls = []
    with open(filename, "r", encoding="utf-8") as file_object:
        for url in file_object:
            urls.append(url.strip())
    urls.append("SHUTDOWN")
    return urls


def test_client(mocker, capsys):
    urls = setup_urls("06/urls.txt")

    recv_mock = mocker.patch(
        "socket.socket.recv", return_value='{"word1": 6}'.encode("utf-8")
    )
    connect_mock = mocker.patch("socket.socket.connect")
    send_mock = mocker.patch("socket.socket.send")

    client = Client(3, "06/urls.txt")
    client.start()

    client_print = capsys.readouterr().out

    recv_data = client_print.split("\n")[:-1]
    expected_recv_data = [url + ": {'word1': 6}" for url in urls if url != "SHUTDOWN"]

    send_data = [data[0][0] for data in send_mock.call_args_list]
    expected_send_data = [url.encode("utf-8 ") for url in urls]

    assert sorted(recv_data) == sorted(expected_recv_data)
    assert sorted(send_data) == sorted(expected_send_data)
    assert recv_mock.call_count == 100
    assert send_mock.call_count == 101
    assert connect_mock.call_count == 101


def test_server_master(mocker):
    server = Server(2, 10)

    accept_mock = mocker.patch("socket.socket.accept")
    socket_mock = mocker.patch("socket.socket")
    accept_mock.side_effect = [(socket_mock, None) for _ in range(3)]

    master = threading.Thread(target=server.listen_client_connection)
    master.start()
    time.sleep(0.01)
    server.shutdown_event.set()
    master.join()

    assert server.clients_queue.qsize() == 3
    assert server.clients_queue.get() == socket_mock
    assert server.clients_queue.qsize() == 2


def test_server_valid_url(mocker, capsys):
    urls = setup_urls("06/urls.txt")

    socket_mock = mocker.patch("socket.socket")
    mocker.patch("queue.Queue.get", return_value=socket_mock)
    send_mock = mocker.patch("socket.socket.send")
    parse_html_mock = mocker.patch(
        "server.Server.get_text_from_html", return_value="Mock text"
    )

    count_words_data = [f"Count words {i}" for i in range(100)]
    count_words_mock = mocker.patch(
        "server.Server.get_most_common_words", side_effect=count_words_data
    )

    recv_data = [url.encode("utf-8") for url in urls]
    recv_mock = mocker.patch("socket.socket.recv", side_effect=recv_data)

    server = Server(1, 10)
    server.start()

    server_print = capsys.readouterr().out
    server_statistics = server_print.split("\n")[:-1]
    expected_server_statistics = [f"Proccessed {i+1} urls" for i in range(100)]

    send_data = [data[0][0] for data in send_mock.call_args_list]
    expected_send_data = [data.encode("utf-8") for data in count_words_data]

    assert sorted(server_statistics) == sorted(expected_server_statistics)
    assert sorted(send_data) == sorted(expected_send_data)
    assert recv_mock.call_count == 101
    assert send_mock.call_count == 100
    assert count_words_mock.call_count == 100
    assert parse_html_mock.call_count == 100
    assert server.shutdown_event.is_set()


def test_server_invalid_url(mocker, capsys):
    invalid_urls = ["htp:/broken.com", "another.broken.com", ""]
    invalid_urls.append("SHUTDOWN")

    socket_mock = mocker.patch("socket.socket")
    mocker.patch("queue.Queue.get", return_value=socket_mock)
    send_mock = mocker.patch("socket.socket.send")
    parse_html_mock = mocker.patch(
        "server.Server.get_text_from_html", return_value="Mock"
    )
    count_words_mock = mocker.patch(
        "server.Server.get_most_common_words", side_effect="Mock"
    )

    recv_data = [url.encode("utf-8") for url in invalid_urls]
    recv_mock = mocker.patch("socket.socket.recv", side_effect=recv_data)

    server = Server(1, 10)
    server.start()

    server_print = capsys.readouterr().out
    server_statistics = server_print.split("\n")[:-1]
    expected_server_statistics = [f"Proccessed {i+1} urls" for i in range(3)]

    send_data = [data[0][0] for data in send_mock.call_args_list]
    expected_send_data = ["URL is broken".encode("utf-8") for _ in range(3)]

    assert sorted(server_statistics) == sorted(expected_server_statistics)
    assert sorted(send_data) == sorted(expected_send_data)
    assert recv_mock.call_count == 4
    assert send_mock.call_count == 3
    assert parse_html_mock.call_count == 0
    assert count_words_mock.call_count == 0
    assert server.shutdown_event.is_set()


def test_get_text_from_html(mocker):
    response = Response()
    response._content = "<html>Some text with <a>link</a></html>".encode("utf-8")
    mocker.patch("requests.get", return_value=response)
    server = Server(1, 3)
    html_text = server.get_text_from_html("https://somesite.com")
    assert html_text == "Some text with link"


def test_get_most_common_words():
    server = Server(1, 2)

    text = "Test, teStiNg. Testcase // test, test."
    expected_data = '{"test": 3, "testing": 1}'
    count_words = server.get_most_common_words(text)
    assert count_words == expected_data

    text = None
    expected_data = "Data is broken"
    count_words = server.get_most_common_words(text)
    assert count_words == expected_data
