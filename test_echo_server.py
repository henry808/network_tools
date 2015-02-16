import pytest
import socket


def test_server_text(test_socket):
    test_socket().sendall("this is a test")
    test_socket().shutdown(socket.SHUT_WR)

    text = test_socket().recv(32)
    test_socket().close()
    print text
    assert text == "this is a test"


@pytest.fixture(scope='function')
def test_socket():
    test_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
        socket.IPPROTO_IP)
    test_socket.connect(('127.0.0.1', 50000))
    return test_socket
